from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.education import Education
from models.skills import Skills
from models.user import User

class VisitProfileHandler(Handler):
    """ Used to Visit Other User's Profiles """
    def get(self, user_name):
        user_other = User.by_name(user_name)
        if user_other:
            other_education = Education.query(Education.user.name == user_name).fetch()
            self.render('aboutme.html',
                         education = other_education,
                         user_other = user_other)
        else:
            self.render('errorpage.html', error = "Sorry, that user could not be found.")
