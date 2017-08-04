from handlers.handler import Handler
from helpers import *

from models.user import User

class Login(Handler):
    """ Logs In User """
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        user = User.login(username, password)
        if user:
            usercookie = make_secure_val(str(username))
            self.response.headers.add_header("Set-Cookie",
                                             "u=%s; Path=/" % usercookie)
            self.login(user)
            self.redirect('/main')
        else:
            message = 'Invalid login'
            self.render('login.html', error = message)
