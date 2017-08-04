from google.appengine.ext import ndb
from helpers import *

class User(ndb.Model):
    """ DataStore Model for Users """
    name = ndb.StringProperty(required = True)
    pw_hash = ndb.StringProperty(required = True)
    email = ndb.StringProperty()
    display = ndb.StringProperty()
    occupation = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add = True)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = User.query().filter(ndb.GenericProperty('name')==name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None, display = None, occupation = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email,
                    display = display,
                    occupation = occupation)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u
