from flask_login import UserMixin
from flaskr import login_manager
from .db_connect import execute_query


# User Model for Flash-Login
class User(UserMixin):
    # Constructor for User Model
    def __init__(self, id, username, f_name, l_name, email, password, active=True):
        self.username = username
        self.id = id
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.password = password
        self.active = active

    # Returns true because users are always active
    def is_active(self):
        return True

    # Returns false because users are always not anonymous
    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

    @login_manager.user_loader
    def load_user(id):
        user_id = int(id)
        query = """SELECT id, username, f_name, l_name, email, password FROM users WHERE id = %d;""" % user_id
        dbuser = list(execute_query(query))
        print(dbuser)
        if dbuser:
            user_obj = User(id=dbuser[0][0], username=dbuser[0][1], f_name=dbuser[0][2], l_name=dbuser[0][3],
            email=dbuser[0][4], password=dbuser[0][5])
            return user_obj
        else:
            return None
