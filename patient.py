from time import gmtime, strftime

from user import User
class Patient(User):
    def __init__(self,first_name,last_name,email,user_type,username,password, mhwpAsigned, emergencyEmail, colourCode):
        super().__init__(first_name,last_name,email,user_type,username,password)
        self.mhwpAsigned = mhwpAsigned
        self.mood = []
        self.journalEntries = []
        self.patientCalendar = []
        self.conditions = []
        self.notes = []
        self.emergencyEmail = emergencyEmail
        self.colourCode = colourCode

    def moodTracker(self):
        #LINK TO PRACTITIONER
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

        if appointmentDay < 10:
            appointmentDay = "0" + str(appointmentDay)
        if appointmentMonth < 10:
            appointmentMonth = "0" + str(appointmentMonth)

        
        return "{0}-{1}-{2}".format(appointmentYear,appointmentMonth,appointmentDay)

    def bookAppointment(self):
        # appointment assumptions 
        # every appointment is 1hr
        # could potentially change this to fetch dates within a range

        appointmentDate = Patient.getUserAppointmentDate()

        # UPDATE THIS TO USE THE ACTUAL CALENDAR
        mhwpCalendar = [] 

        # UPDATE THESE SO THAT THEY PULL FROM THE MHWP OBJECT
        # block out times outside the mhwp's Working hours
        mhwpStart = 9
        mhwpFinish = 17

        # check and see if user has appointments on the same day
        patientConflictingAppointments = []

        for datetime in self.patientCalendar:
            # this assumes that the the first entry is the actual time 
            # also need to remove the time part from datetime
            if datetime[0] == appointmentDate:
                patientConflictingAppointments.append(datetime[0])

        if patientConflictingAppointments:
            print("You already have the following appointments on the date {0}: ".format(appointmentDate))
            for appointment in patientConflictingAppointments:
                print(appointment)
        
        flag = True
        confirmation = False

        while flag and patientConflictingAppointments:
            # confirm if patient would still like to book an appointment 
            yes_no = {1:"Yes", 2: "No"}
            try:
                confirmation = int(input("Would you still like to book a new appointment for this day: {0}".format(yes_no)))
                if confirmation not in yes_no:
                    print("Please only enter 1 OR 2 depending on your selection.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")

        if confirmation and confirmation == 2:
            print("No appointment has been made")
            return 

        # filter MHWP calendar to get only appointments on date selected
        currentMHWPAppointments = []
        for datetime in mhwpCalendar:
            # this assumes that the first value is the appointment date 
            # also need to remove the time element of the string 
            if datetime[0] == appointmentDate:
                currentMHWPAppointments.append(datetime[0])
        
        # find potential times 
        potentialTimes = []
        while mhwpStart <= mhwpFinish:
            if mhwpStart not in currentMHWPAppointments:
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

        finalTime = "{0} {1}:00".format(appointmentDate,selectedTime)

        # CREATE THE APPOINTMENT IN THE FOLLOWING LINE 
        # newAppointment = Appointment()

        self.patientCalendar.append([finalTime,newAppointment])
        print("Appointment has been booked for the following time and date: [{0}]".format (finalTime))

    # allow to send short message to MHWP for reason of appointment
    # email update

    def cancelAppointment(self,appointmentInstance):
        appointmentInstance.cancel()
        # send email update 
        # cancelling an appointment should go into both patient and mhwp calendars and remove them 

    def getRecord(self):
        #LINK TO PRACTITIONER
        outputString = "{0} {1}".format(self.first_name,self.last_name)
        outputString += "-- Conditions --\n"
        # list all conditions
        for condition in self.conditions:
            outputString += "{0}\n".format(condition)
        
        outputString += "-- Notes --\n"
        # list all notes
        for indivdualNote in self.notes:
            outputString += ("{0} at {1}\n".format(indivdualNote[2],indivdualNote[0]))
            outputString += ("{0}".format(indivdualNote[1]))

        print(outputString)

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


# patient = Patient("hannah","zhao","h@gmail.com",user_type="patient",username="han",password="881",mhwpAsigned="drhannah",
#                   emergencyEmail="hannahzhao2@han.com",
#                   colourCode=None)


# patient.updateEmergencyContact()
# patient.searchExercises()
# patient.moodTracker()
# patient.journal()
# patient.bookAppointment()


# Each calendar object is: [YYYY-MM-DD HH:MM:SS]

# add mhwp name to each list in notes (so it is [time,commments,mhwp_name])

