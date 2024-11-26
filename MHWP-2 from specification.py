from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt

# Mood levels and corresponding colors
moods = ["Very Happy", "Happy", "Neutral", "Sad", "Very Sad", "Angry"]
colors = ["green", "lime", "yellow", "orange", "red", "darkred"]


class MHWP:
    def __init__(self, email):
        self.email = email
        self.appointments = []
        self.patients = {}#patients objects

    def display_calendar(self):
        """
        Display all appointments with their status.
        """
        for appointment in self.appointments:
            print(f"Appointment with {appointment['patient']} on {appointment['date']} - Status: {appointment['status']}")

    def confirm_appointment(self, patient_email, appointment_date):
        for appointment in self.appointments:
            if appointment['patient'] == patient_email and appointment['date'] == appointment_date:
                appointment['status'] = 'Confirmed'
                self.send_email(patient_email, 'Appointment Confirmed', f"Your appointment on {appointment_date} has been confirmed.")
                self.send_email(self.email, 'Appointment Confirmed', f"Appointment with {patient_email} on {appointment_date} has been confirmed.")
                break

    def cancel_appointment(self, patient_email, appointment_date):
        for appointment in self.appointments:
            if appointment['patient'] == patient_email and appointment['date'] == appointment_date:
                appointment['status'] = 'Cancelled'
                self.send_email(patient_email, 'Appointment Cancelled', f"Your appointment on {appointment_date} has been cancelled.")
                self.send_email(self.email, 'Appointment Cancelled', f"Appointment with {patient_email} on {appointment_date} has been cancelled.")
                break

    def add_patient_info(self, patient_email, condition, notes):
        if patient_email not in self.patients:
            self.patients[patient_email] = {'conditions': [], 'notes': [], 'mood_tracking': []}
        self.patients[patient_email]['conditions'].append(condition)
        self.patients[patient_email]['notes'].append(notes)

    def display_dashboard(self):
        for patient_email, data in self.patients.items():
            print(f"Patient: {patient_email}")
            print(f"Conditions: {', '.join(data['conditions'])}")
            print(f"Notes: {', '.join(data['notes'])}")
            self.plot_mood_tracking(patient_email, data['mood_tracking'])
        

    # Mood tracker implementation
    def mood_tracker(self):
        fig, ax = plt.subplots(figsize=(8, 2))
        
        # Plotting each mood level
        for i, (mood, color) in enumerate(zip(moods, colors)):
            ax.bar(i, 1, color=color, edgecolor="black", align="center")
            ax.text(i, 1.2, mood, ha="center", fontsize=9)
        
        # Formatting the plot
        ax.set_xlim(-0.5, len(moods) - 0.5)
        ax.set_ylim(0, 1.5)
        ax.axis("off")
        plt.title("Mood Tracker", fontsize=14, weight="bold")
        plt.show()



    def plot_mood_tracking(self, patient_email, mood_tracking):
        dates = [entry['date'] for entry in mood_tracking]
        moods = [entry['mood'] for entry in mood_tracking]
        plt.plot(dates, moods)
        plt.title(f"Mood Tracking for {patient_email}")
        plt.xlabel('Date')
        plt.ylabel('Mood')
        plt.show()
        def select_conditions(self, patient_email, conditions):
            predefined_conditions = ['anxiety', 'autism', 'depression', 'bipolar disorder', 'OCD', 'PTSD']
            if patient_email not in self.patients:
                self.patients[patient_email] = {'conditions': [], 'notes': [], 'mood_tracking': []}
            for condition in conditions:
                if condition in predefined_conditions:
                    self.patients[patient_email]['conditions'].append(condition)
                else:
                    print(f"Condition '{condition}' is not in the predefined list.")
    def send_email(self, to_email, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, 'your_password')  # Replace with your email password
            text = msg.as_string()
            server.sendmail(self.email, to_email, text)
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")

# Example usage
mhwp = MHWP('mhwp@example.com')
mhwp.appointments.append({'patient': 'patient1@example.com', 'date': '2023-10-10', 'status': 'Requested'})
mhwp.confirm_appointment('patient1@example.com', '2023-10-10')
mhwp.add_patient_info('patient1@example.com', 'anxiety', 'Patient shows signs of anxiety.')
mhwp.display_dashboard()
mhwp.mood_tracker()