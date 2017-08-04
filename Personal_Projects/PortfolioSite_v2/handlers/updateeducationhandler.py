from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.user import User
from models.education import Education

class UpdateEducationHandler(Handler):
    """ Queries the DataStore for users education """
    def post(self):
        if not self.user:
            self.redirect('/login')
        u = self.request.get('university')
        d = self.request.get('degree')
        g = self.request.get('gpa')
        y_s = self.request.get('year_start')
        y_g = self.request.get('year_graduate')

        if (u):
            e = Education(parent = education_key(),
                          user = self.user,
                          university = u)
            if (d):
                e.degree = d
            if (g):
                e.gpa = g
            if (y_s):
                e.year_start = y_s
            if (y_g):
                e.year_graduate = y_g
            e.put()
            self.redirect('/about_me')
        else:
            self.render('errorpage.html', error = "No University Provided")
