from datetime import datetime

class Admin(User):
    # Maybe add admin levels? giving different kind of authhority
    def __init__(self, first_name, last_name, username, email):
        # Initialise Admin using the base User class
        super().__init__(first_name, last_name, username, email, user_type="Admin")
    
    # Method to allocate a patient to an MHWP
    def allocate_patient_to_mhwp(self, patient, mhwp):
        if isinstance(patient, Patient) and isinstance(mhwp, MHWP):
            patient.assigned_mhwp = mhwp.username
            mhwp.patients_list.append(patient)
            print(f"Patient {patient.username} has been assigned to MHWP {mhwp.username}")
        else:
            print("Invalid user types. Make sure both Patient and MHWP are properly provided.")

    # Method to edit user information (for both MHWP and patient)
    def edit_user_info(self, user, **kwargs):
        if isinstance(user, (Patient, MHWP)):
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                    print(f"{key} has been updated to {value} for user {user.username}")
                else:
                    print(f"Attribute {key} not found for user {user.username}")
        else:
            print("Invalid user type. Please provide either a Patient or MHWP.")

    # Method to delete a user (either a Patient or MHWP)
    def delete_user(self, user):
        if isinstance(user, User):
            if user.username != self.username:  # Prevent deleting yourself
                User.users.pop(user.username, None)
                print(f"User {user.username} has been deleted.")
            else:
                print("Admin cannot delete themselves.")
        else:
            print("Invalid user type. Must be an instance of User.")

    # Method to disable a user (either a Patient or MHWP)
    def disable_user(self, user):
        if isinstance(user, User):
            user.blocked = True
            print(f"User {user.username} has been disabled.")
        else:
            print("Invalid user type. Must be an instance of User.")
    
    # Method to display a summary of all users, their allocations, and bookings
    def display_summary(self):
        print("\nSummary Report")
        print("--------------")
        print(f"{'Username':<15} {'User Type':<10} {'Assigned MHWP':<15} {'Confirmed Bookings':<10}")
        for username, user in User.users.items():
            if isinstance(user, Patient):
                print(f"{user.username:<15} {'Patient':<10} {user.assigned_mhwp:<15} {len(user.appointments):<10}")
            elif isinstance(user, MHWP):
                print(f"{user.username:<15} {'MHWP':<10} {'N/A':<15} {len(user.appointments):<10}")
        print("--------------")

# # Example Usage
# # Assuming we have already initialized some users
# admin = Admin("Alice", "Johnson", "admin1", "alice@example.com")
# mhwp1 = MHWP("Bob", "Smith", "mhwp1", "bob@example.com")
# patient1 = Patient("John", "Doe", "patient1", "john@example.com")

# # Allocate a patient to an MHWP
# admin.allocate_patient_to_mhwp(patient1, mhwp1)

# # Edit patient's contact information
# admin.edit_user_info(patient1, email="newjohn@example.com")

# # Disable a user
# admin.disable_user(patient1)

# # Delete a user
# admin.delete_user(patient1)

# # Display summary of all users
# admin.display_summary()
