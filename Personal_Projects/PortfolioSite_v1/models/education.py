from google.appengine.ext import ndb

from models.user import User

class Education(ndb.Model):
    """ DataStore Model for Education """
    user = ndb.StructuredProperty(User)
    university = ndb.StringProperty(required = True)
    gpa = ndb.StringProperty(default = '[N/A]')
    degree = ndb.StringProperty(default = '[N/A]')
    year_start = ndb.StringProperty(default = '[N/A]')
    year_graduate = ndb.StringProperty(default = '[N/A]')
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)
