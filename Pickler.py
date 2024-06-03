import pickle

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

print("You have started the Pickler.")
prompt = 0

while(prompt != "exit"):
    print("\nTo make a new pickle please type 'reset the pickle'\nTo check the current pickle type 'check'\nElse type 'exit' to end the program\n")
    prompt = input()
    if prompt == "reset the pickle" and prompt != "exit":

        #create empty dictionary for new pickle
        pickleDict = {}        

        #write new dictionary to memory
        with open("students_data.pkl", "wb") as fp:
            pickle.dump(pickleDict, fp)
            fp.close()

        print("\nPickle has been reset")
    
    elif prompt == "check" and prompt != "exit":
        with open("students_data.pkl", "rb") as fp:
            pickleDict = pickle.load(fp)
            print(pickleDict)
    
    elif prompt != "exit": 
        print("Invalid input. Please input one of the following prompts\n")
