import os
import re
import random
import hashlib
import hmac
import time

from string import letters
from google.appengine.ext import ndb

import jinja2

# Jinja Initializion

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

# Global Variables

secret = '2o4092j3tf!`~!5r023urj~!$##`'

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

# Global Functions

def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PASS_RE.match(password)

def valid_email(email):
    return not email or EMAIL_RE.match(email)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

# Authentication

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

# Model Keys

def education_key(name = 'default'):
    return ndb.Key('education', name)

def post_key(name = 'default'):
    return ndb.Key('projects', name)

def users_key(group = 'default'):
    return ndb.Key('users', group)

def categories_key(name = 'default'):
    return ndb.Key('categories', name)

def skills_key(name = 'default'):
    return ndb.Key('skills', name)

def status_key(name = 'default'):
    return ndb.Key('status', name)

def comment_key(name = 'default'):
    return ndb.Key('comments', name)
