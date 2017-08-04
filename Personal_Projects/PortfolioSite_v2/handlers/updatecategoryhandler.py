from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.categories import Categories
from models.user import User

class UpdateCategoryHandler(Handler):
    """ Handler Used to Add Categories """
    def post(self):
        if self.user:
            name = self.request.get('category_name')
            feature = self.request.get("c_feature")
            if name:
                c = Categories(parent = categories_key(),
                               name = name,
                               user = self.user)
                if (feature and feature == 'true'):
                    c.feature = True
                c.put()
                self.redirect('/main')
            else:
                self.render('errorpage.html', error = "No Category Given")
        else:
            self.redirect('/login')
