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

    def display_conditions(self, predefined_conditions):
        print("Please select a condition from the following list:")
        for i, condition in enumerate(predefined_conditions, start=1):
            print(f"{i}. {condition}")

    def add_patient_info(self, patient_email, notes, mood):
        predefined_conditions = ['anxiety', 'autism', 'depression', 'bipolar disorder', 'OCD', 'PTSD']
        self.display_conditions(predefined_conditions)

        # User selects a condition
        try:
            choice = int(input("Enter the number of the condition: "))
            if 1 <= choice <= len(predefined_conditions):
                condition = predefined_conditions[choice - 1]
            else:
                print("Invalid choice. No condition selected.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        # Initialize patient data if not already present
        if patient_email not in self.patients:
            self.patients[patient_email] = {'conditions': [], 'notes': [], 'mood': []}

        # Add valid condition, notes, and mood
        self.patients[patient_email]['conditions'].append(condition)
        self.patients[patient_email]['notes'].append(notes)
        self.patients[patient_email]['mood'].append(mood)

    def display_patients_with_moods(self):
        mood_colors = {
            1: "\033[91m",  # Red for very bad mood
            2: "\033[93m",  # Yellow for bad mood
            3: "\033[92m",  # Green for neutral mood
            4: "\033[96m",  # Cyan for good mood
            5: "\033[94m",  # Blue for very good mood
        }
        reset_color = "\033[0m"  # Reset color to default

        print("\033[1mPatient Mood Tracker\033[0m")  # Bold header
        print("-" * 30)
        for email, data in self.patients.items():
            if data["mood"]:
                current_mood = data["mood"][-1]  # Use the last mood value
                mood_color = mood_colors.get(current_mood, reset_color)
            else:
                current_mood = "No mood data"
                mood_color = reset_color
            
            print(
                f"{mood_color}Email: {email}\n"
                f"Current Mood: {current_mood}\033[0m\n"  # Reset color after each section
            )
            print("-" * 30)

    def update_patient_health_record(self, patient, new_entry):
        # Add a new entry to the specified patient's health record.
        pass

    def display_summary_of_all_patients(self):
        # Display a summary of all patients, including mood tracking plots.
        pass