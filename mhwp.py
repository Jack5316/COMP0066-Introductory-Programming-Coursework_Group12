from datetime import datetime, timedelta
from user import User
from time import gmtime, strftime
from patient import Patient
from utils import export_appointments_to_ics

class MHWP(User):
    def __init__(self, first_name, last_name, email, username, password):
        # Call the parent class constructor to initialize user-related attributes
        super().__init__(first_name, last_name, email, "mhwp", username, password)

        # Initialize attributes specific to MHWP
        self.all_patients = []  # List to store all Patient objects
        self.appointment_calendar = {}  # Dictionary to store appointments by date/time
        self.unavailable_periods = []  # List to store unavailable periods
        self.working_hours = {"start": "09:00", "end": "17:00"}  # MHWP working hours

    # SET UNAVAILABLE TIME PERIOD E.G. HOLIDAYS

    def set_unavailable_period(self, start_date, end_date):
        """Set a period during which the MHWP is unavailable."""
        # Validate the date range
        try:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())
        except Exception as e:
            print(f"Error in date conversion: {e}")
            return

        if start_datetime >= end_datetime:
            print("Error: Start date must be earlier than end date.")
            return

        # Add the additional check here to ensure the end date is after the start date
        if end_datetime <= start_datetime:
            print("Error: End date must be after start date.")
            return

        # Mark the unavailable period
        if not hasattr(self, 'unavailable_periods'):
            self.unavailable_periods = []  # Initialize if not already present

        self.unavailable_periods.append((start_datetime, end_datetime))
        print(f"Unavailable period set from {start_date} to {end_date}.")


    def cli_set_unavailable_period(self):
        """Handle the CLI for setting unavailable periods."""
        try:
            start_date = input("Enter the start date for the unavailable period (YYYY-MM-DD): ")
            end_date = input("Enter the end date for the unavailable period (YYYY-MM-DD): ")
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            self.set_unavailable_period(start_date, end_date)
        except ValueError:
            print("Invalid date format. Please enter the dates in YYYY-MM-DD format.")


    # DISPLAY CALENDAR

    def display_calendar(self, start_date, end_date):
        """Display appointments scheduled within a given date range, including unavailable periods."""

        # Convert dates to datetime with range covering the whole days
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        # Validate date range
        if start_datetime >= end_datetime:
            print("Error: Start date must be earlier than end date.")
            return

        # Display unavailable periods
        print("\033[1mUnavailable Periods:\033[0m")
        if hasattr(self, 'unavailable_periods'):
            for start, end in self.unavailable_periods:
                if start <= end_datetime and end >= start_datetime:  # Overlaps with the requested range
                    print(f"- {start} to {end}")
        else:
            print("No unavailable periods set.")

        # Display appointments
        appointments_in_date_range = {
            time: appointment
            for time, appointment in self.appointment_calendar.items()
            if start_datetime <= time <= end_datetime
        }

        print("\033[1mScheduled Appointments:\033[0m")
        if appointments_in_date_range:
            for time, appointment in sorted(appointments_in_date_range.items()):
                patient = appointment.patientInstance  # Access the Patient instance
                status = appointment.status  # Access the appointment status
                print(f"- {time}: {patient.first_name} {patient.last_name} ({status})")
        else:
            print(f"No appointments scheduled between in given time range.")

    # CONFIRM APPOINTMENT

    def confirm_appointment(self, appointment):
        """Confirm an appointment by updating its status."""
        if appointment.status == "confirmed":
            print(
                f"Appointment with {appointment.patientInstance.first_name} {appointment.patientInstance.last_name} is already confirmed.")
        else:
            appointment.confirm()  # Use the confirm method from the Appointment class
            print(
                f"Appointment with {appointment.patientInstance.first_name} {appointment.patientInstance.last_name} has been confirmed.")


    def cli_confirm_appointment(self):
        """Handle the CLI for confirming an appointment."""
        # Get the timeframe to display relevant appointments
        start_date_str = input("Enter the start date for viewing appointments (YYYY-MM-DD): ")
        end_date_str = input("Enter the end date for viewing appointments (YYYY-MM-DD): ")
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        # Check if there are any appointments to confirm
        appointments_to_confirm = [
            appt for appt in self.appointment_calendar.values()
            if appt.status == "requested" and start_date <= appt.date_time.date() <= end_date
        ]

        if appointments_to_confirm:
            for idx, appt in enumerate(appointments_to_confirm, start=1):
                print(f"{idx}. {appt.date_time} - {appt.patientInstance.first_name} {appt.patientInstance.last_name}")

            try:
                confirm_choice = int(input("Enter the number of the appointment to confirm: "))
                if 1 <= confirm_choice <= len(appointments_to_confirm):
                    appointment_to_confirm = appointments_to_confirm[confirm_choice - 1]

                    # Confirm the action
                    confirm = input(
                        f"Are you sure you want to confirm the appointment with "
                        f"{appointment_to_confirm.patientInstance.first_name} "
                        f"{appointment_to_confirm.patientInstance.last_name} "
                        f"on {appointment_to_confirm.date_time}? (y/n): "
                    ).lower()

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

    # CANCEL APPOINTMENT
    def cancel_appointment(self, appointment):
        """Cancel an appointment by updating its status."""
        if appointment.status == "cancelled":
            print(
                f"Appointment with {appointment.patientInstance.first_name} {appointment.patientInstance.last_name} is already cancelled.")
        else:
            appointment.cancel()  # Use the cancel method from the Appointment class
            print(
                f"Appointment with {appointment.patientInstance.first_name} {appointment.patientInstance.last_name} has been cancelled.")


    def cli_cancel_appointment(self):
        """Handles the CLI for the MHWP to cancel appointments."""

        # Get the timeframe to display relevant appointments
        start_date_str = input("Enter the start date for viewing appointments (YYYY-MM-DD): ")
        end_date_str = input("Enter the end date for viewing appointments (YYYY-MM-DD): ")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        # Check if there are any appointments to cancel (allow for both 'requested' and 'confirmed' statuses)
        appointments_to_cancel = [
            appt for appt in self.appointment_calendar.values()
            if start_date <= appt.date_time.date() <= end_date and appt.status != "cancelled"
        ]

        if appointments_to_cancel:
            for idx, appt in enumerate(appointments_to_cancel, start=1):
                print(
                    f"{idx}. {appt.date_time} - {appt.patientInstance.first_name} {appt.patientInstance.last_name} ({appt.status})")

            try:
                cancel_choice = int(input("Enter the number of the appointment to cancel: "))
                if 1 <= cancel_choice <= len(appointments_to_cancel):
                    appointment_to_cancel = appointments_to_cancel[cancel_choice - 1]

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

    # VIEW REQUESTS
    def view_requests(self):
        """Display enumerated appointments with the 'requested' status."""
        # Filter appointments with 'requested' status
        requested_appointments = [
            (time, appointment)
            for time, appointment in sorted(self.appointment_calendar.items())
            if appointment.status == "requested"
        ]
        return requested_appointments


    def cli_handle_requested_appointments(self):
        """Handle the CLI for managing requested appointments."""
        while True:
            requested_appointments = self.view_requests()

            # Only print if there are appointments
            if requested_appointments:
                print("\033[1mRequested Appointments:\033[0m")  # Bold header
                for idx, (time, appointment) in enumerate(requested_appointments, start=1):
                    patient = appointment.patientInstance  # Access the Patient instance
                    print(f"{idx}. {time}: {patient.first_name} {patient.last_name} ({appointment.status})")
            else:
                print("No requested appointments at the moment.")
                return  # Exit if there are no requested appointments

            try:
                # Get the user's selection
                choice = int(input("Enter the number of the appointment to manage (or 0 to exit): "))

                if choice == 0:
                    print("Exiting request management.")
                    return

                if 1 <= choice <= len(requested_appointments):
                    # Get the selected appointment
                    selected_time, selected_appointment = requested_appointments[choice - 1]

                    # Ask for confirmation or cancellation
                    action = input(f"Do you want to (c)onfirm or (x)ancel the appointment with "
                                f"{selected_appointment.patientInstance.first_name} "
                                f"{selected_appointment.patientInstance.last_name} on {selected_time}? ").lower()

                    if action == 'c':
                        self.confirm_appointment(selected_appointment)
                    elif action == 'x':
                        self.cancel_appointment(selected_appointment)
                    else:
                        print("Invalid action. Please choose 'c' to confirm or 'x' to cancel.")
                else:
                    print("Invalid number. Please select a valid appointment.")
            except ValueError:
                print("Please enter a valid number.")

    # EXPORT APPOINTMENTS TO CALENDAR
    def export_appointments_to_ics(self, start_date, end_date):
        """
        Export the MHWP's confirmed appointments within the specified date range to an .ics file.
        """
        filename_prefix = f"{self.first_name}_{self.last_name}"
        print(f"Exporting {filename_prefix}'s calendar...")
        export_appointments_to_ics(self.appointment_calendar, start_date, end_date, filename_prefix, is_mhwp=True)

    def cli_export_appointments(self):
        """
        CLI for exporting MHWP's appointments to an ICS file.
        """
        print("Exporting MHWP appointments to ICS file.")
        start_date_str = input("Enter start date (YYYY-MM-DD): ")
        end_date_str = input("Enter end date (YYYY-MM-DD): ")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            # Call export function
            export_appointments_to_ics(self.appointment_calendar, start_date, end_date,
                                       f"{self.first_name}_{self.last_name}")

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")



    def display_conditions(self, predefined_conditions):
        print("Please select a condition from the following list:")
        for i, condition in enumerate(predefined_conditions, start=1):
            print(f"{i} - {condition}")


    def select_patient(self):
        """Function allows the MHWP to select a patient from all their patients  

        Returns:
            Patient: The selected object for the selected patient.
            bool: Returns False if the user decides to not select a patient.
        """
        patients_enum = enumerate(self.all_patients,start=1)
        patient_display_string = ""

        for index,patient in patients_enum:
                patient_display_string = patient_display_string + f"{index} - {patient.first_name} {patient.last_name}\n"
        
        while True:
            print("Select a patient from the following list by typing the respective number (OR type 0 to cancel)")
            print(patient_display_string)
            try:
                selection = int(input("Select one of the above: "))
                if selection == 0:
                    print("No patient has been chosen")
                    return False
                
                elif (0 < selection <= len(self.all_patients)):
                    selected_patient_object = self.all_patients[selection - 1]
                    print("You have selected patient: {0} {1}".format(selected_patient_object.first_name,selected_patient_object.last_name))
                    return selected_patient_object

                else:
                    print("Select a valid patient from the list. ")
                    continue

            except ValueError:
                print("Please enter a valid number: ")

        
    def add_patient_note(self):
        current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        patient_object = self.select_patient()
        if patient_object == False:
            print("Add patient note cancelled as no patient given")
            return False

        comments = input("Enter your desired comments: ")
        new_note = [current_time,comments,self.first_name + " " + self.last_name]

        patient_object.notes.append(new_note)


    def add_patient_condition(self):
        patient_object = self.select_patient()
        if patient_object == False:
            print("Add patient condition cancelled as no patient given")
            return False
        
        predefined_conditions = ['anxiety', 'autism', 'depression', 'bipolar disorder', 'OCD', 'PTSD']
        for condition in predefined_conditions:
            if condition in patient_object.conditions:
                predefined_conditions.remove(condition)
        self.display_conditions(predefined_conditions)

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

        patient_object.conditions.append(condition)
        print(f"Patient named {patient_object.first_name} {patient_object.last_name} has had the following condition added: {condition}")
        return 


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
