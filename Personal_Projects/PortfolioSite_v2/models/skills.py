from google.appengine.ext import ndb

from models.user import User

class Skills(ndb.Model):
    """ Stores skills of User """
    user = ndb.StructuredProperty(User)
    name = ndb.StringProperty(required = True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)

    @classmethod
    def by_name(cls, name):
        u = Skills.query().filter(ndb.GenericProperty('name')==name).get()
        return u
