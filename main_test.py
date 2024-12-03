
from datetime import datetime
from user import User 
from patient import Patient
from mhwp import MHWP
from appointment import Appointment 



practioner = MHWP("John", "Smith", "auctionsite097@gmail.com", user_type="mhwp", username="bland", password="881")
patient = Patient("Patient", "Zeri", "auctionsite097@gmail.com", user_type="patient", username="diseas", password="881",
                  mhwpAsigned=practioner, emergencyEmail="auctionsite097@gmail.com", colourCode=None)

example_date = patient.bookAppointment()


new_appointment = Appointment(patient=patient, mhwp=practioner, date_time=example_date)

new_appointment.confirm()