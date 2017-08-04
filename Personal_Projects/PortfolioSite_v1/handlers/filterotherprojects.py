from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.projects import Projects
from models.categories import Categories
from models.user import User

class FilterOtherProjects(Handler):
    """ Used to Filter the Projects in the Projects page """
    def post(self, user_name):
        user_other = User.by_name(user_name)
        if user_other:
            name_category = self.request.get("name_c")

            if (name_category == 'all'):
                self.redirect('/visit/projects/%s' % (user_other.name))
            else:
                if (name_category):
                    category = Categories.by_name(name_category)
                projects = Projects.query(Projects.category_name == name_category).fetch()
                categories = Categories.query(Categories.user == user_other).fetch()
                self.render('visitprojects.html',
                            category_filter = category,
                            user_other = user_other,
                            projects = projects,
                            categories = categories)
        else:
            self.render('errorpage.html', error = "Sorry, that information could not be found.")
