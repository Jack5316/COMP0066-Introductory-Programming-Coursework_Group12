

class User():

    def __init__(self,first_name,last_name,email,user_type,username,password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.blocked = False
        self.user_type = user_type
        self.username = username
        self.password = password

    # incorporate both login and logout functions 
    def login(self):
        pass
    def logout(self): 
        pass

    def update_email(self,new_email):
        self.email = new_email 

    def update_password(self,new_password):
        self.password = new_password

