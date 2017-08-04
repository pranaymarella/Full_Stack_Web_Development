from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.projects import Projects
from models.categories import Categories
from models.user import User

class FilterProjects(Handler):
    """ Used to Filter the Projects in the Projects page """
    def post(self):
        name_category = self.request.get("name_c")

        if (name_category == 'all'):
            self.redirect('/projects')
        else:
            if (name_category):
                category = Categories.by_name(name_category)
            projects = Projects.query(Projects.category_name == name_category).fetch()
            categories = Categories.query(Categories.user == self.user).fetch()
            self.render('projects.html',
                        category_filter = category,
                        projects = projects,
                        categories = categories)
