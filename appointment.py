
from datetime import datetime
from patient import Patient
from mhwp import MHWP

class Appointment:    
    def __init__(self, patient, mhwp, date_time, status="requested"):        
        self.patientUsername = patient
        self.mhwpUsername = mhwp
        self.date_time = date_time
        self.status = status

    def confirm(self):
        # notification sent to both patient and practitioner     
        self.status = "confirmed"

    def cancel(self):        
        # cancel should delete this instance of Appointment object
        # notification sent to both patient and practitioner
        self.status = "requested"

    def display_appointment(self):
        return (f"Appointment(Patient={self.patient}, MHWP={self.mhwp}, "
                f"DateTime={self.date_time}, Status={self.status})")