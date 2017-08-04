from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.categories import Categories
from models.user import User

class DeleteCategory(Handler):
    """ Handler Used to Delete Categories """
    def post(self, category_id):
        if not self.user:
            self.redirect('/login')
        key = ndb.Key('Categories', int(category_id), parent=categories_key())
        category = key.get()

        if (category and category.user.name == self.user.name):
            category.key.delete()
            time.sleep(0.1)
            self.redirect('/main')
        else:
            self.redirect('/login')
