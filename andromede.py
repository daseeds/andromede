# -*- coding: utf-8 -*-
import os
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
from webapp2_extras import routes
import jinja2

DEFAULT_SITE_NAME = 'default_site'

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])

def jinja2_factory(app):
    j = jinja2.Jinja2(app)
    j.environment.filters.update({
        #'naturaldelta':naturaldelta,
        })
    j.environment.globals.update({
        # 'Post': Post,
        #'ndb': ndb, # could be used for ndb.OR in templates
        })
    return j

def site_key(site_name=DEFAULT_SITE_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Site', site_name)


class SiteContent(ndb.Model):
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    block_1_3_heading = ndb.StringProperty()
    block_1_3_content = ndb.StringProperty()
    block_2_1_heading = ndb.StringProperty()
    block_2_1_content = ndb.StringProperty()
    block_2_2_heading = ndb.StringProperty()
    block_2_2_content = ndb.StringProperty()

class History(ndb.Model):
	author = ndb.UserProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(factory=jinja2_factory)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)

class MainPage(BaseHandler):

	def get(self):
		site_name = self.request.get('site_name', DEFAULT_SITE_NAME)
		sitecontent_query = SiteContent.query(ancestor=site_key(site_name))
		sitecontent = sitecontent_query.fetch(1)
		template_values = {
		'description': u"Un soin énergétique apaise et soulage. Il revitalise et redynamise le corps en réactivant la force vitale de l'être. Le soin agit à la fois sur un plan physique, psychique et émotionnel.",
		'title': u"Chantal Jean - Soins Energétiques Traditionnels",
		'base_url': u"http://chantaljean.juganville.com",
		#'url': u"http://chantaljean.juganville.com/soins-energetiques-valognes-chantal-jean/",
		'url': u"http://chantaljean.juganville.com/",
		}
		self.render_response('view/index.html', template_values)

class RedirectPage(webapp2.RequestHandler):

	def get(self):
		self.redirect('/soins-energetiques-valognes-chantal-jean')


class TestPage(webapp2.RequestHandler):

	def get(self):
		template = JINJA_ENVIRONMENT.get_template('view/index2.html')
		self.response.write(template.render())


class AdminPage(webapp2.RequestHandler):
	def get(self):
		if not users.get_current_user():
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			template_values = {
				'url': url,
				'url_linktext': url_linktext,
			}
			template = JINJA_ENVIRONMENT.get_template('view/admin.html')
			return  self.response.write(template.render(template_values))

		url = users.create_logout_url(self.request.uri)
		url_linktext = 'Logout'


		template_values = {
			'url': url,
			'url_linktext': url_linktext,
			'user': users.get_current_user(),
		}	
		template = JINJA_ENVIRONMENT.get_template('view/admin.html')
		self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
	webapp2.Route('/', handler=MainPage, name='redirect'),
	webapp2.Route('/soins-energetiques-valognes-chantal-jean', handler=MainPage, name='main'),
	webapp2.Route('/2', handler=TestPage, name='test'),
	webapp2.Route('/admin', handler=AdminPage, name='admin'),
	], debug=True)

#uri = webapp2.uri_for('main', _full=True)

