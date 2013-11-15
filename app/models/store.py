import logging

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.db import djangoforms

from app import elo


class League(db.Model):
	name = db.StringProperty(choices=set(["Bronze", "Silver", "Gold"]))

class Game(db.Model):
	first_player = db.UserProperty(required=True)
	first_score = db.IntegerProperty(required=True)
	second_player = db.UserProperty(required=True)
	second_score = db.IntegerProperty(required=True)
	max_score = db.IntegerProperty(required=True, choices=set([11, 21]))
	reporter = db.UserProperty(required=True)
	stored_time = db.DateTimeProperty(auto_now_add=True)
	validated = db.BooleanProperty()

class League(db.Model):
	name = db.StringProperty(choices=set(["Bronze", "Silver", "Gold"]))

class Player(db.Model):
	identity = db.UserProperty(required=True)
	rating = db.FloatProperty(required=True)
	league = db.ReferenceProperty(League, collection_name="members")
	
	def _get_played(self):
		return 1
	played = property(_get_played)
	
		
	@classmethod
	def get_player(cls, user):
		q = db.Query(cls)
		q.filter('identity =', users.get_current_user())
		
		player = q.get()
		if not player:
			player = cls.create_player(user)
		return player
	
	@classmethod
	def create_player(cls, user):
		logging.info('Creating player %s' % user.nickname())
		league = db.Query(League).filter('name =', 'Bronze').get()
		player = cls(identity = user,
						rating = elo.DEFAULT_RATING,
						league=league)
		player.save()
		return player
		
		

class PlayerForm(djangoforms.ModelForm):
	class Meta:
		model = Player
