from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.status import Status
from models.user import User

class UpdateStatus(Handler):
    """ Allows users to post status """
    def post(self):
        if self.user:
            status = self.request.get('status')
            if status:
                s = Status(parent = status_key(),
                           user = self.user,
                           content = status)
                s.put()
                self.redirect("/newsfeed")
            else:
                self.render("errorpage.html", error = "Status cannot be empty!")
        else:
            self.redirect("/login")
