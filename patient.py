from time import gmtime, strftime
from user import User
from datetime import datetime, timedelta
from utils import export_appointments_to_ics


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

    def moodTracker(self):
        moods = {"Dark Green": "Very Happy", "Light Green": "Happy", "Yellow":"Positive Neutral", "Orange":"Negative Neutral", "Light Red":"Sad", "Dark Red":"Very Sad"}
        moodColours = {1:"Dark Green", 2:"Light Green", 3:"Yellow", 4:"Orange", 5:"Light Red", 6:"Dark Red"}

        while True:
            try:
                colourCode = int(input(f"Please input the number that matches your mood colour: {moodColours}: "))
                if colourCode not in moodColours:
                    print("Please enter a valid option, 1-6.")
                else:
                    colourValue = moodColours[colourCode]
                    moodDescription = moods[colourValue]
                    comment=input("Please add any comments about your mood: ")
                    break

            except ValueError:
                print("Please enter a valid option, 1-6.")

        timeStamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        # moodEntry format: [time, description, comments]
        moodEntry = [timeStamp,moodDescription,comment]
        self.mood.append(moodEntry)
        print("Mood entry added:")
        print("Date/Time:", moodEntry[0])
        print("Mood:", moodEntry[1])
        print("Comments:", moodEntry[2])

    def journal(self):
        journalText=input("Please input your journal text: ")
        timeStamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        journalEntry={"Date/Time": timeStamp, "Journal Entry": journalText}
        self.journalEntries.append(journalEntry)

        print("Journal entry added:")
        for key, value in journalEntry.items():
            print(f"{key}: {value}")

    def updateEmergencyContact(self):
        while True:
            updatedEmergencyEmail = input("Please enter your updated emergency email or type 'EXIT' to quit: ")
            if updatedEmergencyEmail.upper() == 'EXIT':
                print("Exiting without updating details.")
                break
            else:
                self.emergencyEmail=updatedEmergencyEmail
                print("Your details have been successfuly updated.")
                break

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
            currentAppointmentOccurence = appointmentDatetime.split(" ")[0]
            if currentAppointmentOccurence == datetime.strftime(appointmentDate,"%Y-%m-%d"):
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
            currentAppointmentOccurence = mhwpDatetime.split(" ")
            if currentAppointmentOccurence[0] == datetime.strftime(appointmentDate,"%Y-%m-%d"):
                # append the taken time to list IF the date is the same
                currentMHWPAppointments.append(int(currentAppointmentOccurence[1].split(":")[0]))
      
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
        print("Avaliable times are: ")
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
                    currentAppointmentOccurrence = mhwpDatetime.split(" ")[0]
                    if currentAppointmentOccurrence == nextDay.strftime("%Y-%m-%d"):
                        currentMHWPAppointments.append(int(mhwpDatetime.split(" ")[1].split(":")[0]))
                patientConflictingAppointments = []
                for appointmentDatetime in self.patientCalendar.keys():
                    currentAppointmentOccurrence = appointmentDatetime.split(" ")[0]
                    if currentAppointmentOccurrence == nextDay.strftime("%Y-%m-%d"):
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
                    print(f"Appointment successfully booked for {finalDateTime}.")
                    return finalDateTime
                else:
                    nextDay += timedelta(days=1)
                   
    def emergencyAppointment(self):
        """
        Allows the patient to book an emergency appointment on the same day.
        The user is prompted to select a time and confirm the appointment.
        """
        currentDate = datetime.now().date()
        currentTime = datetime.now().time()
        mhwpStart = int(self.mhwpAsigned.working_hours["start"].split(":")[0])
        mhwpFinish = int(self.mhwpAsigned.working_hours["end"].split(":")[0])

        print("This is an emergency booking. If it is a medical emergency, please call 999.")

        # check available slots for the remainder of the day
        potentialTimes = []
        for hour in range(mhwpStart, mhwpFinish):
            appointmentTime = datetime.combine(currentDate, datetime.min.time()) + timedelta(hours=hour)
            if (
                appointmentTime.time() > currentTime and
                all(not (start <= appointmentTime <= end) for start, end in self.mhwpAsigned.unavailable_periods)
            ):
                potentialTimes.append(hour)

        if not potentialTimes:
            print("No emergency slots are available today.")
            return False
        
        mhwpAppointments = self.mhwpAsigned.appointment_calendar.keys()
        availableTimes = []
        for time in potentialTimes:
            appointmentTime = datetime.combine(currentDate, datetime.min.time()) + timedelta(hours=time)
            formattedTime = appointmentTime.strftime("%Y-%m-%d %H:%M")
    
            if formattedTime not in mhwpAppointments:
                availableTimes.append(time)

        
        print("Available emergency appointment times today:")
        for index, hour in enumerate(potentialTimes, start=1):
            print(f"{index}. {hour:02d}:00")

        while True:
            try:
                choice = int(input("Select a time by entering the corresponding number: "))
                if 1 <= choice <= len(potentialTimes):
                    selectedTime = potentialTimes[choice - 1]
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
                    print(f"Emergency appointment successfully booked for {finalDateTime}.")
                    return finalDateTime
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(potentialTimes)}.")
            except ValueError:
                print("Please enter a valid number.")
    
    def cancelAppointment(self,appointmentInstance):
        appointmentInstance.cancel()
        # send email update 
        # cancelling an appointment should go into both patient and mhwp calendars and remove them 

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
        for key in self.patientCalendar.keys():
            splitTime = key.split(" ")
            appointmentObject = self.patientCalendar[key]
            print("Appointment on [{0}] at time [{1}] with practitioner: {2} {3}".format(splitTime[0],splitTime[1],appointmentObject.mhwpInstance.first_name,appointmentObject.mhwpInstance.last_name))

    @classmethod
    def searchExercises(cls):
        while True:
            search = input("Please enter your search term or type 'EXIT' to quit: ")
            exercises={"Mindfulness": "https://drive.google.com/file/d/19spOJz71lzbZiX5CDX7L-YNXrQutJPJX/view",
                       "Meditation": "https://drive.google.com/file/d/1dcsW9byG8G4Gyb1hFvtFS27LnrBdfvDA/view?usp=sharing",
                       "Breathing": "https://drive.google.com/file/d/19cCxG03o26RJB57g4xMUdyoDQlvaK8vS/view?usp=sharing",
                       "Sleep": "https://insighttimer.com/glennharrold/guided-meditations/relax-and-sleep-well",
                       "Anxiety": "https://insighttimer.com/andreawachter/guided-meditations/decrease-anxiety-and-increase-peace",
                       "Healing": "https://insighttimer.com/davidji/guided-meditations/deep-healing"}

            if search.upper() == 'EXIT':
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
                  

