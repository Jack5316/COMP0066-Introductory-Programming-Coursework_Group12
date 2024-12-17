# CLI Main Program
from user import User
from admin import Admin
from patient import Patient
from mhwp import MHWP
from appointment import Appointment

def initialize_users():
    User.user_dictionary = {}
    User.all_user_objects = {}

    mhwp1 = MHWP("John", "Smith", "him@gmail.com", username="mhwp1", password="")
    mhwp2 = MHWP("Jane", "Smith", "her@gmail.com", username="mhwp2", password="")
    mhwp3 = MHWP("Joanna", "Smith", "heragain@gmail.com", username="mhwp3", password="")
    patient1 = Patient("Patient", "One", "diseased@gmail.com", user_type="patient", username="patient1", password="",
                  mhwpAsigned=mhwp1, emergencyEmail="disease@outlook.com", colourCode=None)
    patient2 = Patient("Patient", "Two", "debilitated@gmail.com", user_type="patient", username="patient2", password="",
                  mhwpAsigned=mhwp2, emergencyEmail="debilitation@outlook.com", colourCode=None)
    patient3 = Patient("Patient", "Three", "wasted@gmail.com", user_type="patient", username="patient3", password="",
                  mhwpAsigned=mhwp3, emergencyEmail="wasted@outlook.com", colourCode=None)
    admin = Admin("Admin", "Adamson", "adminadamson@gmail.com",user_type= "admin", username="admin", password="")
    
    User.all_user_objects[admin.username] = admin
    User.all_user_objects[patient1.username] = patient1
    User.all_user_objects[patient2.username] = patient2
    User.all_user_objects[patient3.username] = patient3
    User.all_user_objects[mhwp1.username] = mhwp1
    User.all_user_objects[mhwp2.username] = mhwp2

    User.user_dictionary[admin.username] = admin.password
    User.user_dictionary[patient1.username] = patient1.password
    User.user_dictionary[patient2.username] = patient2.password
    User.user_dictionary[patient2.username] = patient3.password
    User.user_dictionary[mhwp1.username] = mhwp1.password
    User.user_dictionary[mhwp2.username] = mhwp2.password

