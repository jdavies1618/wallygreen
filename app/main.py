import os

from google.appengine.api import users
from google.appengine.ext.webapp import template

import webapp2
import logging

class Page(webapp2.RequestHandler):

	"""This is the generic page handler.

	method to render any template on the server, and also automatically loads
	related static content, and places the home bar at the top of the page.
	"""

	def yield_page(self, tname, tvals):
		user = users.get_current_user()
		if user is None:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			cpath = os.path.join(os.path.dirname(__file__), 'templates/{}.html')
			content = template.render(cpath.format(tname), tvals)
			path = os.path.join(os.path.dirname(__file__), 'templates/layout.html')
			self.response.out.write(template.render(path, {
				"tname": tname,
				"yield": content,
				"username": user.nickname(),
				"logout_url": users.create_logout_url("/")
			}))

class MainPage(Page):

	def get(self):
		tvals = {}
		self.yield_page("index", tvals)

class Profile(Page):

	def get(self):
		pass

class Rankings(Page):

	def get(self):
		pass

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/profile', Profile),
	('/rankings', Rankings),
], debug=True)