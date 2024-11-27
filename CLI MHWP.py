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
            mhwp1.cli_cancel_appointment()  # Trigger the cancel appointment functionality

        elif choice == "3":
            mhwp1.cli_confirm_appointment()  # Trigger the confirm appointment functionality

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