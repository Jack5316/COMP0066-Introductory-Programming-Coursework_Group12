from time import gmtime, strftime
from user import User
from datetime import datetime, timedelta
from utils import export_appointments_to_ics
from operator import itemgetter


class Patient(User):
    def __init__(self,first_name,last_name,email,user_type,username,password, mhwpAsigned, emergencyEmail, colourCode):
        super().__init__(first_name,last_name,email,user_type,username,password)
        self.mhwpAsigned = mhwpAsigned
        self.mood = []
        self.journalEntries = []
        self.patientCalendar = {}   # each calendar entry is: {"YYYY-MM-DD HH:MM" : appointmentObject}
        self.conditions = []
        self.notes = []     # each notes entry is in form [time,commments,mhwp_name]
        self.emergencyEmail = emergencyEmail
        self.colourCode = colourCode
        mhwpAsigned.all_patients.append(self)

    def moodTracker(self):
        moods = {"Dark Green": "Very Happy", 
                 "Light Green": "Happy", 
                 "Yellow":"Positive Neutral", 
                "Orange":"Negative Neutral", 
                "Light Red":"Sad", 
                "Dark Red":"Very Sad"}
        
        moodColours = {1: ("\033[32m1", "Dark Green"), 
            2: ("\033[92m2", "Light Green"), 
            3: ("\033[93m3", "Yellow"), 
            4: ("\033[33m4", "Orange"), 
            5: ("\033[31m5", "Light Red"),  
            6: ("\033[91m6", "Dark Red")}
        
        reset_color = "\033[0m"
        
        #arrow colour scale
        print("\nMood Scale:")
        print(f"\033[92m<{'-' * 15}\033[93m{'-' * 15}\033[91m{'-' * 15}>{reset_color}")
        print(f"\033[92mPositive {' ' * 10}\033[93mNeutral {' ' * 10}\033[91mNegative{reset_color}")
        
        while True:
            try:
                print("\nMood Options:")
                for i, (number, colourName) in moodColours.items():
                    print(f"{number}", end=" ")
                    
                colourCode = int(input(f"\033[0m\n\nPlease input the number that matches your mood colour (1-6): "))
                if colourCode not in moodColours:
                    print("Please enter a valid option, 1-6.")
                else:
                    _, colourName = moodColours[colourCode]
                    moodDescription = moods[colourName]
                    comment=input("Please add any comments about your mood: ")
                    break

            except ValueError:
                print("Please enter a valid option, 1-6.")

        timeStamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        # moodEntry format: [time, description, comments]
        moodEntry = [timeStamp,moodDescription,comment]
        self.mood.append(moodEntry)
        print("\n--- Mood Entry Added ---")
        print("Date/Time:", moodEntry[0])
        print("Mood:", moodEntry[1])
        print("Comments:", moodEntry[2])

    def journal(self):
        journalText=input("Please input your journal text: ")
        timeStamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        journalEntry={"Date/Time": timeStamp, "Journal Entry": journalText}
        self.journalEntries.append(journalEntry)

        print(("\n--- Journal Entry Added ---"))
        for key, value in journalEntry.items():
            print(f"{key}: {value}")

    def updateEmail(self):
        while True:
            try:
                new_email = input("Please enter your new email (or type 0 to exit): ").strip()
                if new_email == '0':
                    print("Exiting without updating details.")
                    break
                self.update_email(new_email)
                print("Email updated successfully.")
                break
            except ValueError as e:
                print(f"Error: {e}")
            
    def updateEmergencyContact(self):
        while True:
            try:
                updatedEmergencyEmail = input("Please enter your updated emergency email (or type 0 to exit): ")
                if updatedEmergencyEmail == '0':
                    print("Exiting without updating details.")
                    break
                User.email_validate(updatedEmergencyEmail)
                self.emergencyEmail = updatedEmergencyEmail
                print("Emergency email updated successfully.")
                break
            except ValueError as e:
                print(f"Error: {e}")

    @staticmethod
    def getUserAppointmentDate():
        currentYear = int(strftime("%Y", gmtime()))
        currentMonth = int(strftime("%m", gmtime()))
        currentDay = int(strftime("%d", gmtime()))
        print("Would you like to book the appointment for the current year [{0}] or the next year [{1}]".format(currentYear,(currentYear+1)))
        while True:
            try:
                appointmentYear = int(input("Enter either:\n 1 - Current Year [{0}] \n 2 - Next Year [{1}] \n".format(currentYear,(currentYear+1))))
                if appointmentYear == 1:
                    appointmentYear = currentYear
                    break
                elif appointmentYear == 2:
                    appointmentYear = currentYear + 1
                    break
            except ValueError:
                print("Please enter a valid number")
    
        allMonths = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

        # if user wants an appointment this year then only show the relevant months
        if appointmentYear == currentYear:
            inputMonthText = ""
            for key in allMonths.keys():
                if key >= currentMonth:
                    inputMonthText = inputMonthText + " " + str(key) + " - " + allMonths[key] + "\n"

        # if appointment year is next year then just show all months
        else:
            inputMonthText = ""
            for key in allMonths.keys():
                inputMonthText = inputMonthText + str(key) + " - " + allMonths[key] + "\n"


        print("Enter the month you would like to book the appointment for: ")
        while True:
            try:
                appointmentMonth = int(input(inputMonthText))
                if not (1 <= appointmentMonth <= 12):
                    print("Enter a valid number between 1 and 12.")
                    continue

                if currentYear == appointmentYear and appointmentMonth < currentMonth:
                    print("Enter a valid month in the future.")
                    continue
                    
                break

            except ValueError:
                print("Please enter a valid number: ")
        
        
        daysInMonth = {1: 31,2: 28,3: 31,4: 30,5: 31,6: 30,7: 31,8: 31,9: 30,10: 31,11: 30,12: 31}
        leapFlag = False
        # check for leap year
        if appointmentYear % 4 == 0 and (appointmentYear % 100 != 0 or appointmentYear % 400 == 0):
            leapFlag = True
        
        # get number of days in month
        daysInSelectedMonth = daysInMonth[appointmentMonth]
        if leapFlag and appointmentMonth == 2:
            daysInSelectedMonth += 1 
        
        # if user is booking an appointment for the same month then only show them today onwards
        sameMonth = False
        if currentMonth == appointmentMonth and currentYear == appointmentYear:
            sameMonth = True
        earliestDay = 1
        if sameMonth:
            earliestDay = currentDay

        # collect day from user
        while True:
            try:
                appointmentDay = int(input("Enter the desired date of your appointment [{0} - {1}]:\n".format(earliestDay,daysInSelectedMonth)))
                if not (earliestDay <= appointmentDay <= daysInSelectedMonth):
                    print("Enter a valid number between {0} and {1}.".format(earliestDay,daysInSelectedMonth))
                    continue
                break
            except ValueError:
                print("Please enter a valid number. ")

        appointmentDate = datetime(appointmentYear, appointmentMonth, appointmentDay)
        return appointmentDate

    def bookAppointment(self):
        """
        Returns the time a patient wants an appointment for. No input paramaters required.
        Checks the calendar of the MHWP for any conflicts.
        Also ensures the desired date is in the future.

        Returns:
        str: The finalized appointment datetime in the format 
            "YYYY-MM-DD HH:00", OR False if no appointment is booked.
        """
        appointmentDate = Patient.getUserAppointmentDate()

        for start, end in self.mhwpAsigned.unavailable_periods:
            if start.date() <= appointmentDate.date() <= end.date():
                print(f"Sorry, your MHWP is unavailable on {appointmentDate.date()} due to a scheduled holiday.")
                return False
            
        # pull out working hours of mhwp
        mhwpStart = self.mhwpAsigned.working_hours["start"].split(":")[0]
        mhwpStart = int(mhwpStart)
        mhwpFinish = self.mhwpAsigned.working_hours["end"].split(":")[0]
        mhwpFinish = int(mhwpFinish)

        # check and see if user has appointments on the same day
        patientConflictingAppointments = []

        for appointmentDatetime in self.patientCalendar.keys():
            # remove the time part from datetime
            # convert to each one to a datetime object in format (YYYY-MM-DD)
            if appointmentDatetime.date() == appointmentDate.date():
                patientConflictingAppointments.append(appointmentDatetime)

        if patientConflictingAppointments:
            print("You already have the following appointments on the date {0}: ".format(datetime.strftime(appointmentDate,"%Y-%m-%d")))
            for appointment in patientConflictingAppointments:
                print(appointment)
        
        flag = True
        confirmation = False

        while flag and patientConflictingAppointments:
            # confirm if patient would still like to book an appointment 
            yes_no = {1:"Yes", 2: "No"}
            print("Would you still like to book a new appointment for this day:")
            try:
                for key, value in yes_no.items():
                    print("{0} - {1}".format(key,value))
                confirmation = int(input("Enter your choice: "))
                if confirmation not in yes_no:
                    print("Please only enter 1 OR 2 depending on your selection.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")

        if confirmation and confirmation == 2:
            print("No appointment has been made")
            return False

        mhwpCalendar = self.mhwpAsigned.appointment_calendar 
    
        # filter MHWP calendar to get only appointments on date selected
        currentMHWPAppointments = []
        for mhwpDatetime in mhwpCalendar.keys():
            # split the MHWP datetime string into the date and time 
            if mhwpDatetime.date() == appointmentDate.date():
                # Extract the hour from the datetime object and append it to the list
                currentMHWPAppointments.append(mhwpDatetime.hour)
        
        

      
        # find potential times based on MHWP calendar
        potentialTimes = []
        while mhwpStart < mhwpFinish:
            appointmentTime = datetime.combine(appointmentDate, datetime.min.time()) + timedelta(hours=mhwpStart)
            if (
                mhwpStart not in currentMHWPAppointments and
                all(not (start <= appointmentTime <= end) for start, end in self.mhwpAsigned.unavailable_periods)
            ):
                potentialTimes.append(mhwpStart)
            mhwpStart += 1
        
        # show user potential times and get input 
        enumPotentialTimes = list(enumerate(potentialTimes,1))
        print("Available times are: ")
        for index,time in enumPotentialTimes:
            print(str(index) + " - " + str(time)+":00")
        
        while True:
            try:
                selectedTime = int(input("Select one of the available times: \n"))
                if 1 <= selectedTime <= len(potentialTimes):
                    selectedTime = enumPotentialTimes[(selectedTime - 1)][1]
                    print("You have selected the time: {0}:00".format(selectedTime))
                    break 
                else:
                    print("Please select a valid option from the list.")    
            except ValueError:
                print("Please enter a valid integer ")
        
        if selectedTime < 10:
            selectedTime = "0" + str(selectedTime) 

        appointmentDate = datetime.strftime(appointmentDate,"%Y-%m-%d")
        finalDateTime = "{0} {1}:00".format(appointmentDate,selectedTime)

        # import the appointment class here otherwise issue due to circular imports
        from appointment import Appointment
        Appointment(self,self.mhwpAsigned,finalDateTime)

        print("Appointment has been requested for the following time and date:\n{0}".format (finalDateTime))
        return finalDateTime
    
    # allow to send short message to MHWP for reason of appointment
    # email update

    def bookSoonestAppointment(self):
        # automatically books the soonest available appointment starting from the next day.
        currentDate = datetime.now().date()
        nextDay = currentDate + timedelta(days=1)
        mhwpStart = int(self.mhwpAsigned.working_hours["start"].split(":")[0])
        mhwpFinish = int(self.mhwpAsigned.working_hours["end"].split(":")[0])

        while True:
            # check if the nextDay is within an unavailable period
            for start, end in self.mhwpAsigned.unavailable_periods:
                if start.date() <= nextDay <= end.date():
                    nextDay += timedelta(days=1)
                    break
            else:
                # check for available slots on this day
                currentMHWPAppointments = []
                for mhwpDatetime in self.mhwpAsigned.appointment_calendar.keys():
                    if mhwpDatetime.date() == nextDay:
                        currentMHWPAppointments.append(mhwpDatetime.hour)
                        
                patientConflictingAppointments = []
                for appointmentDatetime in self.patientCalendar.keys():
                    if appointmentDatetime.date() == nextDay:
                        patientConflictingAppointments.append(appointmentDatetime)

                if patientConflictingAppointments:
                    print("You already have the following appointments on the date {0}:".format(nextDay.strftime("%Y-%m-%d")))
                    for appointment in patientConflictingAppointments:
                        print(appointment)

                potentialTimes = []
                for hour in range(mhwpStart, mhwpFinish):
                    appointmentTime = datetime.combine(nextDay, datetime.min.time()) + timedelta(hours=hour)
                    if (
                        hour not in currentMHWPAppointments and
                        all(not (start <= appointmentTime <= end) for start, end in self.mhwpAsigned.unavailable_periods)
                    ):
                        potentialTimes.append(hour)

                if potentialTimes:
                    selectedTime = potentialTimes[0]
                    appointmentDateTime = datetime.combine(nextDay, datetime.min.time()) + timedelta(hours=selectedTime)
                    print(f"Suggested soonest appointment: {appointmentDateTime.strftime('%Y-%m-%d %H:%M')}")

                    flag = True
                    confirmation = False
                    yes_no = {1: "Yes", 2: "No"}

                    while flag:
                        print("Would you like to confirm this appointment?")
                        try:
                            for key, value in yes_no.items():
                                print(f"{key} - {value}")
                            confirmation = int(input("Enter your choice: "))
                            if confirmation not in yes_no:
                                print("Please only enter 1 or 2.")
                                continue
                            break
                        except ValueError:
                            print("Please enter a valid number.")

                    if confirmation == 2:
                        print("No appointment has been made.")
                        return False

                    appointmentDate = nextDay.strftime("%Y-%m-%d")
                    finalDateTime = f"{appointmentDate} {selectedTime:02d}:00"
                    from appointment import Appointment
                    Appointment(self,self.mhwpAsigned,finalDateTime)
                    print(f"Appointment has been requested for the following time and date: \n{finalDateTime}.")
                    return finalDateTime
                else:
                    nextDay += timedelta(days=1)
                   
    def emergencyAppointment(self):
        #Allows the patient to book an emergency appointment on the same day.
        currentDate = datetime.now().date()
        currentTime = datetime.now().time()
        mhwpStart = int(self.mhwpAsigned.working_hours["start"].split(":")[0])
        mhwpFinish = int(self.mhwpAsigned.working_hours["end"].split(":")[0])

        print("This is an emergency booking. If it is a medical emergency, please call 999.")

        # Get already booked appointments for today
        mhwpAppointments = []
        for datetime_obj in self.mhwpAsigned.appointment_calendar.keys():
            if datetime_obj.date() == currentDate and datetime_obj.time() > currentTime:
                mhwpAppointments.append(datetime_obj.hour)

        # check available slots for the remainder of the day
        availableTimes = []
        for hour in range(mhwpStart, mhwpFinish):
            appointmentTime = datetime.combine(currentDate, datetime.min.time()) + timedelta(hours=hour)
            if (
                appointmentTime.time() > currentTime and
                hour not in mhwpAppointments and
                all(not (start <= appointmentTime <= end) for start, end in self.mhwpAsigned.unavailable_periods)
            ):
                availableTimes.append(hour)

        if not availableTimes:
            print("No emergency slots are available today.")
            return False
        
        print("Available emergency appointment times today:")
        enumAvailableTimes = list(enumerate(availableTimes, start=1))
        for index, hour in enumAvailableTimes:
            print(f"{index}. {hour:02d}:00")

        while True:
            try:
                choice = int(input("Select a time by entering the corresponding number: "))
                if 1 <= choice <= len(availableTimes):
                    selectedTime = enumAvailableTimes[choice - 1][1]
                    appointmentDateTime = datetime.combine(currentDate, datetime.min.time()) + timedelta(hours=selectedTime)
                    print(f"Selected emergency appointment: {appointmentDateTime.strftime('%Y-%m-%d %H:%M')}")

                    flag = True
                    confirmation = False
                    yes_no = {1: "Yes", 2: "No"}

                    while flag:
                        print("Would you like to confirm this appointment?")
                        try:
                            for key, value in yes_no.items():
                                print(f"{key} - {value}")
                            confirmation = int(input("Enter your choice: "))
                            if confirmation not in yes_no:
                                print("Please only enter 1 or 2.")
                                continue
                            break
                        except ValueError:
                            print("Please enter a valid number.")

                    if confirmation == 2:
                        print("No appointment has been made.")
                        return False

                    appointmentDate = currentDate.strftime("%Y-%m-%d")
                    finalDateTime = f"{appointmentDate} {selectedTime:02d}:00"
                    from appointment import Appointment
                    Appointment(self,self.mhwpAsigned,finalDateTime)
                    print(f"Emergency appointment has been requested for the following time and date: \n{finalDateTime}.")
                    return finalDateTime
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(availableTimes)}.")
            except ValueError:
                print("Please enter a valid number.")
    
    def cancelAppointment(self):
        if not self.patientCalendar:
            print("\n--- No appointments found ---")
            return
        print("\nYour appointments:")
        appointments = list(self.patientCalendar.items())
        for idx, (datetime_obj, appointment) in enumerate(self.patientCalendar.items(), 1):
            date_str = datetime_obj.strftime("%Y-%m-%d")
            time_str = datetime_obj.strftime("%H:%M")
            print(f"{idx}. Appointment on [{date_str}] at time [{time_str}] "
            f"with practitioner: {appointment.mhwpInstance.first_name} {appointment.mhwpInstance.last_name}")

        print(f"{len(appointments) + 1}. Return to Patient Menu")
        while True:
            try:
                choice = int(input(f"\nSelect appointment to cancel (1-{len(appointments) + 1}): "))
                if 1 <= choice <= len(appointments):
                    appointmentInstance = appointments[choice - 1][1]
                    appointmentInstance.cancel()
                    break
                elif choice == len(appointments) + 1:
                    print("Returning to Patient Menu...")
                    break
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(appointments) + 1}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def getRecord(self):
        outputString = "{0} {1}".format(self.first_name,self.last_name)
        outputString += "-- Conditions --\n"
        # list all conditions
        for condition in self.conditions:
            outputString += "{0}\n".format(condition)
        
        outputString += "-- Notes --\n"
        # list all notes
        # note format is:  [ [time,commments,mhwp_name] , ... ]
        for indivdualNote in self.notes:
            outputString += ("{0} at {1}\n".format(indivdualNote[2],indivdualNote[0]))
            outputString += ("{0}".format(indivdualNote[1]))

        print(outputString)

    def displayAllAppointments(self):
        if not self.patientCalendar:
            print("\n--- No appointments found ---")
            return
        print("\n--- All Appointments ---")
        for key, appointmentObject in self.patientCalendar.items():
            date_str = key.strftime("%Y-%m-%d")
            time_str = key.strftime("%H:%M")
            print(f"Appointment on [{date_str}] at time [{time_str}] with practitioner: {appointmentObject.mhwpInstance.first_name} {appointmentObject.mhwpInstance.last_name}")


    @classmethod
    def searchExercises(cls):
        while True:
            search = input("\nPlease enter your search term or type '0' to quit: ")
            exercises={"Mindfulness": "https://drive.google.com/file/d/19spOJz71lzbZiX5CDX7L-YNXrQutJPJX/view",
                       "Meditation": "https://drive.google.com/file/d/1dcsW9byG8G4Gyb1hFvtFS27LnrBdfvDA/view?usp=sharing",
                       "Breathing": "https://drive.google.com/file/d/19cCxG03o26RJB57g4xMUdyoDQlvaK8vS/view?usp=sharing",
                       "Sleep": "https://insighttimer.com/glennharrold/guided-meditations/relax-and-sleep-well",
                       "Anxiety": "https://insighttimer.com/andreawachter/guided-meditations/decrease-anxiety-and-increase-peace",
                       "Healing": "https://insighttimer.com/davidji/guided-meditations/deep-healing"}

            if search == '0':
                break
            else:
                for key, value in exercises.items():
                    if key.lower()==search.lower():
                        print(f"This resource matches your search term, {key.lower()}: {value}.")
                        break
                else:
                    print("Sorry, we could not find any resources to match your search term. Some suggestions are 'mindfulness' or 'meditation'.")


    def export_appointments_to_ics(self, start_date, end_date):
        """
        Export the patient's confirmed appointments  within the specified date range to an .ics file.
        """
        filename_prefix = f"{self.first_name}_{self.last_name}"
        print(f"Exporting {filename_prefix}'s calendar...")

        calendar_with_datetime = {}
        for date_time, appointment in self.patientCalendar.items():
            if isinstance(appointment.date_time, str):
                appointment.date_time = datetime.strptime(appointment.date_time, "%Y-%m-%d %H:%M")
            calendar_with_datetime[date_time] = appointment
        export_appointments_to_ics(self.patientCalendar, start_date, end_date, filename_prefix, is_mhwp=False)

    # EXPORT APPOINTMENTS TO CALENDAR
    def cli_export_appointments(self):
        """
        CLI for exporting Patient's appointments to an ICS file.
        """
        print("Exporting Patient's appointments to ICS file.")
        start_date_str = input("Enter start date (YYYY-MM-DD): ")
        end_date_str = input("Enter end date (YYYY-MM-DD): ")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            # Call export function
            export_appointments_to_ics(self.patientCalendar, start_date, end_date,
                                       f"{self.first_name}_{self.last_name}", is_mhwp=False)

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


    def show_all_journal_entries(self):
        if not self.journalEntries:
            print("No journal entries found.")
        else:
            print("\n--- All Journal Entries ---")
            for jour_entry in self.journalEntries:
                print("Date/Time:", jour_entry["Date/Time"])
                print("Journal Entry:", jour_entry["Journal Entry"])
                print("---")
    
    def search_journal_entries(self):

        # take a input of a keyword
        # rank all journal entries on the amount of times the keyword comes up
        # show top 3 journal entries (if there are 3) with most occurences of keyword
        # display the number of keyword occurences with each journal entry above

        if not self.journalEntries:
            print("No journal entries found.")
            return 
        
        while True:
            keyword = input("Enter the keyword/phrase you would like to search by (or type 0 to exit): ")

            if keyword == "0":
                print("Cancelling the journal search")
                return False
            
            if len(keyword.split(" ")) > 1:
                print("Please only enter one word with no spaces.")
                continue 

            break 
        
        occurence_index = [] 
        lowercase_keyword = keyword.lower()

        for entry in self.journalEntries:
            journal_text = entry["Journal Entry"]
            all_words_in_text = journal_text.lower().split()
            word_count = all_words_in_text.count(lowercase_keyword)

            if word_count > 0:
                occurence_index.append((word_count, entry))
        
        if len(occurence_index) == 0:
            print("No journal entries found with keyword {0}".format(keyword))
            return False

        number = 3
        if len(occurence_index) < 3:
            number = len(occurence_index)

        occurence_index.sort(key=itemgetter(0), reverse=True)

        best_matches = occurence_index[:number]

        if number != 3:
            if number == 1:
                print(f"Only journal entry containing '{keyword}':")
            else:
                print(f"Only {number} journal entries containing '{keyword}':")
        else:
            print(f"Top 3 journal entries containing '{keyword}':")
            
        for count, entry in best_matches:
            print("Date/Time:", entry["Date/Time"])
            print("Journal Entry:", entry["Journal Entry"])
            print(f"Occurrences of '{keyword}': {count}")
            print("---")

