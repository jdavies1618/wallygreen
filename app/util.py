import urllib
import hashlib

from google.appengine.api import app_identity
server_url = app_identity.get_default_version_hostname()

DEFAULT_SIZE = 20
DEFAULT_URL = 'http://media.tumblr.com/tumblr_mdpfupn4Pz1qhi1mx.jpg'


# This should be a template tag.
def get_gravatar_url(email, size=DEFAULT_SIZE, default_url=DEFAULT_URL):
	# construct the url
	gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
	gravatar_url += urllib.urlencode({'d':default_url, 's':str(size)})
	return gravatar_url
