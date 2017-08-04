from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.projects import Projects
from models.categories import Categories
from models.skills import Skills
from models.user import User

class VisitMainHandler(Handler):
    """ Used to Visit Main Page of Other User """
    def get(self, user_name):
        user_other = User.by_name(user_name)
        if user_other:
            other_projects = Projects.query(Projects.user.name == user_name).fetch()
            other_categories = Categories.query(Categories.user.name == user_name).fetch()
            recent_projects = Projects.query(Projects.user.name == user_name).fetch(limit=6)
            other_skills = Skills.query(Skills.user.name == user_name).fetch()
            self.render('visitmain.html',
                         recent_projects = recent_projects,
                         other_projects = other_projects,
                         other_categories = other_categories,
                         user_other = user_other,
                         other_skills = other_skills)
        else:
            self.render('errorpage.html', error = "Sorry, that user could not be found.")
