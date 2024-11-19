from user import User


class Admin(User):
    



    def __init__(self, first_name, last_name, email, username, password):  #INITIALIZING ADMIN OBJECT
        super().__init__(first_name,last_name,email,"admin",username, password) #CALLING __INIT__ METHOD FROM PARENT USER CLASS
        self.allocations={} #dictionary to track patient-MHWP allocations





    def allocate_patient(self, patient_username, mhwp_username):

        if patient_username not in User.user_dictionary or mhwp_username not in User.user_dictionary:
            raise ValueError("Invalid username(s). Ensure both patient and MHWP exist.")   #CHECKING IF BOTH THE PATIENT AND MHWP EXIST
        
        self.allocations[patient_username]=mhwp_username  #UPDATING THE ALLOCATIONS DICTIONARY WITH THE MAPPING OF THE PATIENT TO THE PRACTITIONER





    


    
    def edit_user(self, user, new_details): #TAKES NEW_DETAILS AS A DICTIONARY OF UPDATED FIELDS
        #if username not in User.user_dictionary: #FIRST CHECKING IF USER EXISTS
            #raise ValueError("User not found") 
        
        for key, value in new_details.items(): #ITERATING THROUGH DICTIONARY OF NEW DETAILS
            if hasattr(self, key): #CHECKING IF ATTRIBUTE EXISTS IN THE OBJECT (SUCH AS FIRST NAME, LAST NAME ETC.))
                setattr(self,key,value) #UPDATES THE USER OBJECT DYNAMICALLY WITH NEW VALUES
            else:
                print("attribute not found")


        
        






  
    def delete_user(self, username):
        if username not in User.user_dictionary:  #FIRST CHECKING IF USER EXISTS
            raise ValueError("User not found.")
        del User.user_dictionary[username] #DELETES THE USERNAME FROM THE GLOBAL USER DICTIONARY
        self.allocations.pop(username,None)  #REMOVES THE USERNAME FROM THE ALLOCATIONS DICTIONARY

        

    def disable_user(self,user):
        if self.username not in User.user_dictionary:
            raise ValueError("User not found")
        
        
        user.blocked=True #USER BLOCKED ATTRIBUTE NOW = TRUE
        print(f"User {user.username} has been disabled")



    def user_summary(self): #will show all users usernames, password, and allocations.
        print("User summary:")
        for username, password in User.user_dictionary.items(): #LOOPING THROUGH USER DICTIONARY TO GET EVERY USERNAME AND CORRELATING PASSWORD
            print(f"Username:{username} , Password:{password}")
        
        print("\nAllocations:")
        for patient, mhwp in self.allocations.items(): #LOOPING THROUGH ALLOCATIONS DICTIONARY TO GET ALL PATIENT-MHWP MAPPINGS
            print(f"Patient: {patient}, MHWP: {mhwp}")



doruk=Admin("Doruk","Ustay","doruk@gmail.com","dorukustay","password123")

alex=User("Alex","Chris","alex@gmail.com","patient","alex1","password123")

print(alex.blocked)

doruk.disable_user(alex)

print(alex.blocked)

doruk.edit_user("alex1",{"first_name":"Jordan"})

print(alex.first_name)