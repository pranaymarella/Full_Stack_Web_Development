from google.appengine.ext import ndb

from models.user import User

class Status(ndb.Model):
    """ Status Entity """
    user = ndb.StructuredProperty(User)
    content = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    likes = ndb.IntegerProperty(default = 0)
    comments = ndb.IntegerProperty(default = 0)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self)
