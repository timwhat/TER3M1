import ast
import time
import datetime

# configS
roomsFilePath = "rooms.txt"
fastText = 0.005
currentDate = datetime.datetime.now().strftime("%Y-%m-%d")

# Reservation System for a School
# This system allows users to create reservations for rooms, view existing reservations, search for available rooms, and generate reports.  
def main():
    global rooms
    rooms = retrieveRooms()
    # print(rooms)
    # Options Menu
    exit = False
    while not exit:
        textSeperator()
        slowPrint(0.01, "Welcome to the Reservation System!\n\n")
        
        slowPrint(fastText, "Today's date is: ", currentDate, "\n")
        slowPrint(fastText, "Please select an option from the menu below:\n\n")
        slowPrint(fastText, "1. Create/Delete a Reservation\n")
        slowPrint(fastText, "2. View Reservations / Search Available Rooms\n") # we combining this with search available rooms
        # slowPrint(fastText, "3. Search Available Rooms\n")
        slowPrint(fastText, "3. Generate Report\n")
        slowPrint(fastText, "4. Exit\n\n")
        slowPrint(fastText, "Please select an option [1-5]:\t")
        choice = inputChecker("", int)
        textSeperator()
        
        # Handle user choice
        if choice == 1:
            slowPrint(fastText, "Do you want to create or delete a reservation? [1-2]:\t")
            subChoice = inputChecker("", int)
            if subChoice == 1 or subChoice == '':
                createReservation()
                slowPrint(fastText, "Creating a reservation...\n")
            elif subChoice == 2:
                deleteReservation()
                slowPrint(fastText, "Deleting a reservation...\n")
            else:
                slowPrint(fastText, "Invalid option. Please try again.\n")
                continue
        elif choice == 2:
            selectedRoom = input("which room would you like to view the reservations for?\t")
            try: 
                viewReservations(selectedRoom)
            except KeyError:
                print("Invalid room name. Please try again.")
                continue
        elif choice == 3:
            #TODO: How do we wanna display this??!?
            # Thinking rn we can just ask user for a list of rooms and display
            pass
        elif choice == 4:
            subChoice = inputChecker("Do you want to generate a report for a user or for a room? [1-2]:\t", int)
            if subChoice == 1:
                userName = inputChecker("Enter the name of the user:\t")
            if subChoice == 2:
                roomName = inputChecker("Enter the name of the room:\t")
        elif choice == 5:
            updateRoomsFile()
            print("Exiting the system. Goodbye!")
            exit = True
        else:
            print("Invalid option. Please try again.")
            pass
        # textSeperator()
        
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

def retrieveRooms():
    with open (roomsFilePath,"r") as f:
        unconvertedRoomsList = ast.literal_eval(f.read())
    # print(unconvertedRoomsList)
    convertedRoomsList = unconvertedRoomsList
    for room in unconvertedRoomsList:
        # print(room)
        for index, reservation in enumerate(unconvertedRoomsList[room]):
            convertedRoomsList[room][index] = objectifyDictionary(reservation)
    return convertedRoomsList
                                                                                                                        
def objectifyDictionary(dictionary):
    newObject = Reservation(dictionary["name"],dictionary["id"],dictionary["role"],dictionary["reason"],dictionary["startTime"],dictionary["endTime"])
    # print("objectified",dictionary,"into",newObject)
    return newObject

def viewReservations(selectedRoom):
    
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
            # print(tempDict)
        # print(room,reservationList,newReservationList)
        tempRooms[room] = newReservationList
    with open (roomsFilePath, "w") as f:
        f.write(str(tempRooms))

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
    print(roomsFilePath)
    with open (roomsFilePath,"w") as f:
        f.write(str(tempDict))
        
# Used to visually separate text in the terminal 
def textSeperator():
    print('\n/************************************************************************/\n')

# Function to create a reservation
def createReservation():
    # Getting the User Input 
    slowPrint(fastText, "\nEnter the room you want to reserve [rooms 101-199, smallGym, largeGym, library, compLab1, and compLab2]:\n\t")
    roomForReservation = inputChecker("")
    textSeperator()
    slowPrint(fastText, "Enter your name:\t\t")
    tempName = inputChecker()
    slowPrint(fastText, "Enter your ID:\t\t\t")
    tempId = inputChecker()
    slowPrint(fastText, "Enter your role:\t\t")
    tempRole = inputChecker()
    slowPrint(fastText, "Enter reason:\t\t\t")
    tempReason = inputChecker()
    slowPrint(fastText, "Enter start time (ex. 10):\t")
    tempStartTime = inputChecker("", int)
    slowPrint(fastText, "Enter end time (ex. 22):\t")
    tempEndTime = inputChecker("", int)
    
    if checkTimeSlot(roomForReservation,tempStartTime,tempEndTime):
        tempReservation = Reservation(tempName,tempId,tempRole,tempReason,tempStartTime,tempEndTime)
        rooms[roomForReservation].append(tempReservation)
        # print(rooms)
def deleteReservation():
    selectedRoom = input("which room would you like to delete a reservation from?\t")
    viewReservations(selectedRoom)
    selectedReservation = inputChecker("which reservation would you like to delete?\t",int)
    textSeperator()
    rooms[selectedRoom].pop(selectedReservation-1)
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
            slowPrint(fastText, "Time slot invalid. Try again please")
            return False
    textSeperator()
    slowPrint(0.1, ".......")
    slowPrint(fastText, "Booking successful.\n")
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