def cli_book_appointment(patient):
        # CLI to handle different types of appointment booking: regular, soonest, or emergency.

            print("\n--- Appointment Booking ---")
            print("1. Book a Regular Appointment")
            print("2. Book the Soonest Available Appointment")
            print("3. Book an Emergency Appointment")
            print("4. Return to Main Menu")
            
            while True:
                try:
                    choice = int(input("Enter your choice (1-4): "))
                    if choice == 1:
                        print("\n--- Booking a Regular Appointment ---")
                        appointment_time = patient.bookAppointment()
                        if appointment_time:
                            print(f"Appointment successfully requested for {appointment_time}.")
                        break
                    elif choice == 2:
                        print("\n--- Booking the Soonest Available Appointment ---")
                        appointment_time = patient.bookSoonestAppointment()
                        if appointment_time:
                            print(f"Successfully booked the soonest appointment for {appointment_time}.")
                        break
                    elif choice == 3:
                        print("\n--- Booking an Emergency Appointment ---")
                        appointment_time = patient.emergencyAppointment()
                        if appointment_time:
                            print(f"Successfully booked an emergency appointment for {appointment_time}.")
                        break
                    elif choice == 4:
                        print("Returning to Patient Menu...")
                        break
                    else:
                        print("Invalid choice. Please select a number between 1 and 4.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")