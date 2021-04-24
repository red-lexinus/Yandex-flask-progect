class UserLogin:
    def create_log(self, user_info):
        self.user_info = user_info

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_info[0])
