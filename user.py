import re

class User:
    user_dictionary = {}

    user_session = None

    def __init__(self, first_name, last_name, email, user_type, username, password):
        username_clean = str(username).strip().lower()
        self.type_validate(user_type)
        self.email_validate(email)
        self.username_validate(username_clean)

        User.user_dictionary[username_clean] = str(password)

        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.email = str(email)
        self.blocked = False
        self.user_type = str(user_type)
        self.username = username_clean
        self.password = str(password)

    @classmethod
    def display_users(cls):
        return cls.user_dictionary

    @staticmethod
    def type_validate(user_type):
        allowed_types = {"admin", "patient", "mhwp"}
        if user_type not in allowed_types:
            raise ValueError("Incorrect user type!")

    @staticmethod
    def username_validate(username):
        if str(username) in User.user_dictionary:
            raise ValueError(f"Username({username}) taken!")

    @staticmethod
    def email_validate(email):
        regex_email = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(regex_email, str(email)):
            raise ValueError("Email invalid!")

    @classmethod
    def login(cls, username, password):
        login_clean = str(username).strip().lower()
        if login_clean in cls.user_dictionary and cls.user_dictionary[login_clean] == password:
            cls.user_session = login_clean
            print(f"Login successful: welcome {login_clean}.")
        else:
            print("Invalid login details!")

    @classmethod
    def logout(cls):
        if cls.user_session:
            print(f"Logout successful: goodbye {cls.user_session}.")
            cls.user_session = None
        else:
            print("User not logged in!")

    def update_email(self, new_email):
        User.email_validate(new_email)
        self.email = str(new_email)


    def update_password(self, new_password):
        self.password = new_password
        User.user_dictionary[self.username] = str(new_password)

# practitioner = User("John", "Smith", "him@gmail.com", user_type="mhwp", username=" Bland ", password="881")

# print(practitioner.username)

# User.login("  bLand", "881")





