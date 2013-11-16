import logging
import webapp2
import os

from google.appengine.api import users
from google.appengine.ext.webapp import template
from models.store import PlayerForm, GameForm

from app.models.store import Player
from models.store import PlayerForm, PlayerForm
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
				"player": player,
				'gravatar_url': get_gravatar_url(user.email()),
				"logout_url": users.create_logout_url("/"),
			}
			context.update(tvals)

			cpath = os.path.join(os.path.dirname(__file__), 'templates/%s.html' % tname)
			self.response.out.write(template.render(cpath, context))

class MainPage(Page):

	def get(self):
		players_by_league = Player.get_players_by_league()
		players_by_league_l = []
		for league, players in players_by_league.iteritems():
			players_by_league_l.append(dict(league=league, players=players))

		user = users.get_current_user()
		if user is None:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			player = Player.get_player(user)
			form = GameForm()
			form.first_player = player
			tvals = {
				'form_data': form,
				'players_by_league': players_by_league_l
			}
			self.yield_page("index", tvals)

class StoreGame(Page):

	def post(self):
		user=users.get_current_user()
		if user is None:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			player = Player.get_player(user)
			data=GameForm(data=self.request.POST)
			if data.is_valid():
				entity = data.save(commit=False)
				entity.reporter = player
			 	entity.first_player_wins = (entity.first_score > entity.second_score)
				entity.put()
			self.redirect('/')

class Profile(Page):

	def get(self):
		tvals = {}
		self.yield_page("profile", tvals)

class Rankings(Page):

	def get(self):
		players_by_league = Player.get_players_by_league()
		players_by_league_l = []
		for league, players in players_by_league.iteritems():
			players_by_league_l.append(dict(league=league, players=players))
		tvals = {
			'players_by_league': players_by_league_l
		}
		self.yield_page("rankings", tvals)

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
			self.redirect('/')
		else:
			self.response.out.write('<html><body>'
					'<form method="POST" '
					'action="/player">'
					'<table>')
			self.response.out.write(PlayerForm())
			self.response.out.write('</table>'
									'<input type="submit">'
									'</form></body></html>')

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/profile', Profile),
	('/rankings', Rankings),
	('/player', AddPlayer),
	('/storegame', StoreGame)
], debug=True)
