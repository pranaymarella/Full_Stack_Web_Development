from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.projects import Projects
from models.categories import Categories
from models.user import User

class UpdateProjectHandler(Handler):
    """ Handler Used to Update Projects """
    def post(self):
        title = self.request.get("title")
        link = self.request.get("link")
        description = self.request.get("description")
        programming_language = self.request.get("programming_language")
        category = self.request.get("name_category")
        add_category = self.request.get("add_category")
        feature = self.request.get("p_feature")
        error = "Need Title, Link, and Description!"

        if self.user:
            if (title):
                p = Projects(parent = post_key(),
                             title=title,
                             link = '[None]',
                             description = '[None]',
                             user = self.user)
                if (link):
                    p.link = link
                if (description):
                    p.description = description
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
                self.redirect('/main')
        else:
            self.redirect('/login')
