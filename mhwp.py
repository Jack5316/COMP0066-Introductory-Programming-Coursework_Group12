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

    # Check in case a user is disabled
    def check_access(func):
        def wrapper(self, *args, **kwargs):
            if self.blocked:
                print(f"Access Denied: User {self.username} is disabled.")
                return None
            return func(self, *args, **kwargs)
        return wrapper
    
    # SET UNAVAILABLE TIME PERIOD E.G. HOLIDAYS
    @check_access
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

        # Mark the unavailable period
        if not hasattr(self, 'unavailable_periods'):
            self.unavailable_periods = []  # Initialize if not already present

        self.unavailable_periods.append((start_datetime, end_datetime))
        print(f"Unavailable period set from {start_date} to {end_date}.")
  
    @check_access
    def view_unavailable_periods(self):
        """View the existing unavailable periods."""
        if not self.unavailable_periods:
            print("No unavailable periods set.")
            return

        print("\nExisting Unavailable Periods:")
        for idx, (start, end) in enumerate(self.unavailable_periods, 1):
            print(f"{idx}. From {start.date()} to {end.date()}")

        while True:
            try:
                print("\nSelect a period to manage or enter 0 to go back to the main menu.")
                choice = int(input("Enter the number of the period (or 0 to go back): "))

                if choice == 0:
                    return   # Return to the main menu

                if 1 <= choice <= len(self.unavailable_periods):
                    selected_period = self.unavailable_periods[choice - 1]
                    self.manage_selected_period(choice - 1, selected_period)
                else:
                    print("Invalid choice. Please select a valid period number or 0 to go back.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    @check_access
    def manage_selected_period(self, period_index, period):
        """Manage a selected unavailable period."""
        while True:
            print(f"\nManaging Period: From {period[0].date()} to {period[1].date()}")
            print("1. Edit this period")
            print("2. Cancel this period")
            print("3. Go back to the period list")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.edit_unavailable_period(period_index)
                self.view_unavailable_periods()
                return  # Return to the period list after editing
            elif choice == "2":
                self.cancel_unavailable_period(period_index)
                # Check if no periods are left after cancellation
                if not self.unavailable_periods:
                    print("No unavailable periods set.")
                    return

                print("Remaining unavailable periods:")
                self.view_unavailable_periods()
                return
            elif choice == "3":
                return  # Go back to the period list
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")


    @check_access
    def edit_unavailable_period(self, period_index):
        """Edit a specific unavailable period."""
        try:
            start_date = input("Enter the new start date (YYYY-MM-DD): ")
            end_date = input("Enter the new end date (YYYY-MM-DD): ")
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())

            if start_datetime >= end_datetime:
                print("Error: Start date must be earlier than end date.")
                return

            self.unavailable_periods[period_index] = (start_datetime, end_datetime)
            print(f"Unavailable period updated to {start_date} to {end_date}.")
        except ValueError:
            print("Invalid date format. Please enter the dates in YYYY-MM-DD format.")

    @check_access
    def cancel_unavailable_period(self, period_index):
        """Cancel a specific unavailable period."""
        removed_period = self.unavailable_periods.pop(period_index)
        print(f"Unavailable period from {removed_period[0].date()} to {removed_period[1].date()} canceled.")

    @check_access
    def cli_set_unavailable_period(self):
        """Handle the CLI for managing unavailable periods."""
        while True:
            print("\nUnavailable Period Management:")
            print("1. View unavailable periods")
            print("2. Set a new unavailable period")
            print("3. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                self.view_unavailable_periods()
            elif choice == "2":
                try:
                    start_date = input("Enter the start date for the unavailable period (YYYY-MM-DD): ")
                    end_date = input("Enter the end date for the unavailable period (YYYY-MM-DD): ")
                    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                    self.set_unavailable_period(start_date, end_date)
                except ValueError:
                    print("Invalid date format. Please enter the dates in YYYY-MM-DD format.")
            elif choice == "3":
                print("Exiting Unavailable Period Management.")
                break
            else:
                print("Invalid choice. Please enter a number between 1, 2, and 5.")


    # DISPLAY CALENDAR
    @check_access
    def display_calendar(self, start_date, end_date):
        """ Display appointments scheduled within a given date range, including unavailable periods."""
                
        try:
            # Attempt to parse the input dates
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
            end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            print("Error: Invalid date format. Please enter dates in the format YYYY-MM-DD.")
            return

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
            print(f"No appointments scheduled between {start_date} and {end_date}.")


    # CONFIRM APPOINTMENT
    @check_access
    def confirm_appointment(self, appointment):
        """Confirm an appointment by updating its status."""
        if appointment.status == "confirmed":
            print(
                f"Appointment with {appointment.patientInstance.first_name} {appointment.patientInstance.last_name} is already confirmed.")
        else:
            appointment.confirm()  # Use the confirm method from the Appointment class
            print(
                f"Appointment with {appointment.patientInstance.first_name} {appointment.patientInstance.last_name} has been confirmed.")

    @check_access
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
            if appt.status == "requested" and
            (
                (isinstance(appt.date_time, str) and
                    start_date <= datetime.strptime(appt.date_time, "%Y-%m-%d %H:%M").date() <= end_date) or
                (isinstance(appt.date_time, datetime) and
                    start_date <= appt.date_time.date() <= end_date)
            )
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
    @check_access
    def cancel_appointment(self, appointment):
        """Cancel an appointment by updating its status."""
        if appointment.status == "cancelled":
            print(
                f"Appointment with {appointment.patientInstance.first_name} {appointment.patientInstance.last_name} is already cancelled.")
        else:
            appointment.cancel()  # Use the cancel method from the Appointment class
            print(
                f"Appointment with {appointment.patientInstance.first_name} {appointment.patientInstance.last_name} has been cancelled.")


    @check_access
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
            if appt.status == "confirmed" and
            (
                (isinstance(appt.date_time, str) and
                    start_date <= datetime.strptime(appt.date_time, "%Y-%m-%d %H:%M").date() <= end_date) or
                (isinstance(appt.date_time, datetime) and
                    start_date <= appt.date_time.date() <= end_date)
            )
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
    @check_access
    def view_requests(self):
        """Display enumerated appointments with the 'requested' status."""
        # Filter appointments with 'requested' status
        requested_appointments = [
            (time, appointment)
            for time, appointment in sorted(self.appointment_calendar.items())
            if appointment.status == "requested"
        ]
        return requested_appointments

    @check_access
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
    @check_access
    def export_appointments_to_ics(self, start_date, end_date):
        """
        Export the MHWP's confirmed appointments within the specified date range to an .ics file.
        """
        filename_prefix = f"{self.first_name}_{self.last_name}"
        print(f"Exporting {filename_prefix}'s calendar...")

        calendar_with_datetime = {}
        for date_time, appointment in self.patientCalendar.items():
            if isinstance(appointment.date_time, str):
                appointment.date_time = datetime.strptime(appointment.date_time, "%Y-%m-%d %H:%M")
            calendar_with_datetime[date_time] = appointment
        export_appointments_to_ics(self.appointment_calendar, start_date, end_date, filename_prefix, is_mhwp=True)

    @check_access
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


    @check_access
    def display_conditions(self, predefined_conditions):
        print("Please select a condition from the following list:")
        for i, condition in enumerate(predefined_conditions, start=1):
            print(f"{i} - {condition}")

    @check_access
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

    @check_access
    def add_patient_note(self):
        current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        patient_object = self.select_patient()
        if patient_object == False:
            print("Add patient note cancelled as no patient given")
            return False

        comments = input("Enter your desired comments: ")
        new_note = [current_time,comments,self.first_name + " " + self.last_name]

        patient_object.notes.append(new_note)


    @check_access
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


    @check_access
    def display_patients_with_moods(self):
        moods = {
            "Very Happy": "\033[32m",  # dark green
            "Happy": "\033[92m",  # light green
            "Positive Neutral": "\033[93m",  # yellow
            "Negative Neutral": "\033[33m",  # orange
            "Sad": "\033[31m",  # light red
            "Very Sad": "\033[91m"  # dark red
        }
        reset_color = "\033[0m"  # Reset color to default

        print("\n--- Patient Mood Tracker ---")
        print("-" * 30)

        if not self.all_patients:
            print("No patients found.")
            return

        for patient in self.all_patients:
            print(f"Patient: {patient.first_name} {patient.last_name}")
            if patient.mood:
                # Get the most recent mood entry
                latest_mood = patient.mood[-1]  # Format is [time, description, comments]
                mood_description = latest_mood[1]  # Get the mood description
                mood_color = moods.get(mood_description, reset_color)
                
                print(f"Latest Mood ({latest_mood[0]}):")
                print(f"{mood_color}{mood_description}{reset_color}")
                print(f"Comments: {latest_mood[2]}")
            else:
                print("No mood data recorded")
            print("-" * 30)

