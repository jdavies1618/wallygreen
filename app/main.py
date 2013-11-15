import hashlib
import logging
import os
import urllib

from google.appengine.api import users
from google.appengine.ext.webapp import template
from models.store import PlayerForm
import webapp2


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
			context = {
				"username": user.nickname(),
				'user': user,
				'gravatar_url': get_gravatar_url(user.email()),
				"logout_url": users.create_logout_url("/")
			}
			context.update(tvals)
			
			cpath = os.path.join(os.path.dirname(__file__), 'templates/%s.html' % tname)
			self.response.out.write(template.render(cpath, context))
			

class MainPage(Page):

	def get(self):
		tvals = {}
		self.yield_page("index", tvals)

class Profile(Page):

	def get(self):
		
		tvals = {}
		self.yield_page("profile", tvals)

class AddPlayer(Page):
	def get(self):
		self.response.out.write('<html><body>'
								'<form method="POST" '
								'action="/player">'
								'<table>')
		self.response.out.write(PlayerForm())
		self.response.out.write('</table>'
								'<input type="submit">'
								'</form></body></html>')
	def post(self):
		data=PlayerForm(data=self.request.POST)
		if data.is_valid():
			entity = data.save(commit=False)
			entity.put()
		else:
			self.response.out.write('<html><body>'
					'<form method="POST" '
					'action="/player">'
					'<table>')
			self.response.out.write(PlayerForm())
			self.response.out.write('</table>'
									'<input type="submit">'
									'</form></body></html>')

class Rankings(Page):

	def get(self):
		pass

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/profile', Profile),
	('/rankings', Rankings),
	('/player', AddPlayer)
], debug=True)



# This should be a template tag.

DEFAULT_SIZE =20 
DEFAULT_URL = 'http://t3.gstatic.com/images?q=tbn:ANd9GcRos9zoopqiNEf586EHxFxoP1YK4-oTxTDWAJ1qsWdzEP5P_2l0TQ'
def get_gravatar_url(email, size=DEFAULT_SIZE, default_url=DEFAULT_URL):
	# construct the url
	gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
	gravatar_url += urllib.urlencode({'d':default_url, 's':str(size)})
	return gravatar_url
