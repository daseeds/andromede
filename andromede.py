# -*- coding: utf-8 -*-
import os
import urllib
import webapp2
import logging
from functools import wraps
from webapp2_extras.routes import RedirectRoute
from webapp2_extras import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

DEFAULT_SITE_NAME = 'default_site'

# JINJA_ENVIRONMENT = jinja2.Environment(
# 	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
# 	extensions=['jinja2.ext.autoescape'])

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


PREVIOUS = 1
CURRENT = 2

class SiteContent(ndb.Model):
    STATUS_CHOICES = (
        (PREVIOUS, 'Previous'),
        (CURRENT, 'Current'),
    )
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty()
    main_title = ndb.StringProperty()
    description = ndb.StringProperty()
    tags = ndb.StringProperty()
    block_1_3_content = ndb.TextProperty()
    block_2_1_content = ndb.TextProperty()
    block_2_2_content = ndb.TextProperty()
    block_1_3_heading = ndb.StringProperty()
    block_2_1_heading = ndb.StringProperty()
    block_2_2_heading = ndb.StringProperty()
    status = ndb.IntegerProperty(default=CURRENT, choices=[PREVIOUS, CURRENT])
    picture = ndb.BlobKeyProperty()
    background = ndb.BlobKeyProperty()

def admin_protect(f):
    @wraps(f)
    def decorated_function(self, *args, **kwargs):
        user = users.get_current_user()
        if not user or not users.is_current_user_admin():
            return self.redirect(users.create_login_url(self.request.uri))
        return f(self, *args, **kwargs)
    return decorated_function

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
		# site_name = self.request.get('site_name', DEFAULT_SITE_NAME)
		# sitecontent_query = SiteContent.query(ancestor=site_key(site_name))
		# sitecontent = sitecontent_query.fetch(1)

		sitecontent = SiteContent.get_or_insert(DEFAULT_SITE_NAME, status=CURRENT)


		template_values = {
		'title': u"Chantal Jean - Soins Energétiques Traditionnels",
		'base_url': u"http://chantaljean.fr",
		#'url': u"http://chantaljean.juganville.com/soins-energetiques-valognes-chantal-jean/",
		'url': u"http://chantaljean.fr/",
		'sitecontent': sitecontent,
		}
		self.render_response('index.html', **template_values)

class RedirectPage(webapp2.RequestHandler):

	def get(self):
		self.redirect('/soins-energetiques-valognes-chantal-jean')


class TestPage(webapp2.RequestHandler):

	def get(self):
		template = JINJA_ENVIRONMENT.get_template('view/index2.html')
		self.response.write(template.render())


class AdminPage(BaseHandler):
	@admin_protect
	def get(self):

		url = users.create_logout_url(self.request.uri)
		url_linktext = 'Logout'

		keyname = "some_key"
		site_name = self.request.get('site_name', DEFAULT_SITE_NAME)
		sitecontent = SiteContent.get_or_insert(DEFAULT_SITE_NAME, status=CURRENT)

		# site_name = self.request.get('site_name', DEFAULT_SITE_NAME)
		# sitecontent_query = SiteContent.query(ancestor=site_key(site_name)).order(SiteContent.date)
		# sitecontent = sitecontent_query.fetch(1)

		# if len(sitecontent) == 0:
		# 	sitecontent.append(SiteContent())

		#picture = BlobInfo(sitecontent.picture)

		template_values = {
			'url': url,
			'url_linktext': url_linktext,
			'user': users.get_current_user(),
			'sitecontent': sitecontent,
			'upload_url': blobstore.create_upload_url('/upload'),
			'picture': '/serve/%s' % sitecontent.picture,
		}	
		return self.render_response('admin.html', **template_values)


class AdminUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	@admin_protect
	def post(self):

		sitecontent_prev = SiteContent.get_or_insert('test', status=PREVIOUS)
		sitecontent = SiteContent.get_or_insert(DEFAULT_SITE_NAME, status=CURRENT)

		if self.get_uploads('picture'):
			upload_files = self.get_uploads('picture')  # 'file' is file upload field in the form	
			blob_info = upload_files[0]
			sitecontent.picture = blob_info.key()
		elif self.get_uploads('background'):
			upload_files = self.get_uploads('background')  # 'file' is file upload field in the form	
			blob_info = upload_files[0]
			sitecontent.background = blob_info.key()
		else:
			return self.error(404)
		
		sitecontent.put()

		self.redirect('/admin')

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, resource):
		try:
			logging.info("ServeHandler resource: %s", resource)
			resource = str(urllib.unquote(resource))
			blob_info = blobstore.BlobInfo.get(resource)
			self.send_blob(blob_info)
		except (ValueError, TypeError):
			self.response.out.write("bug")


