import logging
import webapp2
import os

from google.appengine.api import users
from google.appengine.ext.webapp import template

import elo
from models.store import Player, Game
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
				"gravatar_url": get_gravatar_url(user.email()),
				"logout_url": users.create_logout_url("/"),
				"tname":tname
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

		players_by_league_l.reverse()
		user = users.get_current_user()
		if user is None:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			players = [(player.identity, player.nickname) for player in Player.all().run()]
			tvals = {
				'player_choices': players,
				'initial_options': range(12), # start with game to 11
				'players_by_league': players_by_league_l
			}
			self.yield_page("index", tvals)

class StoreGame(Page):

	def post(self):
		user=users.get_current_user()
		if user is None:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			# store game
			data=self.request.POST
			first_player=Player.get_player_with_id(data['first_player'])
			second_player=Player.get_player_with_id(data['second_player'])
			first_score=int(data['first_score'])
			second_score=int(data['second_score'])
			game = Game(first_player=first_player, first_score=first_score,
						second_player=second_player, second_score=second_score)
			game.first_player_wins = (first_score > second_score)
			game.reporter = Player.get_player(user)
			game.put()

			# update ratings
			wp_1 = game.first_player_wins
			wp_r, lp_r = (first_player.rating, second_player.rating) if wp_1 \
							else (second_player.rating, first_player.rating)
			new_wp, new_lp = elo.update_ratings(wp_r, lp_r)
			first_player.rating = new_wp if wp_1 else new_lp
			second_player.rating = new_lp if wp_1 else new_wp
			first_player.put()
			second_player.put()

			self.redirect('/')

class Profile(Page):

	def post(self, user_id):
		data = self.request.POST
		user = users.get_current_user()

		if user_id != user.user_id():
			return self.get(user_id)

		player = Player.get_player_with_id(user_id)
		player.email = data['email']
		player.nickname = data['name']
		player.save()

		return self.render_profile(player)

	def get(self, user_id):
		player = Player.get_player_with_id(user_id)

		self.render_profile(player)

	def render_profile(self, player):
		tvals = {
			'profile': player,
			}
		self.yield_page("profile", tvals)

class ProfileMe(Page):

	def get(self):
		user = users.get_current_user()
		self.redirect('/profile/' + user.user_id())

class Rankings(Page):

	def get(self):
		players_by_league = Player.get_players_by_league()
		players_by_league_l = []
		for league, players in players_by_league.iteritems():
			players_by_league_l.append(dict(league=league, players=players))

		players_by_league_l.reverse()
		tvals = {
			'players_by_league': players_by_league_l
		}
		self.yield_page("rankings", tvals)

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/profile/(\d+)', Profile),
	('/storegame', StoreGame),
	('/profile/?', ProfileMe),
	('/rankings', Rankings),
], debug=True)
