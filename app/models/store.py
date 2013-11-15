from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.db import djangoforms

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

class PlayerForm(djangoforms.ModelForm):
	class Meta:
		model = Player