class AdminUpdate(BaseHandler):
	@admin_protect
	def post(self):

		sitecontent_prev = SiteContent.get_or_insert('test', status=PREVIOUS)
		sitecontent = SiteContent.get_or_insert(DEFAULT_SITE_NAME, status=CURRENT)

		# site_name = self.request.get('site_name', DEFAULT_SITE_NAME)
		# sitecontent_query = SiteContent.query(ancestor=site_key(site_name)).order(SiteContent.date)
		# sitecontent = sitecontent_query.fetch(1)

		# site_name = self.request.get('site_name', DEFAULT_SITE_NAME)
		# sitecontent = SiteContent(parent=site_key(site_name))

		sitecontent_prev = SiteContent.get_or_insert('test', status=PREVIOUS)
		sitecontent = SiteContent.get_or_insert(DEFAULT_SITE_NAME, status=CURRENT)

		sitecontent_prev.title = sitecontent.title
		sitecontent_prev.main_title = sitecontent.main_title
		sitecontent_prev.author = sitecontent.author
		sitecontent_prev.description = sitecontent.description
		sitecontent_prev.tags = sitecontent.tags
		sitecontent_prev.block_1_3_heading = sitecontent.block_1_3_heading
		sitecontent_prev.block_2_1_heading = sitecontent.block_2_1_heading
		sitecontent_prev.block_2_2_heading = sitecontent.block_2_2_heading
		sitecontent_prev.block_1_3_content = sitecontent.block_1_3_content
		sitecontent_prev.block_2_1_content = sitecontent.block_2_1_content
		sitecontent_prev.block_2_2_content = sitecontent.block_2_2_content
		sitecontent_prev.put()

		sitecontent.title = self.request.get('title')
		sitecontent.main_title = self.request.get('main_title')
		sitecontent.author = users.get_current_user()
		sitecontent.description = self.request.get('description')
		sitecontent.tags = self.request.get('tags')
		sitecontent.block_1_3_heading = self.request.get('block_1_3_heading')
		sitecontent.block_2_1_heading = self.request.get('block_2_1_heading')
		sitecontent.block_2_2_heading = self.request.get('block_2_2_heading')
		sitecontent.block_1_3_content = self.request.get('block_1_3_content')
		sitecontent.block_2_1_content = self.request.get('block_2_1_content')
		sitecontent.block_2_2_content = self.request.get('block_2_2_content')

		sitecontent.put()
		self.redirect('/admin')

class AdminRevert(BaseHandler):
	@admin_protect
	def post(self):

		sitecontent_prev = SiteContent.get_or_insert('test', status=PREVIOUS)
		sitecontent = SiteContent.get_or_insert(DEFAULT_SITE_NAME, status=CURRENT)
		sitecontent_temp = SiteContent()

		sitecontent_temp.title = sitecontent.title
		sitecontent_temp.main_title = sitecontent.main_title
		sitecontent_temp.author = sitecontent.author
		sitecontent_temp.description = sitecontent.description
		sitecontent_temp.tags = sitecontent.tags
		sitecontent_temp.block_1_3_heading = sitecontent.block_1_3_heading
		sitecontent_temp.block_2_1_heading = sitecontent.block_2_1_heading
		sitecontent_temp.block_2_2_heading = sitecontent.block_2_2_heading
		sitecontent_temp.block_1_3_content = sitecontent.block_1_3_content
		sitecontent_temp.block_2_1_content = sitecontent.block_2_1_content
		sitecontent_temp.block_2_2_content = sitecontent.block_2_2_content

		sitecontent.title = sitecontent_prev.title
		sitecontent.main_title = sitecontent_prev.main_title
		sitecontent.author = sitecontent_prev.author
		sitecontent.description = sitecontent_prev.description
		sitecontent.tags = sitecontent_prev.tags
		sitecontent.block_1_3_heading = sitecontent_prev.block_1_3_heading
		sitecontent.block_2_1_heading = sitecontent_prev.block_2_1_heading
		sitecontent.block_2_2_heading = sitecontent_prev.block_2_2_heading
		sitecontent.block_1_3_content = sitecontent_prev.block_1_3_content
		sitecontent.block_2_1_content = sitecontent_prev.block_2_1_content
		sitecontent.block_2_2_content = sitecontent_prev.block_2_2_content
		sitecontent.put()

		sitecontent_prev.title = sitecontent_temp.title
		sitecontent_prev.main_title = sitecontent_temp.main_title
		sitecontent_prev.author = sitecontent_temp.author
		sitecontent_prev.description = sitecontent_temp.description
		sitecontent_prev.tags = sitecontent_temp.tags
		sitecontent_prev.block_1_3_heading = sitecontent_temp.block_1_3_heading
		sitecontent_prev.block_2_1_heading = sitecontent_temp.block_2_1_heading
		sitecontent_prev.block_2_2_heading = sitecontent_temp.block_2_2_heading
		sitecontent_prev.block_1_3_content = sitecontent_temp.block_1_3_content
		sitecontent_prev.block_2_1_content = sitecontent_temp.block_2_1_content
		sitecontent_prev.block_2_2_content = sitecontent_temp.block_2_2_content

		sitecontent_prev.put()
		self.redirect('/admin')



debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

logging.getLogger().setLevel(logging.DEBUG)


application = webapp2.WSGIApplication([
	webapp2.Route('/serve/<:([^/]+)?>', ServeHandler, name='ServeHandler'),
	webapp2.Route('/', handler=MainPage, name='main'),
	webapp2.Route('/soins-energetiques-valognes-chantal-jean', handler=MainPage, name='main'),
	webapp2.Route('/2', handler=TestPage, name='test'),
	webapp2.Route('/admin', handler=AdminPage, name='admin'),
	webapp2.Route('/admin/update', handler=AdminUpdate, name='adminupdate'),
	webapp2.Route('/admin/revert', handler=AdminRevert, name='adminrevert'),
	webapp2.Route('/upload', handler=AdminUploadHandler, name='AdminUploadHandler'),

	], debug=debug)

#uri = webapp2.uri_for('main', _full=True)

