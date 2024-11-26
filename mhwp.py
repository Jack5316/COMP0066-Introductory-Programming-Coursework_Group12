from datetime import datetime
from user import User

class Patient(User):
    def __init__(self, first_name, last_name, email, username, password):
        super().__init__(first_name, last_name, email, "patient", username, password)


class MHWP(User):
    def __init__(self, first_name, last_name, email, user_type, username, password):

        super().__init__(first_name, last_name, email, "mhwp", username, password)
        self.all_patients = []  # List to store all Patient objects.
        self.appointment_calendar = {}  # Dictionary to store appointments.
        self.working_hours = {"start": "09:00", "end": "17:00"}  # MWWP working hours.

    def display_calendar(self, start_time, end_time):
    # Display appointments scheduled within a given timeframe.
    # Validate user input
        if start_time >= end_time:
            print("Error: Start time must be earlier than end time.")
            return

        # Filter appointments within given time frame
        appointments_in_timeframe = {
            time: appointment_info
            for time, appointment_info in self.appointment_calendar.items()
            if start_time <= time <= end_time
        }

        # Display results
        if appointments_in_timeframe:
            print(f"Appointments from {start_time} to {end_time}:")

            for time, appointment_info in sorted(appointments_in_timeframe.items()):
                patient = appointment_info["patient"]
                status = appointment_info["status"]
                print(f"- {time}: {patient.first_name} {patient.last_name} ({status})")
        else:
            print(f"No appointments scheduled between {start_time} and {end_time}.")

    def confirm_appointment(self, appointment_time):
        """
        Confirm an appointment by updating its status in the calendar.
        """
        if appointment_time in self.appointment_calendar:
            appointment = self.appointment_calendar[appointment_time]
            if appointment["status"] == "requested":
                appointment["status"] = "confirmed"
                patient = appointment["patient"]
                print(f"Appointment with {patient.first_name} {patient.last_name} on {appointment_time} confirmed.")
                # Notify patient
                self.notify_patient(
                    patient,
                    f"Your appointment on {appointment_time} has been confirmed."
                )
            else:
                print("Error: Appointment is already confirmed or canceled.")
        else:
            print("Error: No appointment found at the specified time.")

    def cancel_appointment(self, appointment_time):
        """
        Cancel an appointment and notify the patient.
        """
        if appointment_time in self.appointment_calendar:
            appointment = self.appointment_calendar[appointment_time]
            patient = appointment["patient"]

            # Remove the appointment from the calendar
            del self.appointment_calendar[appointment_time]
            print(f"Appointment with {patient.first_name} {patient.last_name} on {appointment_time} canceled.")

            # Notify the patient
            self.notify_patient(
                patient,
                f"Your appointment on {appointment_time} has been canceled."
            )
        else:
            print("Error: No appointment found at the specified time.")

    def notify_patient(self, patient, message):
        """
        Notify the patient with a message. Simulate email or SMS notifications.
        """
        print(f"Notification sent to {patient.email}: {message}")
