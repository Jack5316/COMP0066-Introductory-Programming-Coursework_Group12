
from datetime import datetime
from user import User 
from patient import Patient
from mhwp import MHWP
from appointment import Appointment 



practioner = MHWP("John", "Smith", "him@gmail.com", user_type="mhwp", username="bland", password="881")
patient = Patient("Patient", "Zeri", "diseased@gmail.com", user_type="patient", username="diseas", password="881",
                  mhwpAsigned=practioner, emergencyEmail="disease@outlook.com", colourCode=None)

practioner.appointment_calendar = {"2024-12-15 09:00":"object"}
example_date = patient.bookAppointment()


new_appointment = Appointment(patient=patient, mhwp=practioner, date_time=example_date)


