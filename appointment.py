from datetime import datetime
from patient import Patient
from mhwp import MHWP 
from email_sender import send_email
import pickle 


class Appointment:

    all_appointment_objects = []

    def __init__(self, patient, mhwp, date_time, status="requested"):          
        self.patientInstance = patient
        self.mhwpInstance = mhwp
        self.date_time = date_time
        self.status = status

        self.patient_username = patient.username
        self.mhwp_username = mhwp.username

        patient.patientCalendar[date_time] = self
        Appointment.all_appointment_objects.append(self)
        Appointment.save_all_appointments()

    def confirm(self):
        # notification sent to both patient and practitioner  
        self.status = "confirmed"
        # add object to mhwp calendar 
        if self.date_time not in self.mhwpInstance.appointment_calendar:
            self.mhwpInstance.appointment_calendar[self.date_time] = self
        if self.date_time not in self.patientInstance.patientCalendar:
            self.patientInstance.patientCalendar[self.date_time] = self
        # print("Appointment has been confirmed")
        # email to patient
        subject = "Appointment Confirmed"
        body = (f"Your appointment with {self.mhwpInstance.first_name} {self.mhwpInstance.last_name} on {self.date_time} has been confirmed.\n\nThank you.")
        send_email([self.patientInstance.email], subject, body)
        #email to MHWP
        body_mhwp = (f"You have confirmed an appointment with {self.patientInstance.first_name} {self.patientInstance.last_name} on {self.date_time}.\n\nThank you.")
        send_email([self.mhwpInstance.email], subject, body_mhwp)
        # save appointment changes
        Appointment.save_all_appointments()

    def cancel(self):        
        # cancel should delete this instance of Appointment object
        # notification sent to both patient and practitioner
        self.status = "cancelled"
        if self.date_time in self.patientInstance.patientCalendar:
            self.patientInstance.patientCalendar.pop(self.date_time)
        if self.date_time in self.mhwpInstance.appointment_calendar:
            self.mhwpInstance.appointment_calendar.pop(self.date_time)
        # print("Appointment has been cancelled")
        # email to patient
        subject = "Appointment Cancelled"
        body = (f"Your appointment with {self.mhwpInstance.first_name} {self.mhwpInstance.last_name} on {self.date_time} has been cancelled.\n\nThank you.")
        send_email([self.patientInstance.email], subject, body)
        # email to MHWP
        body_mhwp = (f"You have cancelled an appointment with {self.patientInstance.first_name} {self.patientInstance.last_name} on {self.date_time}.\n\nThank you.")
        send_email([self.mhwpInstance.email], subject, body_mhwp)

        # save appointment changes
        Appointment.save_all_appointments()

    def display_appointment(self):
        patient_name = self.patientInstance.first_name + " " + self.patientInstance.last_name
        mhwp_name = self.mhwpInstance.first_name + " " + self.mhwpInstance.last_name
        return (f"Appointment(Patient ={ patient_name}, MHWP = {mhwp_name}, "
                f"DateTime = {self.date_time}, Status = {self.status})")
    

    @staticmethod
    def save_all_appointments(file_name="appointments.pkl"):
        try:
            with open(file_name, "wb") as file:
                pickle.dump(Appointment.all_appointment_objects, file)
            print(f"Appointments have been saved to {file_name}.")
        except:
            print("Unable to save appointments")
    
    @staticmethod
    def load_appointments(file_name="appointments.pkl"):
        try:
            with open(file_name, "rb") as file:
                Appointment.all_appointment_objects = pickle.load(file)
            print(f"Appointments have been loaded from {file_name}.")

            # Use the all_users dictionary from User class
            from user import User
            all_users_dict = User.all_user_objects  # username -> user object

            # Now loop over each appointment and set the references
            for appointment_obj in Appointment.all_appointment_objects:
                try:
                    patient = all_users_dict[appointment_obj.patient_username]
                    mhwp = all_users_dict[appointment_obj.mhwp_username]
                except KeyError:
                    print(f"Patient and MHWP details could not be found for appointment on {appointment_obj.date_time}")
                    patient = None 
                    mhwp = None

                # reinsert appointment details back into appropriate classes
                if patient and mhwp:
                    appointment_obj.patientInstance = patient
                    appointment_obj.mhwpInstance = mhwp
                    patient.patientCalendar[appointment_obj.date_time] = appointment_obj
                    mhwp.appointment_calendar[appointment_obj.date_time] = appointment_obj

        except FileNotFoundError:
            print(f"No file called {file_name} has been found. Application will start with an empty appointment list.")
            Appointment.all_appointment_objects = []
        except Exception as e:
            print("The following error occured whilst loading appointments: ", e)

