from google.appengine.ext import ndb

from models.user import User
from models.status import Status

class Comments(ndb.Model):
    """ Comments Entity """
    comment = ndb.TextProperty(required=True)
    user = ndb.StructuredProperty(User)
    status = ndb.StructuredProperty(Status)
    created = ndb.DateTimeProperty(auto_now_add = True)
