from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.user import User

class SearchHandler(Handler):
    """ Used to Search for Other Users """
    def get(self):
        user_name = self.request.get('search_user')
        if (user_name):
            user = User.by_name(user_name)
            if user:
                self.redirect('/visit/%s' % user.name)
            else:
                error = "Sorry, that user could not be found."
                self.render('errorpage.html', error=error)
        else:
            self.redirect('/main')
