from datetime import datetime, timedelta

#EXPORT CONFIRMED APPOINTMENTS TO CALENDAR

def export_appointments_to_ics(appointments, start_date, end_date, filename_prefix, is_mhwp=True):
    """
    Export appointments to an ICS file, filtering by status 'confirmed'.
    If no appointments are found, notify the user instead of creating an empty file.
    """
    # Filter appointments based on status and date range
    filtered_appointments = {
        date_time: appointment for date_time, appointment in appointments.items()
        if appointment.status == "confirmed" and start_date <= appointment.date_time.date() <= end_date
    }

    # If no appointments meet the criteria, notify and skip file creation
    if not filtered_appointments:
        print(f"No confirmed appointments to export for {filename_prefix} between {start_date} and {end_date}.")
        return

    # Format the filename based on the provided start and end dates
    filename = f"{filename_prefix}_calendar_{start_date}_{end_date}.ics"

    # Open the file for writing
    with open(filename, 'w') as ics_file:
        # Write the header for the ICS file
        ics_file.write("BEGIN:VCALENDAR\nVERSION:2.0\n")

        # Print the appointments in the calendar for debugging purposes
        print(f"Exporting appointments for {filename_prefix}:")
        for date_time, appointment in filtered_appointments.items():
            print(f"{date_time}: {appointment.patientInstance.first_name} {appointment.patientInstance.last_name} (Status: {appointment.status})")

            # Write each confirmed appointment as an event in the ICS file
            ics_file.write("BEGIN:VEVENT\n")

            if is_mhwp:
                # Export as MHWP: Use the patient's name in the summary
                summary = f"Appointment with {appointment.patientInstance.first_name} {appointment.patientInstance.last_name}"
            else:
                # Export as Patient: Use the MHWP's name in the summary
                summary = f"Appointment with {appointment.mhwpInstance.first_name} {appointment.mhwpInstance.last_name}"

            ics_file.write(f"SUMMARY:{summary}\n")
            ics_file.write(f"DTSTART:{appointment.date_time.strftime('%Y%m%dT%H%M%S')}\n")
            ics_file.write(f"DTEND:{(appointment.date_time + timedelta(hours=1)).strftime('%Y%m%dT%H%M%S')}\n")
            ics_file.write("END:VEVENT\n")

        # Write the footer for the ICS file
        ics_file.write("END:VCALENDAR")

    # Print a confirmation message
    print(f"Appointments exported to {filename}")

