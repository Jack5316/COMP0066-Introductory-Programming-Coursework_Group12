from datetime import datetime
# from user import User

class MHWP(): #input is User
    def __init__(self, first_name, last_name, email, user_type, username, password):
        # super().__init__(first_name, last_name, email, user_type, username, password)
        self.patients = {}  # Dictionary to store patient information.
        self.all_patients = []  # List to store all Patient objects.
        self.appointment_calendar = {}  # Dictionary to store appointments.
        self.working_hours = {"start": "09:00", "end": "17:00"}  # MHWP working hours.

    def display_calendar(self, start_time, end_time):
        # Display appointments scheduled within a given timeframe.
        pass

    def cancel_appointment(self, appointment_time):
        # Cancel an appointment at a specified time.
        pass

    def confirm_appointment(self, appointment_time):
        # Confirm an appointment at a specified time.
        pass

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
        mood_emojis = {
            1: "💔",  # Very bad mood
            2: "👿",  # Bad mood
            3: "😐",  # Neutral mood
            4: "🙂",  # Good mood
            5: "🥳",  # Very good
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
                f"{mood_emojis.get(current_mood, '')}\n"
            )
            print("-" * 30)

    def update_patient_health_record(self, patient, new_entry):
        # Add a new entry to the specified patient's health record.
        pass

    def display_summary_of_all_patients(self):
        # Display a summary of all patients, including mood tracking plots.
        pass
