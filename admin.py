from datetime import datetime

class User:
    users = {}  # Dictionary to store all users

    def __init__(self, username, age=None, first_name=None, last_name=None, email=None, user_type="User"):
        self.username = username
        self.age = age
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_type = user_type
        self.blocked = False
        User.users[username] = self  # Add the user to the dictionary
class Patient(User):
    def __init__(self, username, age, address):
        super().__init__(username, age)
        self.address = address
        self.assigned_mhwp = None
        self.appointments = []  # List of confirmed bookings

class MHWP(User):
    def __init__(self, username, experience, specialization):
        super().__init__(username, first_name=None, last_name=None, email=None, user_type="MHWP")
        self.experience = experience
        self.specialization = specialization
        self.patients_list = []  # List of assigned patients
        self.appointments = []  # List of confirmed bookings


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


# Create an Admin user
admin = Admin(first_name="Alice", last_name="Johnson", username="admin1", email="alice@example.com")

# Create an MHWP and two Patients
mhwp1 = MHWP(username="mhwp1", experience=5, specialization="Therapist")
patient1 = Patient(username="patient1", age=30, address="123 Elm Street")
patient2 = Patient(username="patient2", age=25, address="789 Oak Street")

# Allocate both patients to the MHWP
print("\nAllocating Patients to the MHWP:")
admin.allocate_patient_to_mhwp(patient1, mhwp1)
admin.allocate_patient_to_mhwp(patient2, mhwp1)

# Edit the first patient's contact information
print("\nEditing First Patient's Contact Information:")
admin.edit_user_info(patient1, email="newjohn@example.com", address="456 Maple Avenue")

# Edit the second patient's contact information
print("\nEditing Second Patient's Contact Information:")
admin.edit_user_info(patient2, email="secondpatient@example.com", address="987 Pine Street")

# Disable the first patient
print("\nDisabling the First Patient:")
admin.disable_user(patient1)

# Delete the second patient
print("\nDeleting the Second Patient:")
admin.delete_user(patient2)

# Display summary of all users
print("\nDisplaying Summary of All Users:")
admin.display_summary()
