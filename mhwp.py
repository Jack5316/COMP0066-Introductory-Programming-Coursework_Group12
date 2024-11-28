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

#Aligned display calendar

    def display_calendar(self, start_time, end_time):
        """Display appointments scheduled within a given timeframe."""

        # Validate user input for correct datetime range
        if start_time >= end_time:
            print("Error: Start time must be earlier than end time.")
            return

        # Filter appointments within the given time frame
        appointments_in_timeframe = {
            time: appointment
            for time, appointment in self.appointment_calendar.items()
            if start_time <= time <= end_time
        }

        # Display results
        if appointments_in_timeframe:
            print(f"Appointments from {start_time} to {end_time}:")
            for time, appointment in sorted(appointments_in_timeframe.items()):
                patient = appointment.patientInstance  # Access the Patient instance
                status = appointment.status  # Access the appointment status
                print(f"- {time}: {patient.first_name} {patient.last_name} ({status})")
        else:
            print(f"No appointments scheduled between {start_time} and {end_time}.")

    def cancel_appointment(self, appointment):
        """Cancel an appointment by updating its status."""
        if appointment.status == "cancelled":
            print(
                f"Appointment with {appointment.patientInstance.first_name} {appointment.patientInstance.last_name} is already cancelled.")
        else:
            appointment.cancel()  # Use the cancel method from the Appointment class
            print(
                f"Appointment with {appointment.patientInstance.first_name} {appointment.patientInstance.last_name} has been cancelled.")
            # Remove the appointment from the MHWP calendar
            if appointment.date_time in self.appointment_calendar:
                self.appointment_calendar.pop(appointment.date_time)

    def confirm_appointment(self, appointment):
        """Confirm an appointment by updating its status."""
        if appointment.status == "confirmed":
            print(
                f"Appointment with {appointment.patientInstance.first_name} {appointment.patientInstance.last_name} is already confirmed.")
        else:
            appointment.confirm()  # Use the confirm method from the Appointment class
            print(
                f"Appointment with {appointment.patientInstance.first_name} {appointment.patientInstance.last_name} has been confirmed.")
            # Add the appointment to the MHWP calendar
            if appointment.date_time not in self.appointment_calendar:
                self.appointment_calendar[appointment.date_time] = appointment


    # CLI methods
    def cli_confirm_appointment(self):
        """Handle the CLI for confirming an appointment."""
        self.view_calendar()  # Show the current appointments

        if self.appointments:
            try:
                confirm_choice = int(input("Enter the number of the appointment to confirm: "))
                if 1 <= confirm_choice <= len(self.appointments):
                    appointment_to_confirm = self.appointments[confirm_choice - 1]

                    # Confirm the action
                    confirm = input(
                        f"Are you sure you want to confirm the appointment with {appointment_to_confirm.patientInstance.first_name} {appointment_to_confirm.patientInstance.last_name} on {appointment_to_confirm.date_time}? (y/n): ").lower()

                    if confirm == 'y':
                        self.confirm_appointment(appointment_to_confirm)  # Call the confirm method from MHWP
                    else:
                        print("Confirmation aborted.")
                else:
                    print("Invalid appointment number.")
            except ValueError:
                print("Please enter a valid number.")
        else:
            print("No appointments available to confirm.")

    def cli_cancel_appointment(self):
        """Handles the CLI for the MHWP to cancel appointments."""
        self.view_calendar()  # Show the current appointments

        if self.appointments:
            try:
                cancel_choice = int(input("Enter the number of the appointment to cancel: "))
                if 1 <= cancel_choice <= len(self.appointments):
                    appointment_to_cancel = self.appointments[cancel_choice - 1]

                    # Confirm cancellation
                    confirm = input(
                        f"Are you sure you want to cancel the appointment with {appointment_to_cancel.patientInstance.first_name} {appointment_to_cancel.patientInstance.last_name} on {appointment_to_cancel.date_time}? (y/n): ").lower()

                    if confirm == 'y':
                        self.cancel_appointment(appointment_to_cancel)  # Call the cancel method from MHWP
                    else:
                        print("Cancellation aborted.")
                else:
                    print("Invalid appointment number.")
            except ValueError:
                print("Please enter a valid number.")
        else:
            print("No appointments available to cancel.")











