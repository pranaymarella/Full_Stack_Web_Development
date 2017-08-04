from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.projects import Projects
from models.categories import Categories
from models.user import User

class EditProjectHandler(Handler):
    """ Handler Used to Edit Projects """
    def get(self, project_id):
        if not self.user:
            self.redirect('/login')
        key = ndb.Key('Projects', int(project_id), parent=post_key())
        project = key.get()
        categories = Categories.query(Categories.user == self.user).fetch()

        if (project and project.user.name == self.user.name):
            self.render('editproject.html',
                         project = project,
                         categories = categories)
        else:
            self.redirect('/login')

    def post(self, project_id):
        if not self.user:
            self.redirect('/login')
        key = ndb.Key('Projects', int(project_id), parent=post_key())
        p = key.get()
        title = self.request.get("title")
        link = self.request.get("link")
        description = self.request.get("description")
        programming_language = self.request.get("programming_language")
        category = self.request.get("name_category")
        add_category = self.request.get("add_category")
        feature = self.request.get("p_feature")
        error = "NEEDS A TITLE!"

        if (p and p.user.name == self.user.name):
            if (title):
                p.title = title
                if (link):
                    p.link = link
                else:
                    p.link = '[None]'
                if (description):
                    p.description = description
                else:
                    p.description = '[None]'
                if (programming_language):
                    p.programming_language = programming_language
                if (category):
                    p.category_name = category
                if (add_category):
                    c = Categories(name = add_category, user = self.user)
                    c.put()
                if (feature and feature == "true"):
                    p.feature = True
                else:
                    p.feature = False
                p.put()
                self.redirect('/main')
            else:
                self.render('editproject.html', project = p, error = error)
        else:
            self.redirect('/login')
