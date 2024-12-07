
from datetime import datetime
from user import User 
from patient import Patient
from mhwp import MHWP
from appointment import Appointment 



# At the start of your program, load appointments
Appointment.load_appointments()

practioner = MHWP("John", "Smith", "auctionsite097@gmail.com", username="bland", password="881")
patient_example = Patient("Patient", "Zeri", "auctionsite097@gmail.com", user_type="patient", username="diseas", password="881",
                  mhwpAsigned=practioner, emergencyEmail="auctionsite097@gmail.com", colourCode=None)


print(patient_example.patientCalendar)
patient_example.bookAppointment()

# practioner.cli_confirm_appointment()

print(patient_example.patientCalendar)






