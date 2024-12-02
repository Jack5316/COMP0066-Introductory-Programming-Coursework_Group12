# CLI Main Program
from user import User
from admin import Admin
from patient import Patient
from mhwp import MHWP
from appointment import Appointment



def main_menu():
    while True:
        print("\n--- Breeze Mental Health Management System ---")
        print("1. Login")
        print("2. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            login()
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
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
            else:
                print("Invalid patient or MHWP username.")
        elif choice == "2":
            username = input("Enter username to edit: ").strip()
            user = get_user_instance(username)
            if user:
                field = input("Enter the field to update: ").strip()
                value = input(f"Enter new value for {field}: ").strip()
                admin.edit_user_info(user, **{field: value})
        elif choice == "3":
            username = input("Enter username to delete: ").strip()
            user = get_user_instance(username)
            if user:
                admin.delete_user(user)
            else:
                print("Invalid username.")
        elif choice == "4":
            username = input("Enter username to disable: ").strip()
            user = get_user_instance(username)
            if user:
                admin.disable_user(user)
            else:
                print("Invalid username.")
        elif choice == "5":
            admin.display_summary()
        elif choice == "6":
            User.logout()
            break
        else:
            print("Invalid choice. Please try again.")

def patient_menu(patient):
    while True:
        print("\n--- Patient Menu ---")
        print("1. Edit Personal Information")
        print("2. Add Mood of the Day")
        print("3. Enter Journal Entry")
        print("4. Access Meditation and Relaxation Resources")
        print("5. Book an Appointment")
        print("6. View Appointments")
        print("7. Cancel an Appointment")
        print("8. Logout")
        choice = input("Select an option: ").strip()

        if choice == "1":
            field = input("Enter the field to update (e.g., email, emergency contact): ").strip()
            value = input(f"Enter new value for {field}: ").strip()
            setattr(patient, field, value)
            print(f"{field} updated successfully.")
        elif choice == "2":
            patient.moodTracker()
        elif choice == "3":
            patient.journal()
        elif choice == "4":
            Patient.searchExercises()
        elif choice == "5":
            appointment_time = patient.bookAppointment()
            if appointment_time:
                print(f"Appointment requested for {appointment_time}.")
        elif choice == "6":
            patient.displayAllAppointments()
        elif choice == "7":
            appointment_time = input("Enter the appointment time to cancel (YYYY-MM-DD HH:MM): ").strip()
            if appointment_time in patient.patientCalendar:
                appointment = patient.patientCalendar[appointment_time]
                patient.cancelAppointment(appointment)
            else:
                print("No appointment found at the given time.")
        elif choice == "8":
            User.logout()
            break
        else:
            print("Invalid choice. Please try again.")

def mhwp_menu(mhwp):
    while True:
        print("\n--- MHWP Menu ---")
        print("1. View Calendar")
        print("2. Confirm Appointment")
        print("3. Cancel Appointment")
        print("4. Add Patient Notes/Conditions")
        print("5. View Patient Mood Tracker Summary")
        print("6. Logout")
        choice = input("Select an option: ").strip()

        if choice == "1":
            start_time = input("Enter start time (YYYY-MM-DD HH:MM): ").strip()
            end_time = input("Enter end time (YYYY-MM-DD HH:MM): ").strip()
            mhwp.display_calendar(start_time, end_time)
        elif choice == "2":
            appointment_time = input("Enter the appointment time to confirm (YYYY-MM-DD HH:MM): ").strip()
            mhwp.confirm_appointment(appointment_time)
        elif choice == "3":
            appointment_time = input("Enter the appointment time to cancel (YYYY-MM-DD HH:MM): ").strip()
            mhwp.cancel_appointment(appointment_time)
        elif choice == "4":
            patient_email = input("Enter patient's email: ").strip()
            notes = input("Enter notes: ").strip()
            mood = input("Enter mood: ").strip()
            mhwp.add_patient_info(patient_email, notes, mood)
        elif choice == "5":
            mhwp.display_patients_with_moods()
        elif choice == "6":
            User.logout()
            break
        else:
            print("Invalid choice. Please try again.")

def get_user_instance(username):
    """
    Fetch the user instance by username. Assume users are stored in a dictionary.
    """
    for user in [patient, practioner]:  # Replace with your actual user storage mechanism
        if user.username == username:
            return user
    return None

# # Example Users
# admin = Admin("Alice", "Johnson", "admin1", "alice@example.com")
# mhwp1 = MHWP("Dr. Smith", "Therapist", "drsmith@example.com", "mhwp", "mhwp1", "")
# patient1 = Patient("John", "Doe", "johndoe@example.com", "patient", "patient1", "", mhwp1, "emergency@example.com", [])
# patient2 = Patient("Jane", "Doe", "janedoe@example.com", "patient", "patient2", "", mhwp1, "emergency@example.com", [])


practioner = MHWP("John", "Smith", "him@gmail.com", user_type="mhwp", username="bland", password="881")
patient = Patient("Patient", "Zeri", "diseased@gmail.com", user_type="patient", username="diseas", password="881",
                  mhwpAsigned=practioner, emergencyEmail="disease@outlook.com", colourCode=None)

if __name__ == "__main__":
    main_menu()
