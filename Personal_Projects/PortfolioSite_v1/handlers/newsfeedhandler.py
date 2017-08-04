from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.user import User
from models.status import Status

class NewsFeedHandler(Handler):
    def get(self):
        status = Status.query().order(-Status.created)
        s = status.fetch()
        self.render('newsfeed.html', status = s)
