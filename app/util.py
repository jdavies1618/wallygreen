import urllib
import hashlib

DEFAULT_SIZE = 20
DEFAULT_URL = 'http://t3.gstatic.com/images?q=tbn:ANd9GcRos9zoopqiNEf586EHxFxoP1YK4-oTxTDWAJ1qsWdzEP5P_2l0TQ'

# This should be a template tag.
def get_gravatar_url(email, size=DEFAULT_SIZE, default_url=DEFAULT_URL):
	# construct the url
	gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
	gravatar_url += urllib.urlencode({'d':default_url, 's':str(size)})
	return gravatar_url
