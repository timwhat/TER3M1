import ast
import time
import os

fileDirectory = os.path.dirname(os.path.abspath(__file__))
parentDirectory = os.path.dirname(fileDirectory)

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
    print(rooms)
    # Options Menu
    exit = False
    while not exit:
        slowPrint(0.01, "Welcome to the Reservation System\n\n")
        slowPrint(0.005, "1. Create a Reservation\n")
        slowPrint(0.005, "2. View Reservations\n")
        slowPrint(0.005, "3. Search Available Rooms\n")
        slowPrint(0.005, "4. Generate Report\n")
        slowPrint(0.005, "5. Exit\n\n")
        slowPrint(0.005, "Please select an option [1-5]:")
        choice = inputChecker("", int)
        textSeperator()
        # Handle user choice
        if choice == 1:
            createReservation()
        elif choice == 2:
            viewReservations()
        elif choice == 3:
            # searchAvaislableRooms()
            pass
        elif choice == 4:
            # generateReport()
            pass
        elif choice == 5:
            updateRoomsFile()
            print("Exiting the system. Goodbye!")
            exit = True
        else:
            # print("Invalid option. Please try again.")
            pass
        textSeperator()

def retrieveRooms():
    try:
        with open ("rooms.txt","r") as f:
            return ast.literal_eval(f.read())
    except FileNotFoundError:
        slowPrint(0.005, "rooms.txt not found. Generating initial rooms...")
        generateInitialRooms()
        with open ("rooms.txt","r") as f:
            unconvertedRoomsList = ast.literal_eval(f.read())
        convertedRoomsList = unconvertedRoomsList
        for room in unconvertedRoomsList:
            for index, reservation in enumerate(room):
                convertedRoomsList[room][index] = objectifyDictionary(reservation)
        return convertedRoomsList

def objectifyDictionary(dictionary):
    newObject = Reservation(dictionary["name"],dictionary["id"],dictionary["role"],dictionary["reason"],dictionary["startTime"],dictionary["endTime"])
    return newObject

def viewReservations():
    selectedRoom = input("which room would you like to view the reservations for?\t")
    print('===============')
    resCounter = 1
    
    for reservation in rooms[selectedRoom]:
        print(str(resCounter)+":")
        print(f"start time: {reservation.startTime}:00")
        print("end time: "+str(reservation.endTime)+":00")
        print('===============')
        resCounter += 1
        
def updateRoomsFile():
    tempRooms = rooms
    for room in rooms:
        reservationList= tempRooms[room]
        newReservationList = []
        for reservation in reservationList:
            tempDict = reservation.dict()
            newReservationList.append(tempDict)
            print(tempDict)
        print(room,reservationList,newReservationList)
        tempRooms[room] = newReservationList
    with open ("rooms.txt","w") as f:
        f.write(str(tempRooms))
        pass

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
    slowPrint(0.005, "Enter your name:\t\t")
    tempName = inputChecker()
    slowPrint(0.005, "Enter your ID:\t\t\t")
    tempId = inputChecker()
    slowPrint(0.005, "Enter your role:\t\t")
    tempRole = inputChecker()
    slowPrint(0.005, "Enter reason:\t\t\t")
    tempReason = inputChecker()
    slowPrint(0.005, "Enter start time (ex. 10):\t")
    tempStartTime = inputChecker("", int)
    slowPrint(0.005, "Enter end time (ex. 22):\t")
    tempEndTime = inputChecker("", int)
    
    if checkTimeSlot(roomForReservation,tempStartTime,tempEndTime):
        tempReservation = Reservation(tempName,tempId,tempRole,tempReason,tempStartTime,tempEndTime)
        rooms[roomForReservation].append(tempReservation)
        # print(rooms)

# Check if the time slot is available
def checkTimeSlot(room, startTime, endTime):
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
            textSeperator()
            slowPrint(0.005, "Time slot invalid. Try again please")
            return False
    textSeperator()
    slowPrint(0.005, "Booking successful.\n")
    time.sleep(2)
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