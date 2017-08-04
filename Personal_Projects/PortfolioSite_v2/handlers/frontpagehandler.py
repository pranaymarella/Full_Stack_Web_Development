from google.appengine.ext import ndb
from handlers.handler import Handler

from models.user import User

class FrontPageHandler(Handler):
    """ Makes Sure User is Logged in Otherwise Directed to Base Page """
    def get(self):
        if self.user:
            self.redirect('/main')
        else:
            self.render('login.html')
