from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.education import Education
from models.user import User

class DeleteEducation(Handler):
    """ Handler used to delete Education """
    def post(self, education_id):
        if not self.user:
            self.redirect('/login')
        key = ndb.Key('Education', int(education_id), parent=education_key())
        e = key.get()

        if (e and e.user.name == self.user.name):
            e.key.delete()
            time.sleep(0.1)
            self.redirect('/about_me')
        else:
            self.redirect('/login')
