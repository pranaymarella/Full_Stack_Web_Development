from handlers.handler import Handler

class Logout(Handler):
    """ Logs Out the User """
    def get(self):
        self.logout()
        self.redirect('/')
