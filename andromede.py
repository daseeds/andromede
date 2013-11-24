import os
import urllib

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])

class MainPage(webapp2.RequestHandler):

	def get(self):
		template = JINJA_ENVIRONMENT.get_template('view/index.html')
		self.response.write(template.render())

class RedirectPage(webapp2.RequestHandler):

	def get(self):
		self.redirect('/soins-energetiques-valognes-chantal-jean')


class TestPage(webapp2.RequestHandler):

	def get(self):
		template = JINJA_ENVIRONMENT.get_template('view/index2.html')
		self.response.write(template.render())

application = webapp2.WSGIApplication([
	('/', RedirectPage),
	('/soins-energetiques-valognes-chantal-jean', MainPage),
	('/2', TestPage),
	], debug=True)