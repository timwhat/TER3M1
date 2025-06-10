import ast
import time
# Reservation System for a School
# This system allows users to create reservations for rooms, view existing reservations, search for available rooms, and generate reports.
class Reservation:
    def __init__(self, name, id, role, reason, startTime, endTime):
        self.name = name
        self.id = id
        self.role = role
        self.reason = reason
        self.startTime = startTime
        self.endTime = endTime
    def dict(self):
        return {
            "name":self.name,
            "id":self.id,
            "role":self.role,
            "reason":self.reason,
            "startTime":self.startTime,
            "endTime":self.endTime
        }
    # searches for the information
    
def main():
    global rooms
    rooms = retrieveRooms()
    # Options Menu
    slowPrint(0.05, "Welcome to the Reservation System\n")
    slowPrint(0.05, "1. Create a Reservation\n")
    print("2. View Reservations")
    print("3. Search Available Rooms")
    print("4. Generate Report")
    print("5. Exit")
    choice = input("Please select an option [1-5]:")
    textSeperator()
    # Handle user choice
    if choice == '1':
        createReservation()
        pass
    elif choice == '2':
        # viewReservations()
        pass
    elif choice == '3':
        # searchAvailableRooms()
        pass
    elif choice == '4':
        # generateReport()
        pass
    elif choice == '5':
        # print("Exiting the system. Goodbye!")
        pass
    else:
        # print("Invalid option. Please try again.")
        pass

def retrieveRooms():
    # TODO adda what if this file doesnt exist
    with open ("rooms.txt","r") as f:
        return ast.literal_eval(f.read())

def objectifyDictionary(inDict):
    for room in inDict:
        x = x

def updateRoomsFile():
    with open ("rooms.txt","w") as f:
        f.write(str(rooms))

def generateInitialRooms():
    tempDict = {}
    for i in range(101,200):
        tempRoomName = "room" + str(i)
        tempDict.update({tempRoomName:[]})
    tempDict.update({"smallGym":[]})
    tempDict.update({"largeGym":[]})
    tempDict.update({"library":[]})
    tempDict.update({"compLab1":[]})
    tempDict.update({"compLab2":[]})
    with open ("rooms.txt","w") as f:
        f.write(str(tempDict))
# Used to visually separate text in the terminal
def textSeperator():
    print('\n/************************************************************************/\n')
    
def createReservation():
    roomForReservation = inputChecker("Enter the room you want to reserve\npossible reservations: [rooms 101-199, smallGym, largeGym, library, compLab1, and compLab2]:\n")
    # Logic to create a reservation
    tempName = inputChecker("Enter your name:\t\t")
    tempId = inputChecker("Enter your ID:\t\t\t")
    tempRole = inputChecker("Enter your role:\t\t")
    tempReason = inputChecker("Enter reason:\t\t\t")
    tempStartTime = inputChecker("Enter start time (ex. 10):\t", int)
    tempEndTime = inputChecker("Enter end time (ex. 22):\t", int)   
    if checkTimeSlot(roomForReservation,tempStartTime,tempEndTime):
        print("timslot success")
        tempReservation = Reservation(tempName,tempId,tempRole,tempReason,tempStartTime,tempEndTime)
        rooms[roomForReservation].append(tempReservation)
        print(rooms)

# Check if the time slot is available
def checkTimeSlot(room,startTime,endTime):
    takenHours = []
    requestedHours = []
    selectedRoomSchedule = rooms[room]
    for reservation in selectedRoomSchedule:
        for hour in range(reservation.startTime,reservation.endTime):
            takenHours.append(hour)
    for hour in range(startTime,endTime):
        requestedHours.append(hour)
    for i in requestedHours:
        if i in takenHours:
            return False
    return True
        

# Input Checker, to make sure the input is the right type
def inputChecker(inputText = '', typeOfInput = str):
    while True:
        try:
            userInput = typeOfInput(input(inputText))
            return userInput
        except ValueError:
            continue

# Function to print text with a delay between each character
def slowPrint( delay, *args):
    text = ' '.join(map(str, args))
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

# Check if the room number is valid
def roomNumChecker(roomName):
    global rooms
    if roomName in rooms:
        return True
    return False

main()

# generateInitialRooms()