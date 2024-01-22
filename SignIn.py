from colorama import Fore, Back, Style
import getpass
import pickle
import time as t
from datetime import datetime as d


class Student:
    ID = "" 
    name = ""
    timeIn = None 
    timeOut = None 
    prettyTimeIn = None 
    prettyTimeOut = None 
    timeElapsed = 0
    present = False  

    def __init__(self, ID, timeIn, prettyTimeIn, present):
        self.ID = ID 
        self.timeIn = timeIn
        self.prettyTimeIn = prettyTimeIn
        self.present = present


def convertTime(time):
    hours = twoDigit(str(int(time//3600)))
    minutes = twoDigit(str((int(time%3600)//60)))
    seconds = twoDigit(str(int(time%60)))
    return hours + ":" + minutes + ":" + seconds

def twoDigit(num):
    if len(num) == 1:
        return "0" + num 
    return num

#students = {}

#read in dictionary from previous day
with open("students_data.pkl", "rb") as fp:
    students = pickle.load(fp)
    print("PRINTING STUDENTS DICTIONARY")
    print(students)

numPresent = 0 

tempID = getpass.getpass(prompt="Welcome to the Math Center\nAwaiting card swipe...")

file = open("MC_Attendance_Fall23.csv", "a", encoding="utf-8")

while(tempID != "exit" and  d.now().strftime("%H") != "17"):
        
    # if the student has not beeen signed in today
    if tempID not in students and tempID != "exit":

        numPresent += 1
        students[tempID] = Student(tempID, t.time(), d.now().strftime("%m-%d-%Y, %H:%M:%S"), True)
        if students[tempID].name == "":
            print(Fore.RED + "NEW STUDENT HAS BEEN SWIPED, PLEASE INPUT STUDENT NAME" + Fore.BLACK)
            students[tempID].name = input()
        print(Fore.MAGENTA + students[tempID].name + " signed in at " + students[tempID].prettyTimeIn + "for the first time today.")
        print(Fore.BLUE + "There are currently " + str(numPresent) + " students in the Math Center.")
        

    # if they're currently signed in 
    elif students[tempID].present: 

        numPresent -= 1
        # save time out and time elapsed in variables
        students[tempID].timeOut = t.time()
        students[tempID].prettyTimeOut = d.now().strftime("%H:%M:%S")
        tempElapsed = students[tempID].timeOut - students[tempID].timeIn
        students[tempID].timeElapsed = students[tempID].timeElapsed + tempElapsed

        # make string to be written 
        studentData = students[tempID].ID + "," + students[tempID].prettyTimeIn + "," 
        studentData = studentData + students[tempID].prettyTimeOut + ","
        studentData = studentData + convertTime(students[tempID].timeElapsed) + "\n"

        file.write(studentData)

        # reset student to be checked in again later
        students[tempID].timeIn = None 
        students[tempID].timeOut = None
        students[tempID].present = False 

        print(Fore.CYAN + students[tempID].name + " signed out at " + t.strftime("%H:%M:%S"))
        print(Fore.GREEN + students[tempID].name + " spent " + convertTime(students[tempID].timeElapsed) + " at the Math center this semester.")
        print(Fore.BLUE + "There are currently " + str(numPresent) + " students in the Math Center.")

    # otherwise, they have been signed in before, but are not currently
    else: 

        numPresent += 1
        students[tempID].timeIn = t.time()
        students[tempID].present = True

        print(Fore.GREEN + students[tempID].name + " signed back in at " + t.strftime("%H:%M:%S"))
        print(Fore.BLUE + "There are currently " + str(numPresent) + " students in the Math Center.")

    tempID = getpass.getpass(prompt="")

# Now sign everyone out
for signedIn in students: 
    if students[signedIn].present: 

        # save time out and time elapsed in variables
        students[signedIn].timeOut = t.time()
        students[signedIn].prettyTimeOut = d.now().strftime("%H:%M:%S")
        tempElapsed = students[signedIn].timeOut - students[signedIn].timeIn
        students[signedIn].timeElapsed = students[signedIn].timeElapsed + tempElapsed

        # make string to be written 
        studentData = students[signedIn].ID + "," + students[signedIn].prettyTimeIn + "," 
        studentData = studentData + students[signedIn].prettyTimeOut + ","
        studentData = studentData + convertTime(students[signedIn].timeElapsed) + "\n"

        file.write(studentData)

        # reset student to be checked in again later
        students[signedIn].timeIn = None 
        students[signedIn].timeOut = None
        students[signedIn].present = False 

        print(Fore.CYAN + students[signedIn].name + " signed out at " + t.strftime("%H:%M:%S"))
        print(Fore.GREEN + students[signedIn].name + " spent " + convertTime(students[signedIn].timeElapsed) + " at the Math center.")

numPresent = 0
print(Fore.BLACK + "Everyone signed out.")

file.close()

#write updated dictionary to memory
with open("students_data.pkl", "wb") as fp:
    pickle.dump(students, fp)
    fp.close()