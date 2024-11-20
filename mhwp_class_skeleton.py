from datetime import datetime
from user import User

class MHWP(User):
    def __init__(self, first_name, last_name, email, user_type, username, password):

        # #Initialize MHWP instance, inheriting from the User class.
        # Aruments:
        #     first_name (str): First name of the MHWP.
        #     last_name (str): Last name of the MHWP.
        #     email (str): Email address of the MHWP.
        #     user_type (str): Type of user (e.g., 'MHWP').
        #     username (str): Username for login.
        #     password (str): Password for login.
        # Ensures that all the attributes defined in the parent class(User) are properly initialized when an MHWP object is created.

        super().__init__(first_name, last_name, email, user_type, username, password)
        self.all_patients = []  # List to store all Patient objects.
        self.appointment_calendar = {}  # Dictionary to store appointments.
        self.working_hours = {"start": "09:00", "end": "17:00"}  # MWWP working hours.

    def display_calendar(self, start_time, end_time):
        #Display appointments scheduled within a given timeframe.
        pass

    def cancel_appointment(self, appointment_time):
        #Cancel an appointment at a specified time.
        #Updates the appointment calendar and notifies the patient.
        pass

    def confirm_appointment(self, appointment_time):
        #confirm an appointment at a specified time.
        #Updates the appointment calendar and notifies the patient.
        pass

    def update_patient_health_record(self, patient, new_entry):
        #Add a new entry to the specified patient's health record.
        pass

    def display_summary_of_all_patients(self):
        #Display a summary of all patients, including mood tracking plots.
        #Iterates through the list of patients and collates data.
        pass
