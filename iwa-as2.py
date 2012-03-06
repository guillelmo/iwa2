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

        for url in urls:
            xml = urlfetch.fetch(url)
            if xml.status_code == 200:
                print "XML retrieved."
            else:
                print "Something went wrong with the connection to the Eventful server. Status code: " + xml.status_code

def processLiterals(list):
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
