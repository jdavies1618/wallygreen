from google.appengine.ext import db

class Game(db.Model):
	first_player = db.UserProperty(required=True)
	first_score = db.IntegerProperty(required=True)
	second_player = db.UserProperty(required=True)
	second_score = db.IntegerProperty(required=True)
	max_score = db.IntegerProperty(required=True, choices=set([11, 21]))
	reporter = db.UserProperty(required=True)
	stored_time = db.DateTimeProperty(auto_now_add=True)
	validated = db.BooleanProperty()

class Player(db.Model):
	identity = db.UserProperty(required=True)
	rating = db.FloatProperty(required=True)
	league = db.ReferenceProperty(League, collection_name="members")

class League(db.Model):
	name = db.StringProperty(choices=set(["Bronze", "Silver", "Gold"]))
