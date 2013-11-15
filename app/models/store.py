import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.db import djangoforms

from app import elo

BRONZE = "Bronze"
SILVER = "Silver"
GOLD = "Gold"
class Player(db.Model):
	identity = db.UserProperty(required=True)
	rating = db.FloatProperty(required=True)
	league = db.StringProperty(choices=set([BRONZE, SILVER, GOLD]))

	def _get_played(self):
		return 1
	played = property(_get_played)

	@classmethod
	def get_player(cls, user):
		q = db.Query(cls)
		q.filter('identity', users.get_current_user())

		player = q.get()
		if not player:
			player = cls.create_player(user)
		return player

	@classmethod
	def create_player(cls, user):
		logging.info('Creating player %s' % user.nickname())
		league = BRONZE
		player = cls(identity = user,
						rating = elo.DEFAULT_RATING,
						league=league)
		player.save()
		return player

class Game(db.Model):
	first_player = db.ReferenceProperty(Player, required=True, collection_name="p1_games")
	first_score = db.IntegerProperty(required=True)
	second_player = db.ReferenceProperty(Player, required=True, collection_name="p2_games")
	second_score = db.IntegerProperty(required=True)
	first_player_wins = db.BooleanProperty(required=True)
	max_score = db.IntegerProperty(required=True, choices=set([11, 21]))
	reporter = db.UserProperty(required=True)
	stored_time = db.DateTimeProperty(auto_now_add=True)
	validated = db.BooleanProperty()

class PlayerForm(djangoforms.ModelForm):
	class Meta:
		model = Player
