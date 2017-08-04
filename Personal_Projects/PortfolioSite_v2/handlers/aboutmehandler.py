from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.education import User
from models.education import Education

class AboutMeHandler(Handler):
    """ Directs to the About Me Page of Main User """
    def get(self):
        education = Education.query(Education.user == self.user).fetch()
        self.render('aboutme.html', education = education)
