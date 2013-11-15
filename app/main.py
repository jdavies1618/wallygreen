import logging
import os
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template
from models.store import PlayerForm
import webapp2

from app.models.store import Player, League
from models.store import PlayerForm

from util import get_gravatar_url

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

			player = Player.get_player(user)

			context = {
				"username": user.nickname(),
				'user': user,
				'player': player,
				'gravatar_url': get_gravatar_url(user.email()),
				"logout_url": users.create_logout_url("/"),
				"games_played": 45,
				"games_won": 32,
				"rating": 1600
			}
			context.update(tvals)

			cpath = os.path.join(os.path.dirname(__file__), 'templates/%s.html' % tname)
			self.response.out.write(template.render(cpath, context))

class MainPage(Page):

	def get(self):
		
		leagues = League.all()
		
		tvals = {
				'leagues': leagues
				}
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
