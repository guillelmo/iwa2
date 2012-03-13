import cgi
import datetime
import wsgiref.handlers
import os
import re
import urllib
import urllib2
from django.utils import simplejson as json

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
from google.appengine.dist import use_library

from xml.etree import ElementTree as etree

from rdflib.graph import ConjunctiveGraph
from rdflib.term import URIRef, Literal
from rdflib.namespace import Namespace, RDF, RDFS

rdfStoreUrl = 'http://ct.filmaffinity.com:26080/openrdf-sesame/'
#rdfStoreUrl = 'http://localhost:8081/openrdf-sesame/'

class MainPage(webapp.RequestHandler):
    
    def get(self):
        template_values = {
        }

        path = os.path.join(os.path.dirname(__file__), "index.html")
        self.response.out.write(template.render(path, template_values))

    def post(self):
        query = self.request.get("content")

        literals = re.findall(r'"(.+?)"',query)

        urls = processLiterals(literals)

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
                    graph.add((idns[id], iwa['atVenue'], venuens[id]))

                # self.response.out.write("mygraph")   
                # self.response.out.write(graph)
                storeRDF(graph)
                
                #if(int(res) != 200):
                #self.response.out.write("Something went wrong storing the RDF:  "+str(res))
                #   return
                
            else:
                print "Something went wrong with the connection to the Eventful server. Status code: " + xml.status_code
        
        res = queryRdfStore(query)

        if(type(res) is list):

            if(len(res) == 0):
                self.response.out.write("Empty")
                return 

            mList = []
            for row in res:

                aux = []
                for key,value in row.iteritems():
                    aux.append(value)

                row_tuple = tuple(aux)
                mList.append(row_tuple)

            template_values = {'res':mList, 'values': res[1].keys(), 'numVariables': len(res[1].keys())}        

            path = os.path.join(os.path.dirname(__file__), "results.html")
            #self.response.out.write(mList)
            self.response.out.write(template.render(path, template_values))
        else:
            print "error: "
            print res


def storeRDF(graph):
                    
    data=graph.serialize(format='xml')    
    url = rdfStoreUrl + "repositories/iwa/statements"

    # headers={ 'content-type': 'application/rdf+xml'}    
    # req = urllib2.Request(url,data, headers)
    
    # response = urllib2.urlopen(req)
    
    jsonresult = urlfetch.fetch(url,payload=data,deadline=30,method=urlfetch.POST, headers={ 'content-type': 'application/rdf+xml'})
    #return jsonresult.code
    #return url
    #return response.code
        

def queryRdfStore(query):

    url = rdfStoreUrl + "repositories/iwa?" + urllib.urlencode({"query" : query})

    jsonresult = urlfetch.fetch(url,deadline=30,method=urlfetch.GET, headers={"accept" : "application/sparql-results+json"})

    if(jsonresult.status_code == 200):
        res = json.loads(jsonresult.content)
        
        res_var = res['head']['vars']
        
        response = []
        for row in res['results']['bindings']:
            dic = {}
            for var in res_var:
                dic[var] = row[var]['value']
                
            response.append(dic)
                        
        return response    
    else:
        return {"error" : jsonresult.content} 
    
def create_callback(rpc):
    return lambda: handle_result(rpc)

def processLiterals(list):

    # if number > 0:
    #     numberstr = str(number)
    #     baseurl = "http://api.eventful.com/rest/events/search?app_key=fZbWS6qHrqnNvPW7&page_size=" + numberstr + "&keywords="
    # else:
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
