from google.appengine.ext import ndb

from models.user import User
from models.status import Status

class Like(ndb.Model):
    """ Likes for Posts """
    user = ndb.StructuredProperty(User)
    status = ndb.StructuredProperty(Status)
    created = ndb.DateTimeProperty(auto_now_add = True)
