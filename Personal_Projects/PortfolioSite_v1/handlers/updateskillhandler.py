from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.skills import Skills
from models.user import User

class UpdateSkillHandler(Handler):
    """ Handler Used to Add Skills """
    def post(self):
        if self.user:
            name = self.request.get('skill_name')
            if name:
                s = Skills(parent = skills_key(),
                           name = name,
                           user = self.user)
                s.put()
                self.redirect('/main')
            else:
                self.render('errorpage.html', error = "No Skill Given")
        else:
            self.redirect('/login')
