from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.projects import Projects
from models.categories import Categories
from models.user import User

class VisitProjectsHandler(Handler):
    """ Used to Visit Projects Page of Other User """
    def get(self, user_name):
            user_other = User.by_name(user_name)
            projects = Projects.query(Projects.user == user_other).fetch()
            categories = Categories.query(Categories.user == user_other).fetch()
            self.render('visitprojects.html',
                         projects = projects,
                         categories = categories,
                         user_other = user_other)
