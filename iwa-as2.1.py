import cgi
import datetime
import wsgiref.handlers
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch


    
class MainPage(webapp.RequestHandler):
    def get(self):
        url = "http://api.eventful.com/rest/events/search?app_key=fZbWS6qHrqnNvPW7&keywords=bombay+show+pig"

        template_values = {
        }

        result = urlfetch.fetch(url)

        if result.status_code == 200:
            self.response.out.write(result.content)
        else:
            path = os.path.join(os.path.dirname(__file__), "index2.html")
            self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/', MainPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
