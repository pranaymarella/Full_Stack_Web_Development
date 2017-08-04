import os
import re
import random
import hashlib
import hmac
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

# GLOBAL VARIABLES AND FUNCTIONS #######################

secret = '290438u5skldgn350igmwop23$!@$@~$#$%!@#%#@'

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_username(username):
    """Makes sure username contains only alphabets and numbers"""
    return username and USER_RE.match(username)


def valid_password(password):
    """Makes sure password is between 3-20 characters long"""
    return password and PASS_RE.match(password)


def valid_email(email):
    """Makes sure email is an actual email address"""
    return not email or EMAIL_RE.match(email)


def render_str(template, **params):
    """Renders template with parameters"""
    t = jinja_env.get_template(template)
    return t.render(params)


def make_secure_val(val):
    """Uses Hmac to encrypt the value being passed in"""
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())


def check_secure_val(secure_val):
    """Checks to see if value is the original value"""
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


def make_salt(length=5):
    """creates random characters"""
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    """Encrypts the password using salt"""
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    """Makes sure the password is not tampered with"""
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


def users_key(group='default'):
    return db.Key.from_path('users', group)


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


def comment_key(name='default'):
    return db.Key.from_path('comments', name)

# MAIN HANDLER ##################################


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))


class DirectHandler(Handler):
    def get(self):
        self.redirect('/blog/?')

# GOOGLE DATASTORE ENTITIES ############################


class User(db.Model):
    """User Entity"""
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


class Post(db.Model):
    """Post Entity"""
    user = db.ReferenceProperty(User)
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    likes = db.IntegerProperty(default=0)
    comments = db.IntegerProperty(default=0)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self)


class Like(db.Model):
    """Like Entity"""
    user = db.ReferenceProperty(User)
    post = db.ReferenceProperty(Post)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)


class Comments(db.Model):
    """Comments Entity"""
    comment = db.TextProperty(required=True)
    user = db.ReferenceProperty(User)
    post = db.ReferenceProperty(Post)
    created = db.DateTimeProperty(auto_now_add=True)

# SIGNUP AND LOGIN/LOGOUT HANDLERS #########################


