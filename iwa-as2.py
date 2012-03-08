import cgi
import datetime
import wsgiref.handlers
import os
import re

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch

from xml.etree import ElementTree as etree

from rdflib.graph import ConjunctiveGraph
from rdflib.term import URIRef, Literal
from rdflib.namespace import Namespace, RDF, RDFS
    
class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {
        }

        path = os.path.join(os.path.dirname(__file__), "index.html")
        self.response.out.write(template.render(path, template_values))

    def post(self):
        query = self.request.get("content")
        nrOfResults = self.request.get("amount")

        try:
            number = int(nrOfResults)
        except ValueError:
            number = 0

        literals = re.findall(r'"(.+?)"',query)

        urls = processLiterals(literals, number)

        graph = ConjunctiveGraph()

        for url in urls:
            # Original URL fetch
            xmlresult = urlfetch.fetch(url,deadline=60,method=urlfetch.GET)

            if xmlresult.status_code == 200:

                iwa = Namespace('http://iwa2012-18-2.appspot.com/#')
                idns = Namespace('http://iwa2012-18-2.appspot.com/id/#')
                venuens = Namespace('http://iwa2012-18-2.appspot.com/venueid/#')

                tree = etree.fromstring(xmlresult.content)
                for event in tree.findall('events/event'):
                    id = event.attrib['id']
                    title = event.find('title')
                    url = event.find('url')
                    venueid = event.find('venue_id')
                    venueurl = event.find('venue_url')
                    venuename = event.find('venue_name')

                    graph.add((idns[id], iwa['hasTitle'], Literal(title.text)))
                    graph.add((idns[id], iwa['hasUrl'], Literal(url.text)))
                    graph.add((venuens[id], iwa['hasVenueName'], Literal(venuename.text)))
                    graph.add((venuens[id], iwa['hasUrl'], Literal(venueurl.text)))
                    graph.add((idns[id], iwa['atVenue'], venuens[id])))

            else:
                print "Something went wrong with the connection to the Eventful server. Status code: " + xml.status_code

        print graph.serialize()

def create_callback(rpc):
    return lambda: handle_result(rpc)

def processLiterals(list, number):
    if number > 0:
        numberstr = str(number)
        baseurl = "http://api.eventful.com/rest/events/search?app_key=fZbWS6qHrqnNvPW7&page_size=" + numberstr + "&keywords="
    else:
        baseurl = "http://api.eventful.com/rest/events/search?app_key=fZbWS6qHrqnNvPW7&keywords="

    urls = []
    i=0
    for item in list:
        item = item.replace(" ", "+")
        url = baseurl + item
        urls.insert(i,url)
        i=i+1

    return urls

application = webapp.WSGIApplication([('/', MainPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
