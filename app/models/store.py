from collections import OrderedDict
import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from app import elo


BRONZE = "Bronze"
SILVER = "Silver"
GOLD = "Gold"

LEAGUES = [BRONZE, SILVER, GOLD]
LEAGUE_ELOS = [(0, BRONZE),
			   (2000, SILVER),
			   (2400, GOLD)]

class Player(db.Model):
	identity = db.StringProperty(required=True)
	rating = db.FloatProperty(required=True)
	nickname = db.StringProperty(required=True)
	email = db.StringProperty(required=True)

	def _get_games(self):
		games = [g for g in self.p1_games.run()]
		games.extend([g for g in self.p2_games.run()])
		return games
	games = property(_get_games)

	def _get_played(self):
		return self.p1_games.count() + self.p2_games.count()
	played = property(_get_played)

	def _get_won(self):
		wins_as_p1 = self.p1_games.filter("first_player_wins", True).count()
		wins_as_p2 = self.p2_games.filter("first_player_wins", False).count()
		return wins_as_p1 + wins_as_p2
	won = property(_get_won)

	def _get_lost(self):
		return self.played - self.won
	lost = property(_get_lost)

	def _get_league(self):
		player_elo = self.rating
		player_league = BRONZE
		for min_elo, league in LEAGUE_ELOS:
			if player_elo < min_elo:
				return player_league
			else:
				player_league = league
		return player_league
	league = property(_get_league)

	@classmethod
	def get_player(cls, user):
		player = cls.get_player_with_id(user.user_id())
		if not player:
			player = cls.create_player(user)
		return player

	@classmethod
	def get_player_with_id(cls, user_id):
		q = db.Query(cls)
		q.filter('identity', user_id)
		return q.get()

	@classmethod
	def create_player(cls, user):
		logging.info('Creating player %s' % user.nickname())
		league = BRONZE
		player = cls(identity = user.user_id(),
						rating = elo.DEFAULT_RATING,
						league=league,
						nickname = user.nickname(),
						email = user.email())
		player.save()
		return player

	@classmethod
	def get_players_in_league(cls, league):
		q = Player.all()
		q.filter('league = ', league)
		q.order('-rating')

		players = []
		for player in q.run():
			players.append(player)
		return players

	@classmethod
	def get_players_by_league(cls):
		leagues = OrderedDict()
		for league in LEAGUES:
			leagues[league] = []

		q = Player.all()
		q.order('-rating')
		for player in q.run():
			leagues[player.league].append(player)

		return leagues


	def __unicode__(self):
		return self.identity.nickname()

class Game(db.Model):
	first_player = db.ReferenceProperty(Player, required=True, collection_name="p1_games")
	first_score = db.IntegerProperty(required=True)
	second_player = db.ReferenceProperty(Player, required=True, collection_name="p2_games")
	second_score = db.IntegerProperty(required=True)
	first_player_wins = db.BooleanProperty()
	reporter = db.ReferenceProperty(Player, collection_name="reported_games")
	stored_time = db.DateTimeProperty(auto_now_add=True)

	def _get_winner(self):
		if (self.first_score > self.second_score):
			return self.first_player
		else :
			return self.second_player
	winner = property(_get_winner)
