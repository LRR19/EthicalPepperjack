import os

class Config(object):
	SECRET_KEY = os.environ.get('ETHICAL') or 'something-else'