class Signup(Handler):
    """Handles the Signup Page"""
    def get(self):
        self.render("signup.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(Signup):
    """Registers the user"""
    def done(self):
        # make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/blog')


class Login(Handler):
    """Logs in the user, checks to make sure username
    and password match database"""
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login.html', error=msg)


class Logout(Handler):
    """Logs out user"""
    def get(self):
        self.logout()
        self.redirect('/blog')

# BLOG #########################################


class BlogFront(Handler):
    """Shows the main page of the blog"""
    def get(self):
        posts = db.GqlQuery(
            "SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        self.render('front.html', posts=posts)

# POSTING AND EDITING BLOGS #############################


class NewPost(Handler):
    """Allows user to post new blogs"""
    def get(self):
        # Allows posting if user is logged in, otherwise redirects to login
        if self.user:
            self.render('newpost.html')
        else:
            self.redirect('/login')

    def post(self):
        # Request for the subject, content and user_id
        subject = self.request.get('subject')
        content = self.request.get('content')
        user_id = User.by_name(self.user.name)

        # if both subject AND content, proceed with adding
        # information to database
        if self.user:
            if (subject and content):
                p = Post(parent=blog_key(),
                         subject=subject,
                         content=content,
                         user=user_id)
                p.put()

                self.redirect('/blog/%s' % str(p.key().id()))
            # We need more information from the user
            else:
                error = "Subject and content, please!"
                self.render('newpost.html',
                            subject=subject,
                            content=content,
                            error=error)
        else:
            self.render('errorpage.html',
                        error="You aren't allowed to make posts here!")


class PostPage(Handler):
    """Directs user to indivudal blog pages"""
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        comments = Comments.all().filter('post =', post).order('-created')

        # If post does not exist, then ERROR
        if not post:
            self.error(404)
            return
        if comments:
            if self.user:
                self.render("permalink.html",
                            post=post,
                            comments=comments,
                            user_name=self.user.name)
            else:
                self.redirect('/login')


class EditPost(Handler):
    """Allows user to Edit previously created Blog posts"""
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if self.user:
            if post.user.key().id() == self.user.key().id():
                self.render("editpost.html", post=post)
            else:
                self.render('errorpage.html',
                            error="You cannot edit other user's posts")
        else:
            self.redirect('/login')

    def post(self, post_id):
        key = db.Key.from_path("Post", int(post_id), parent=blog_key())
        post = db.get(key)

        if (self.user):
            if post.user.key().id() == self.user.key().id():
                post.subject = self.request.get('subject')
                post.content = self.request.get('content')
                post.put()
                self.redirect('/blog/%s' % str(post.key().id()))
            else:
                self.response.out.write('it did not work')
        else:
            self.render('errorpage.html',
                        error="You cannot edit other user's posts")


class DeletePost(Handler):
    """Allows user to delete posts"""
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if self.user:
            if post.user.key().id() == self.user.key().id():
                self.render("deletepost.html", post=post)
            else:
                self.render('errorpage.html',
                            error="You may not delete other users posts")
        else:
            self.redirect('/login')

    def post(self, post_id):
        key = db.Key.from_path("Post", int(post_id), parent=blog_key())
        post = db.get(key)

        if (self.user):
            if post.user.key().id() == self.user.key().id():
                db.delete(key)
                self.redirect('/blog')
            else:
                self.render('errorpage.html',
                            error="You may not delete other users posts")
        else:
            self.redirect('/login')

# LIKES AND COMMENTS ############################


class LikeHandler(Handler):
    """Allows user to like other users' posts"""
    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if self.user:
            if (self.user.name == post.user.name):
                self.render('errorpage.html',
                            error="You cannot like your own post")
            else:
                like = Like.all()
                like = like.filter('user =', self.user)
                like = like.filter('post =', post).get()

                if like:
                    self.redirect('/blog/' + str(post.key().id()))
                else:
                    l = Like(parent=key,
                             user=self.user,
                             post=post)
                    post.likes = post.likes + 1

                    l.put()
                    post.put()
                    self.redirect('/blog/'+str(post.key().id()))
        else:
            self.redirect('/login')


class CommentHandler(Handler):
    """Allows users to comment on blog posts"""
    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not self.user:
            self.redirect('/login')
        else:
            comment = self.request.get('comment')
            if comment:
                c = Comments(parent=comment_key(),
                             user=self.user,
                             post=post,
                             comment=comment)
                post.comments = post.comments + 1
                c.put()
                post.put()
            self.redirect('/blog/' + str(post_id))


class DeleteComment(Handler):
    """Allows users to delete their comments"""
    def get(self, c_id):
        key = db.Key.from_path('Comments', int(c_id), parent=comment_key())
        comment = db.get(key)

        if self.user:
            if (comment.user.key().id() == self.user.key().id()):
                self.render("deletecomment.html", comment=comment)
            else:
                self.render('errorpage.html',
                            error="You may not delete other users comments")
        else:
            self.redirect('/login')

    def post(self, c_id):
        key = db.Key.from_path("Comments", int(c_id), parent=comment_key())
        comment = db.get(key)

        if (self.user):
            if (comment.user.key().id() == self.user.key().id()):
                comment.post.comments = comment.post.comments - 1
                comment.post.put()
                db.delete(key)
                self.redirect('/blog/' + str(comment.post.key().id()))
            else:
                self.render('errorpage.html',
                            error="You may not delete other users comments")
        else:
            self.redirect('/login')


class EditComment(Handler):
    """Allows Users to edit their comments"""
    def get(self, c_id):
        key = db.Key.from_path('Comments', int(c_id), parent=comment_key())
        comment = db.get(key)

        if self.user:
            if comment.user.key().id() == self.user.key().id():
                self.render("editcomment.html", comment=comment)
            else:
                self.render('errorpage.html',
                            error="You cannot edit other user's comments")
        else:
            self.redirect('/login')

    def post(self, c_id):
        key = db.Key.from_path("Comments", int(c_id), parent=comment_key())
        comment = db.get(key)

        if (self.user):
            if comment.user.key().id() == self.user.key().id():
                comment.comment = self.request.get('comment')
                comment.put()
                self.redirect('/blog/%s' % str(comment.post.key().id()))
            else:
                self.render('errorpage.html',
                            error="You cannot edit other user's comments")
        else:
            self.render('errorpage.html',
                        error="You cannot edit other user's posts")

# END OF HANDLERS ###############################

app = webapp2.WSGIApplication([('/', DirectHandler),
                               ('/blog/?', BlogFront),
                               ('/blog/newpost', NewPost),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/EditPost/([0-9]+)', EditPost),
                               ('/blog/DeletePost/([0-9]+)', DeletePost),
                               ('/like/([0-9]+)', LikeHandler),
                               ('/comment/([0-9]+)', CommentHandler),
                               ('/blog/editcomment/([0-9]+)', EditComment),
                               ('/blog/deletecomment/([0-9]+)', DeleteComment),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout)
                               ],
                              debug=True)
