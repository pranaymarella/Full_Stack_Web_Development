from google.appengine.ext import ndb

from models.user import User

class Categories(ndb.Model):
    """ DataStore Model for Categories """
    user = ndb.StructuredProperty(User)
    name = ndb.StringProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    feature = ndb.BooleanProperty(default = False)

    @classmethod
    def by_name(cls, name):
        u = Categories.query().filter(ndb.GenericProperty('name')==name).get()
        return u
