
from datetime import datetime
from patient import Patient
from mhwp import MHWP 

class Appointment:    
    def __init__(self, patient, mhwp, date_time, status="requested"):          
        self.patientInstance = patient
        self.mhwpInstance = mhwp
        self.date_time = date_time
        self.status = status

    def confirm(self):
        # notification sent to both patient and practitioner  
        self.status = "confirmed"
        # add object to mhwp calendar 
        if self.date_time not in self.mhwpInstance.appointment_calendar:
            self.mhwpInstance.appointment_calendar[self.date_time] = self
        if self.date_time not in self.patientInstance.patientCalendar:
            self.patientInstance.patientCalendar[self.date_time] = self
        print("Appointment has been confirmed")


    def cancel(self):        
        # cancel should delete this instance of Appointment object
        # notification sent to both patient and practitioner
        self.status = "cancelled"
        if self.date_time in self.patientInstance.patientCalendar:
            self.patientInstance.patientCalendar.pop(self.date_time)
        if self.date_time in self.mhwpInstance.appointment_calendar:
            self.mhwpInstance.appointment_calendar.pop(self.date_time)
        print("Appointment has been cancelled")


    def display_appointment(self):
        patient_name = self.patientInstance.first_name + " " + self.patientInstance.last_name
        mhwp_name = self.mhwpInstance.first_name + " " + self.mhwpInstance.last_name
        return (f"Appointment(Patient ={ patient_name}, MHWP = {mhwp_name}, "
                f"DateTime = {self.date_time}, Status = {self.status})")
    


# create a patient and practioner 

# test if confirm appointment works 
# make an appointment with patient  
# print out patient calendar to make sure it works
# run confirm / run cancel 

# check both patient and practioner calendar to make sure appropriate change has taken place 

