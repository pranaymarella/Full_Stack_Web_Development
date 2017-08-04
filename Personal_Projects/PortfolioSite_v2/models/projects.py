from google.appengine.ext import ndb

from models.user import User

class Projects(ndb.Model):
    """ DataStore Model for Projects """
    user = ndb.StructuredProperty(User)
    category_name = ndb.StringProperty()
    title = ndb.StringProperty(required = True)
    link = ndb.StringProperty()
    description = ndb.TextProperty()
    programming_language = ndb.StringProperty()
    feature = ndb.BooleanProperty(default = False)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)