def main_menu():
    User.load_users()
    Appointment.load_appointments()

    if not User.all_user_objects:
        initialize_users()
        User.save_users()

    while True:
        print("\n--- Breeze Mental Health Management System ---")
        print("1. Login")
        print("2. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            login()
        elif choice == "2":
            Appointment.save_all_appointments()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ")
    User.login(username, password)

    if User.user_session:
        user = get_user_instance(username)
        if isinstance(user, Admin):
            admin_menu(user)
        elif isinstance(user, Patient):
            patient_menu(user)
        elif isinstance(user, MHWP):
            mhwp_menu(user)
    else:
        print("Login failed.")

def admin_menu(admin):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Allocate Patient to MHWP")
        print("2. Edit User Information")
        print("3. Delete User")
        print("4. Disable User")
        print("5. Display Summary")
        print("6. Logout")
        choice = input("Select an option: ").strip()

        if choice == "1":
            patient_username = input("Enter patient username: ").strip()
            mhwp_username = input("Enter MHWP username: ").strip()
            patient = get_user_instance(patient_username)
            mhwp = get_user_instance(mhwp_username)
            if patient and mhwp:
                admin.allocate_patient_to_mhwp(patient, mhwp)
                User.save_users()
            else:
                print("Invalid patient or MHWP username.")
        elif choice == "2":
            edit_user_menu(admin)
        elif choice == "3":
            username = input("Enter username to delete: ").strip()
            user = get_user_instance(username)
            if user:
                admin.delete_user(user)
                User.save_users()
            else:
                print("Invalid username.")
        elif choice == "4":
            username = input("Enter username to disable: ").strip()
            user = get_user_instance(username)
            if user:
                admin.disable_user(user)
                User.save_users()
            else:
                print("Invalid username.")
        elif choice == "5":
            admin.display_summary()
        elif choice == "6":
            User.logout()
            break
        else:
            print("Invalid choice. Please try again.")

def edit_user_menu(admin):
    while True:
        print("\n--- Edit User Information ---")
        print("1. Edit MHWP Information")
        print("2. Edit Patient Information")
        print("3. Return to Admin Menu")
        choice = input("Select an option: ").strip()
        if choice == "1":
            username = input("Enter MHWP username to edit: ").strip()
            user = get_user_instance(username)
            if isinstance(user, MHWP):
                edit_mhwp_info(admin, user)
                User.save_users()
            else:
                print("Invalid MHWP username.")
        elif choice == "2":
            username = input("Enter Patient username to edit: ").strip()
            user = get_user_instance(username)
            if isinstance(user, Patient):
                edit_patient_info(admin, user)
                User.save_users()
            else:
                print("Invalid Patient username.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def edit_mhwp_info(admin, mhwp):
    while True:
        print("\n--- Edit MHWP Information ---")
        print(f"Current First Name: {mhwp.first_name}")
        print(f"Current Last Name: {mhwp.last_name}")
        print(f"Current Email: {mhwp.email}")
        print("1. Change First Name")
        print("2. Change Last Name")
        print("3. Change Email")
        print("4. Return to Edit User Menu")
        choice = input("Select an option: ").strip()
        if choice == "1":
            new_first_name = input("Enter new first name: ").strip()
            admin.edit_user_info(mhwp, first_name=new_first_name)
        elif choice == "2":
            new_last_name = input("Enter new last name: ").strip()
            admin.edit_user_info(mhwp, last_name=new_last_name)
        elif choice == "3":
            new_email = input("Enter new email: ").strip()
            admin.edit_user_info(mhwp, email=new_email)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def edit_patient_info(admin, patient):
    while True:
        print("\n--- Edit Patient Information ---")
        print(f"Current First Name: {patient.first_name}")
        print(f"Current Last Name: {patient.last_name}")
        print(f"Current Email: {patient.email}")
        print(f"Current Emergency Email: {patient.emergencyEmail}")
        print("1. Change First Name")
        print("2. Change Last Name")
        print("3. Change Email")
        print("4. Change Emergency Email")
        print("5. Return to Edit User Menu")
        choice = input("Select an option: ").strip()
        if choice == "1":
            new_first_name = input("Enter new first name: ").strip()
            admin.edit_user_info(patient, first_name=new_first_name)
        elif choice == "2":
            new_last_name = input("Enter new last name: ").strip()
            admin.edit_user_info(patient, last_name=new_last_name)
        elif choice == "3":
            new_email = input("Enter new email: ").strip()
            admin.edit_user_info(patient, email=new_email)
        elif choice == "4":
            new_emergency_email = input("Enter new emergency email: ").strip()
            admin.edit_user_info(patient, emergency_email=new_emergency_email)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def patient_menu(patient):
    while True:
        if patient.blocked:
            print("\n--- Patient Menu ---")
            print("User blocked! Only logout is allowed.")
            print("1. Logout")
            choice = input("Select an option: ").strip()
            if choice == "1":
                User.logout()
                break
        else:
            print("\n--- Patient Menu ---")
            print("1. Edit Personal Information")
            print("2. Add Mood of the Day")
            print("3. Access Meditation and Relaxation Resources")
            print("4. Book an Appointment")
            print("5. View Appointments")
            print("6. Cancel an Appointment")
            print("7. Export Appointments ")
            print("8. Enter Journal Entry")
            print("9. See All Journal Entries")
            print("10. Search Journal Entry by Keyword")
            print("11. Logout")
            choice = input("Select an option: ").strip()

            if choice == "1":
                updatePersonalInfo(patient)
                User.save_users()
            elif choice == "2":
                patient.moodTracker()
                User.save_users()
            elif choice == "3":
                Patient.searchExercises()
            elif choice == "4":
                bookAppointment(patient)
            elif choice == "5":
                patient.displayAllAppointments()
            elif choice == "6":
                patient.cancelAppointment()
            elif choice == "7":
                patient.cli_export_appointments()
            elif choice == "8":
                patient.journal()
            elif choice == "9":
                patient.show_all_journal_entries()
            elif choice == "10":
                patient.search_journal_entries()
            elif choice == "11":
                User.logout()
                break
            else:
                print("Invalid choice. Please try again.")

def updatePersonalInfo(patient):
    print("\n--- Update Personal Information ---")
    print(f"Current First Name: {patient.first_name}")
    print(f"Current Last Name: {patient.last_name}")
    print(f"Current Email: {patient.email}")
    print(f"Current Emergency Email: {patient.emergencyEmail}")
    print("1. Update First Name")
    print("2. Update Last Name")
    print("3. Update Email")
    print("4. Update Emergency Email")
    print("5. Return to Patient Menu")

    while True:
        try:
            choice = int(input("Select an option: ").strip())
            if choice == 1:
                patient.update_first_name()
                break
            elif choice == 2:
                patient.update_last_name()
                break
            elif choice == 3:
                patient.updateEmail()
                break
            elif choice == 4:
                patient.updateEmergencyContact()
                break
            elif choice == 5:
                print("Returning to Patient Menu...")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            
def bookAppointment(patient):
    #for booking different types of appointments
    print("\n--- Appointment Booking ---")
    print("1. Book a Regular Appointment")
    print("2. Book the Soonest Available Appointment")
    print("3. Book an Emergency Appointment")
    print("4. Return to Patient Menu")
    
    while True:
        try:
            choice = int(input("Select an option: "))
            if choice == 1:
                print("\nBooking a Regular Appointment...")
                patient.bookAppointment()
                break
            elif choice == 2:
                print("\nBooking the Soonest Available Appointment...")
                patient.bookSoonestAppointment()
                break
            elif choice == 3:
                print("\nBooking an Emergency Appointment...")
                patient.emergencyAppointment()
                break
            elif choice == 4:
                print("Returning to Patient Menu...")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def mhwp_menu(mhwp):
    while True:
        if mhwp.blocked:
            print("\n--- MHWP Menu ---")
            print("User blocked! Only logout is allowed.")
            print("1. Logout")
            choice = input("Select an option: ").strip()
            if choice == "1":
                User.logout()
                break
        else:
            print("\n--- MHWP Menu ---")
            print("1. View Calendar")
            print("2. Confirm Appointment")
            print("3. Cancel Appointment")
            print("4. Handle Requests")
            print("5. Add Patient Notes/Conditions")
            print("6. View Patient Summary")
            print("7. Export Appointments")
            print("8. Unavailable Periods")
            print("9. Logout")
            choice = input("Select an option: ").strip()

            if choice == "1":
                start_time = input("Enter start time (YYYY-MM-DD): ").strip()
                end_time = input("Enter end time (YYYY-MM-DD): ").strip()
                mhwp.display_calendar(start_time, end_time)
            elif choice == "2":
                mhwp.cli_confirm_appointment()
            elif choice == "3":
                mhwp.cli_cancel_appointment()
            elif choice == "4":
                mhwp.cli_handle_requested_appointments()
            elif choice == "5":
                managePatientRecords(mhwp)
                User.save_users()
            elif choice == "6":
                mhwp.display_patients_with_moods()
            elif choice == "7":
                mhwp.cli_export_appointments()
            elif choice == "8":
                mhwp.cli_set_unavailable_period()
            elif choice == "9":
                User.logout()
                break
            else:
                print("Invalid choice. Please try again.")

def managePatientRecords(mhwp):
    while True:
        print("\n--- Manage Patient Records ---")
        print("1. Add Patient Note")
        print("2. Add Patient Condition")
        print("3. Return to MHWP Menu")
        try:
            choice = int(input("Select an option: ").strip())
            if choice == 1:
                mhwp.add_patient_note()
                break
            elif choice == 2:
                mhwp.add_patient_condition()
                break
            elif choice == 3:
                print("Returning to MHWP Menu...")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_user_instance(username):
    username_clean = str(username).strip().lower()
    return User.all_user_objects.get(username_clean)

# # Example Users
# admin = Admin("Alice", "Johnson", "admin1", "alice@example.com")
# mhwp1 = MHWP("Dr. Smith", "Therapist", "drsmith@example.com", "mhwp", "mhwp1", "")
# patient1 = Patient("John", "Doe", "johndoe@example.com", "patient", "patient1", "", mhwp1, "emergency@example.com", [])
# patient2 = Patient("Jane", "Doe", "janedoe@example.com", "patient", "patient2", "", mhwp1, "emergency@example.com", [])


#practioner = MHWP("John", "Smith", "him@gmail.com", username="mhwp1", password="")
#patient = Patient("Patient", "Zeri", "diseased@gmail.com", user_type="patient", username="patient1", password="",
#                  mhwpAsigned=practioner, emergencyEmail="disease@outlook.com", colourCode=None)
#admin = Admin("Alex", "Chris", "alex@gmail.com",user_type= "admin", username="alex", password="881")


if __name__ == "__main__":
    main_menu()