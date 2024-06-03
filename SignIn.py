from tkinter import *
import csv
from colorama import Fore, Back, Style
import getpass
import pickle
import time as t
from datetime import datetime as d

class Student:
    ID = "" 
    name = ""
    course = ""
    timeIn = None 
    timeOut = None 
    prettyTimeIn = None 
    prettyTimeOut = None 
    timeElapsed = 0
    present = False  
    canceled = False
    

    def __init__(self, ID, timeIn, prettyTimeIn, present):
        self.ID = ID 
        self.timeIn = timeIn
        self.prettyTimeIn = prettyTimeIn
        self.present = present

# start functions
def convertTime(time):
    hours = twoDigit(str(int(time//3600)))
    minutes = twoDigit(str((int(time%3600)//60)))
    seconds = twoDigit(str(int(time%60)))
    return hours + ":" + minutes + ":" + seconds

def twoDigit(num):
    if len(num) == 1:
        return "0" + num 
    return num

# for tkinter window
def save():
    ni = nameInput.get()
    print(ni + " saved")
    students[tempID].name = nameInput.get()
    students[tempID].course = clicked.get()
    students[tempID].canceled = False
    return

def cancel():
    students[tempID].canceled = True
    root.destroy()
    return

def savePickle(fileName):
    with open(fileName, "wb") as fp:
        pickle.dump(students, fp)
        fp.close()

def saveAttendance(fileName, ID_num):

    # make string to be written 
    studentData = students[ID_num].ID + "," + students[ID_num].name + "," 
    studentData = studentData + students[ID_num].prettyTimeIn + "," 
    studentData = studentData + students[ID_num].prettyTimeOut + ","
    studentData = studentData + convertTime(students[ID_num].timeElapsed) + ","
    studentData = studentData + students[ID_num].course + "\n"

    file = open("MC_Attendance_Fall23.csv", "a", encoding="utf-8")
    file.write(studentData)
    file.close
# end functions


#read in dictionary from previous day
with open("students_data.pkl", "rb") as fp:
    students = pickle.load(fp)


numPresent = sum(bool(students[ID].present) for ID in students)
tempID = 0
attendanceFile = "MC_Attendance_Fall23.csv"

print("Welcome to the Math Center\n")

while(tempID != "exit"):
      
    tempID = input(Fore.BLACK + "Input student ID: ")

    if tempID == "report":
        for signedIn in students: 
            if students[signedIn].present:
                print(Fore.GREEN + students[signedIn].name + " " + students[signedIn].course)
        continue
                

    # if the student has not beeen signed in today
    if tempID not in students and tempID != "exit":

        students[tempID] = Student(tempID, t.time(), d.now().strftime("%m-%d-%Y, %H:%M:%S"), True)
        
        if students[tempID].name == "":


            # imports course spreadsheet to list
            with open('Courses.csv', newline='') as courseSheet:
                reader = csv.reader(courseSheet)
                coursesTemp = list(reader)
                
            # we have to do this to reduce the dimension of the courses list
            # otherwise, the dropdown menu with have curly braces
            courses = []

            for c1 in coursesTemp:
                for c2 in c1:
                    courses.append(c2) 

            students[tempID].canceled = True

            # start window
            root = Tk()
            root.geometry("400x400")
            nameLabel = Label(root, text="Student Name: ")
            nameInput = Entry(root)
            clicked = StringVar()
            clicked.set("Select Course")
            drop = OptionMenu(root, clicked, *courses)
            saveButton = Button(root, text = "Save Data", command = save)
            cancelButton = Button(root, text = "Cancel", command = cancel)
            
            nameLabel.place(x=20 , y=20)
            nameInput.place(x=110 , y=20)
            drop.place(x=110 , y=50)
            saveButton.place(x=135 , y=90)
            cancelButton.place(x=140, y=130)
            
            root.mainloop()
        # end window
            
        if students[tempID].canceled:
            students.pop(tempID)
            print("Student canceled!")
            continue

        numPresent += 1

        print(Fore.MAGENTA + students[tempID].name + " signed in at " + students[tempID].prettyTimeIn + " for the first time today.")
        print(students[tempID].name + "is taking " + students[tempID].course)
        print(Fore.BLUE + "There are currently " + str(numPresent) + " students in the Math Center.")
        

    # if they're currently signed in 
    elif tempID != "exit" and students[tempID].present: 

        numPresent -= 1

        # save time out and time elapsed in variables
        students[tempID].timeOut = t.time()
        students[tempID].prettyTimeOut = d.now().strftime("%H:%M:%S")
        tempElapsed = students[tempID].timeOut - students[tempID].timeIn
        students[tempID].timeElapsed = students[tempID].timeElapsed + tempElapsed

        saveAttendance(attendanceFile, tempID)

        # reset student to be checked in again later
        students[tempID].timeIn = None 
        students[tempID].timeOut = None
        students[tempID].present = False 

        print(Fore.CYAN + students[tempID].name + " signed out at " + t.strftime("%H:%M:%S"))
        print(Fore.GREEN + students[tempID].name + " spent " + convertTime(students[tempID].timeElapsed) + " at the Math center this semester.")
        print(Fore.BLUE + "There are currently " + str(numPresent) + " students in the Math Center.")

    # otherwise, they have been signed in before, but are not currently
    elif tempID != "exit": 

        numPresent += 1
        students[tempID].timeIn = t.time()
        students[tempID].prettyTimeIn = d.now().strftime("%m-%d-%Y, %H:%M:%S")
        students[tempID].present = True

        print(Fore.GREEN + students[tempID].name + " signed back in at " + t.strftime("%H:%M:%S"))
        print(students[tempID].name, "is taking ", students[tempID].course)
        print(Fore.BLUE + "There are currently " + str(numPresent) + " students in the Math Center.")

    savePickle("students_data.pkl")
    
# Now sign everyone out
for signedIn in students: 
    if students[signedIn].present: 

        # save time out and time elapsed in variables
        students[signedIn].timeOut = t.time()
        students[signedIn].prettyTimeOut = d.now().strftime("%H:%M:%S")
        tempElapsed = students[signedIn].timeOut - students[signedIn].timeIn
        students[signedIn].timeElapsed = students[signedIn].timeElapsed + tempElapsed

        saveAttendance(attendanceFile, signedIn)

        # reset student to be checked in again later
        students[signedIn].timeIn = None 
        students[signedIn].timeOut = None
        students[signedIn].present = False 

        print(Fore.CYAN + students[signedIn].name + " signed out at " + t.strftime("%H:%M:%S"))
        print(Fore.GREEN + students[signedIn].name + " spent " + convertTime(students[signedIn].timeElapsed) + " at the Math center.")

numPresent = 0
print(Fore.BLACK + "Everyone signed out.")

#write updated dictionary to memory
savePickle("students_data.pkl")
