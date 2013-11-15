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

class EloRating(db.Model):
	player = db.UserProperty(required=True)
	rating = db.FloatProperty(required=True)
