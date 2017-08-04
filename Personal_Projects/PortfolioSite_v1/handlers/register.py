from google.appengine.ext import ndb
from handlers.handler import Handler
from handlers.signup import Signup
from helpers import *

from models.user import User

class Register(Signup):
    """ Used to Register Users """
    def done(self):
        #make sure the user doesn't already exist
        user = User.by_name(self.username)
        if user:
            message = 'The user already exists.'
            self.render('signup.html', error_username = message)
        else:
            user = User.register(self.username,
                                 self.password,
                                 self.email,
                                 self.display,
                                 self.occupation)
            user.put()

            self.login(user)
            self.redirect('/main')
