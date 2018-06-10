class User:

    def __init__(self, user_id, username, authenticated, administrator):
        self.authenticated = authenticated
        self.user_id = user_id
        self.username = username
        self.administrator = administrator


    def is_authenticated(self):
        return self.authenticated


    def is_active(self):
        return True


    def is_anonymous(self):
        return False


    def is_admin(self):
        return self.administrator


    def get_id(self):
        return self.user_id
