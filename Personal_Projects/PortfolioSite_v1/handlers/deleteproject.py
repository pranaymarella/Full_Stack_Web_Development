from google.appengine.ext import ndb
from handlers.handler import Handler
from helpers import *

from models.projects import Projects
from models.user import User

class DeleteProject(Handler):
    """ Handler used to Delete Projects """
    def post(self, project_id):
        if not self.user:
            self.redirect('/login')
        key = ndb.Key('Projects', int(project_id), parent=post_key())
        project = key.get()

        if (project and project.user.name == self.user.name):
            project.key.delete()
            time.sleep(0.1)
            self.redirect('/main')
        else:
            self.redirect('/login')
