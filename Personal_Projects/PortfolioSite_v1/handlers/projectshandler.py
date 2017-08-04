from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.projects import Projects
from models.categories import Categories
from models.skills import Skills
from models.user import User

class ProjectsHandler(Handler):
    """ Directs to the Projects Page of Main User, Retrieves Projects from
    the Google Datastore """
    def get(self):
        projects = Projects.query(Projects.user == self.user).fetch()
        categories = Categories.query(Categories.user == self.user).fetch()
        skills = Skills.query(Skills.user == self.user).fetch()
        self.render('projects.html',
                    projects = projects,
                    categories = categories,
                    skills = skills)
