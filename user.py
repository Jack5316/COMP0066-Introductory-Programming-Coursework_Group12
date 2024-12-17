import re
import pickle

class User:
    user_dictionary = {}
    all_user_objects = {}
    user_session = None

    @staticmethod
    def save_users(file_name="users.pkl"):
        try:
            with open(file_name, "wb") as file:
                pickle.dump((User.user_dictionary, User.all_user_objects), file)
        except Exception as e:
            print(f"Error saving user data: {e}")

    @staticmethod
    def load_users(file_name="users.pkl"):
        try:
            with open(file_name, "rb") as file:
                User.user_dictionary, User.all_user_objects = pickle.load(file)
        except FileNotFoundError:
            print(f"No user data file found ({file_name}). Starting fresh.")
        except Exception as e:
            print(f"Error loading user data: {e}")

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

        User.all_user_objects[username_clean] = self

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

    def update_first_name(self):
        while True:
            new_first_name = input("Please enter your new first name (or type 0 to exit): ").strip()
            if new_first_name == '0':
                print("Exiting without updating details.")
                break
            else:
                self.first_name = str(new_first_name)
                print("Your first name has been successfully updated.")
                break

    def update_last_name(self):
        while True:
            new_last_name = input("Please enter your new last name (or type 0 to exit): ").strip()
            if new_last_name == '0':
                print("Exiting without updating details.")
                break
            else:
                self.last_name = str(new_last_name)
                print("Your last name has been successfully updated.")
                break

    

# practitioner = User("John", "Smith", "him@gmail.com", user_type="mhwp", username=" Bland ", password="881")

# print(practitioner.username)

# User.login("  bLand", "881")





