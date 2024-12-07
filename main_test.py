
from datetime import datetime
from user import User 
from patient import Patient
from mhwp import MHWP
from appointment import Appointment 




practioner = MHWP("John", "Smith", "auctionsite097@gmail.com", username="bland", password="881")
patient_example = Patient("Patient", "Zeri", "auctionsite097@gmail.com", user_type="patient", username="diseas", password="881",
                  mhwpAsigned=practioner, emergencyEmail="auctionsite097@gmail.com", colourCode=None)

# ONLY run load_appointments after setting up basic users 
Appointment.load_appointments()
print(Appointment.all_appointment_objects)

print(patient_example.patientCalendar)
patient_example.bookAppointment()
# practioner.cli_confirm_appointment()


print(Appointment.all_appointment_objects)
