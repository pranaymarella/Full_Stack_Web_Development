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
            # skills
            skills = Skills.query(Skills.user == self.user).fetch()
            # recent projects
            recent = Projects.query(Projects.user == self.user).fetch(limit=5)
            # create dictionary to hold categories with their projects
            data = {}
            # holds the categories which are meant to be shown on homepage
            featured_categories = []
            categories = Categories.query(Categories.user == self.user).fetch()
            for i in categories:
                if (i.feature == True):
                    featured_categories.append(i)
                    data['{}'.format(i.name)] = Projects.query(Projects.category_name == i.name and Projects.feature == True and Projects.user == self.user).fetch()

            self.render('welcome.html',
                        recent = recent,
                        data = data,
                        categories = featured_categories,
                        skills = skills,
                        user = self.user)
        else:
            self.redirect('/login')
