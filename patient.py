from time import gmtime, strftime

import user

class Patient(user.User):
    def __init__(self,first_name,last_name,email,user_type,username,password, mhwpAsigned, emergencyEmail, colourCode):
        user.User.__init__(self,first_name,last_name,email,user_type,username,password)
        self.mhwpAsigned = mhwpAsigned
        self.mood = []
        self.journalEntries = []
        self.patientCalendar = []
        self.conditions = []
        self.notes = []
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
            except:
                print("Please enter a valid number")
    
        allMonths = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

        # if user wants an appointment this year then only show the relevant months
        if appointmentYear == currentYear:
            inputMonthText = ""
            for key in allMonths.keys():
                if key >= currentMonth:
                    inputMonthText = inputMonthText + str(key) + " - " + allMonths[key] + "\n"

        # if appointment year is next year then just show all months
        else:
            inputMonthText = ""
            for key in allMonths.keys():
                inputMonthText = inputMonthText + str(key) + " - " + allMonths[key] + "\n"
                
        print("Enter the month you would like to book the appointment for: ")

        # below you get stuck into an infinite loop when using the next year 
        # may be best to redesign how this works cause it is very confusing to read 
        while True:
            try:
                appointmentMonth = int(input(inputMonthText))
                if appointmentMonth > 12 or appointmentMonth < 1:
                    print("Enter a valid number: ")
                elif appointmentMonth >= currentMonth and currentYear == appointmentYear:
                    break
                else:
                    while appointmentMonth < currentMonth and currentYear == appointmentYear:
                        print("Enter a valid month in the future: ")
                        appointmentMonth = int(input(inputMonthText))
                        if appointmentMonth >= currentMonth and currentYear == appointmentYear:
                            break

            except:
                print("Please enter a valid number: ")

        return appointmentYear



    def bookAppointment(self):
        # appointment assumptions 
        # every appointment is 30 mins (could add in varying appointment times, i.e. 15mins, 30mins, 45mins, 1hr)
        # each one begins at the time specified 
        # if doing this then include the appointment length in the appointment object

        # could potentially change this to fetch dates within a range
    
        answer = patient.getUserAppointmentDate()
        print(answer)


        appointmentDate = input("Please enter the date you want to view availability (YYYY-MM-DD): ")
        
        # when getting date input check for leap years and the days in the month 


        # need to do error checking to make sure a valid date has been inputted
        # also check and make sure the appointment is reasonable 


        # for now just use a hardcoded calendar
        # UPDATE THIS TO USE THE ACTUAL CALENDAR
        mhwpCalendar = [] 

        patientConflictingAppointments = []

        for datetime in self.patientCalendar:
            # this assumes that the the first entry is the actual time 
            # also need to remove the time part from datetime
            if datetime[0] == appointmentDate:
                patientConflictingAppointments.append(datetime[0])

        if patientConflictingAppointments:
            print("You already have the following appointments on the date {0}".format(appointmentDate))
            for appointment in patientConflictingAppointments:
                print(appointment)
        
        flag = True
        while flag:
            # confirm if patient would still like to book an appointment 
            yes_no = {1:"Yes", 2: "No"}
            try:
                confirmation = int(input("Would you still like to book a new appointment: {0}".format(yes_no)))
                if confirmation not in yes_no:
                    print("Please only enter 1 OR 2 depending on your selection.")
                else:
                    flag = False
            except ValueError:
                print("Please enter a valid number.")

        # filter MHWP calendar to get only appointments on date selected
        potentialDates = []
        for datetime in mhwpCalendar:

            # this assumes that the first value is the appointment date 
            # also need to remove the time element of the string 
            if datetime[0] == appointmentDate and datetime[0] not in patientConflictingAppointments:
                potentialDates.append(datetime[0])
        


        # need to check for availability of patient 
        # 

        pass
    #selection done on MHWP'S calendar
    #option for day or week view
    # booked appointment needs to be confirmed by MHWP
    #allow to send short message to MHWP for reason of appointment
    #email update

    def cancelAppointment(self):
        pass
    # selection done on MHWP'S calendar
    # email update

    def emailUpdate(self):
        pass
    # either done by the patint or MHWP

    def getRecord(self):
        return self.healthRecord


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


patient = Patient("hannah","zhao","h@gmail.com",user_type="patient",username="han",password="881",mhwpAsigned="drhannah",
                  emergencyEmail="hannahzhao2@han.com",
                  colourCode=None)



# patient.updateEmergencyContact()
# patient.searchExercises()
# patient.moodTracker()
# patient.journal()
patient.bookAppointment()


# Each calendar object is: [YYYY-MM-DD HH:MM:SS]



