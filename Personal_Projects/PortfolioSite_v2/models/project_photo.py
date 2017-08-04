from google.appengine.ext import ndb
from google.appengine.ext import blobstore

from models.user import User
from models.projects import Projects

class ProjectPhoto(ndb.Model):
    user = ndb.StructuredProperty(User)
    project = ndb.StructuredProperty(Projects)
    blob_key = ndb.BlobKeyProperty()
