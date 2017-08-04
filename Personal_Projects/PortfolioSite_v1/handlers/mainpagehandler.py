from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.projects import Projects
from models.categories import Categories
from models.skills import Skills
from models.user import User

class MainPageHandler(Handler):
    """ Directs to the Welcome Page, Queries for Projects and Categories from
    Google Datastore """
    def get(self):
        if self.user:
            projects = Projects.query(Projects.user == self.user).fetch(limit=5)
            categories = Categories.query(Categories.user == self.user).fetch()
            skills = Skills.query(Skills.user == self.user).fetch()

            self.render('welcome.html',
                        projects = projects,
                        categories = categories,
                        skills = skills)
        else:
            self.redirect('/login')
