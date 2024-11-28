# MHWP logs in (here we simulate login)
print("Welcome to the Breeze Mental Health App")
username = input("Enter your username: ")
if username != mhwp1.name:
    print("Invalid username. Exiting.")
    return

print(f"Welcome {username}!")

# Main loop for interacting with the MHWP
while True:
    print("\nMain Menu:")
    print("1. View Calendar")
    print("2. Cancel Appointment")
    print("3. Confirm Appointment")
    print("4. Update Patient Health Record")
    print("5. Display Summary of All Patients")
    print("6. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        start_time = input("Enter start time (YYYY-MM-DD): ")
        end_time = input("Enter end time (YYYY-MM-DD): ")
        mhwp1.display_calendar(start_time, end_time)  # Display appointments within a time range

    elif choice == "2":
        # Handle canceling an appointment
        # User will enter a date/time to cancel an appointment
        date_time_str = input("Enter the appointment date/time (YYYY-MM-DD HH:MM): ")
        try:
            date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
            appointment = mhwp1.appointment_calendar.get(date_time, None)
            if appointment:
                mhwp1.cancel_appointment(appointment)  # Call cancel method for the appointment
            else:
                print("No appointment found at that time.")
        except ValueError:
            print("Invalid date/time format. Please use the format YYYY-MM-DD HH:MM.")

    elif choice == "3":
        # Handle confirming an appointment
        # User will enter a date/time to confirm an appointment
        date_time_str = input("Enter the appointment date/time (YYYY-MM-DD HH:MM): ")
        try:
            date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
            appointment = mhwp1.appointment_calendar.get(date_time, None)
            if appointment:
                mhwp1.confirm_appointment(appointment)  # Call confirm method for the appointment
            else:
                print("No appointment found at that time.")
        except ValueError:
            print("Invalid date/time format. Please use the format YYYY-MM-DD HH:MM.")

    elif choice == "4":
        patient_name = input("Enter patient's name to update health record: ")
        patient = next((p for p in [patient1] if p.name == patient_name), None)
        if patient:
            new_entry = input("Enter new health record entry: ")
            mhwp1.update_patient_health_record(patient, new_entry)
        else:
            print("Patient not found.")

    elif choice == "5":
        mhwp1.display_summary_of_all_patients()  # Display summary of all patients

    elif choice == "6":
        print("Exiting the system.")
        break

    else:
        print("Invalid option. Please try again.")
