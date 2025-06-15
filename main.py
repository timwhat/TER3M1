import ast
import time
import datetime
from datetime import timedelta

# configS
roomsFilePath = "rooms.txt"
fastText = 0.005

# currentDate = "YYYY-MM-DD" # <----- date override, comment out the line below and put in a date to override
currentDate = datetime.datetime.now().strftime("%Y-%m-%d")

# lengths for the tables
# Date, Start Time, End Time, Name, Role, Reason
lengths = [2, 10, 10, 8, 13, 11, 32]


# Reservation System for a School
# This system allows users to create reservations for rooms, view existing reservations, search for available rooms, and generate reports.  
def main():
    global rooms
    rooms = retrieveRooms()
    # print(rooms)
    # Options Menu
    exit = False
    while not exit:
        textSeparator()
        slowPrint(0.01, "===== NHSS Room Reservation System =====\n\n")
        
        slowPrint(fastText, "Today's date is: ", currentDate, "\n")
        slowPrint(fastText, "Please select an option from the menu below:\n\n")
        slowPrint(fastText, "1. Create / Delete a Reservation\n")
        slowPrint(fastText, "2. View Reservations / Search Available Hours\n")
        slowPrint(fastText, "3. Generate Room Usage or Member Reservation Report\n")
        slowPrint(fastText, "4. Save & Quit\n\n")
        slowPrint(fastText, "Please select an option [1-4]:\t")
        choice = inputChecker("", int)
        textSeparator()
        
        # Handle user choice
        if choice == 1:
            slowPrint(fastText, "Do you want to create or delete a reservation? [1-2]:\t")
            subChoice = inputChecker("", int)
            if subChoice == 1 or subChoice == '':
                createReservation()
            elif subChoice == 2:
                deleteReservation()
            else:
                slowPrint(fastText, "Invalid option. Please try again.\n")
                continue
        elif choice == 2:
            slowPrint(fastText, "Do you want to view reservations or search a room for available hours? [1-2]:\t")
            subChoice = inputChecker("", int)
            if subChoice == 1 or subChoice == '':
                slowPrint(fastText, "Enter the room you want to view reservations for [room101 to room199, smallGym, largeGym, library, compLab1, and compLab2]:\n\t")
                selectedRoom = validRoomInputChecker()
                if not roomNumChecker(selectedRoom):
                    slowPrint(fastText, "Invalid room name. Please try again.\n")
                    continue
                textSeparator()
                # slowPrint(fastText, f"Viewing reservations for {selectedRoom}...\n")
                viewReservations(selectedRoom)
            elif subChoice == 2:
                searchAvailableHours()
            else:
                slowPrint(fastText, "Invalid option. Please try again.\n")
                continue
        elif choice == 3:
            slowPrint(fastText, "Enter the start date for statistics (YYYY-MM-DD) [press Enter for today]:\t")
            searchStartDate = dateInputChecker()
            slowPrint(fastText, "Enter the end date for statistics (YYYY-MM-DD) [press Enter for today]:\t")
            searchEndDate = dateInputChecker()
            if searchStartDate > searchEndDate:
                slowPrint(fastText, "Ending date is before starting date, please try again.\n")
                continue
            subChoice = inputChecker("Do you want to generate statistics for a user or for a room? [1-2]:\t", int)
            if subChoice == 1:
                userName = inputChecker("Enter the name of the user:\t")
                textSeparator()
                generateUserStatistics(userName, searchStartDate, searchEndDate)
            elif subChoice == 2:
                roomName = inputChecker("Enter the name of the room:\t")
                textSeparator()
                generateRoomStatistics(roomName, searchStartDate, searchEndDate)
            else:
                slowPrint(fastText, "Invalid option. Please try again.\n")
                continue
        elif choice == 4:
            updateRoomsFile()
            print("Exiting the system. Goodbye!")
            exit = True
        else:
            print("Invalid option. Please try again.")
            pass
        # textSeparator()
        
class Reservation:
    def __init__(self, name, role, reason, date, startTime, endTime):
        self.name = name
        self.role = role
        self.reason = reason
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
    def dict(self):
        return {
            "name":self.name,
            "role":self.role,
            "reason":self.reason,
            "date":self.date,
            "startTime":self.startTime,
            "endTime":self.endTime
        }
    # searches for the information

def retrieveRooms():
    try:
        with open (roomsFilePath,"r") as f:
            unconvertedRoomsList = ast.literal_eval(f.read())
    except FileNotFoundError:
        print("Rooms file not found. Generating initial rooms...")
        generateInitialRooms()
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
    newObject = Reservation(dictionary["name"],dictionary["role"],dictionary["reason"],dictionary["date"], dictionary["startTime"],dictionary["endTime"])
    # print("objectified",dictionary,"into",newObject)
    return newObject

def viewReservations(selectedRoom=None):
    global rooms
    if not rooms[selectedRoom]:
        print(f"\nNo reservations found for {selectedRoom}.")
        return
    print(f"Reservations for {selectedRoom}:")
    reservationInfoTablePrinter(rooms[selectedRoom])
    enterToContinue()    
    
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
        
def generateUserStatistics(userName, startDate, endDate):
    global rooms
    userReservations = []
    for room in rooms:
        for reservation in rooms[room]:
            if reservation.name == userName and startDate <= reservation.date <= endDate:
                userReservations.append((room, reservation))

    if not userReservations:
        slowPrint(fastText, f"\nNo reservations found for {userName} between {startDate} and {endDate}.\n")
        return

    slowPrint(fastText, f"\nReservations for {userName} from {startDate} to {endDate}:\n")
    # Additional summary statistics
    unique_rooms = set(room for room, _ in userReservations)
    slowPrint(fastText, f"\nSummary:\n")
    slowPrint(fastText, f"Total reservations: {len(userReservations)}\n")
    slowPrint(fastText, f"Unique rooms booked by {userName}: {len(unique_rooms)}\n")
    if unique_rooms:
        slowPrint(fastText, f"Rooms: {', '.join(sorted(unique_rooms))}\n")

    
    # Print detailed reservations in this format not in the table as this is easier to copy and paste
    slowPrint(fastText, f"\nDetailed Reservations:\n")
    for room, res in userReservations:
        slowPrint(fastText, f"Room: {room}, Date: {res.date}, Start Time: {res.startTime}:00, End Time: {res.endTime}:00, Reason: {res.reason}\n")

def generateRoomStatistics(roomName, startDate, endDate):
    global rooms
    if roomName not in rooms:
        slowPrint(fastText, f"Room {roomName} does not exist.\n")
        return

    roomReservations = []
    for reservation in rooms[roomName]:
        if startDate <= reservation.date <= endDate:
            roomReservations.append(reservation)

    if not roomReservations:
        slowPrint(fastText, f"No reservations found for {roomName} between {startDate} and {endDate}.\n")
        return

    # Calculate statistics for the room
    total_reservations = len(roomReservations)
    unique_users = set()
    user_counts = {}

    for reservation in roomReservations:
        unique_users.add(reservation.name)
        user_counts[reservation.name] = user_counts.get(reservation.name, 0) + 1

    slowPrint(fastText, f"Summary for {roomName} from {startDate} to {endDate}:\n\n")
    slowPrint(fastText, f"Total times booked: {total_reservations}\n")
    slowPrint(fastText, f"Unique users: {len(unique_users)}\n")
    if unique_users:
        slowPrint(fastText, "Bookings per user:\n")
        for user, count in user_counts.items():
            slowPrint(fastText, f"  {user}: {count} time(s)\n")
    slowPrint(fastText, f"\nDetailed Reservations for {roomName} from {startDate} to {endDate}:\n")
    for res in roomReservations:
        slowPrint(fastText, f"Name: {res.name}, Role: {res.role}, Date: {res.date}, Start Time: {res.startTime}:00, End Time: {res.endTime}:00, Reason: {res.reason}\n")

def searchAvailableHours():
    slowPrint(fastText, "\nEnter the room you want to reserve [room101 to room199, smallGym, largeGym, library, compLab1, and compLab2]:\n\t")
    roomName = validRoomInputChecker()
    slowPrint(fastText, "Enter starting date (YYYY-MM-DD) [press Enter for today]:\t")
    startDate = convertStringDateToDateObject(dateInputChecker())
    slowPrint(fastText, "Enter ending date (YYYY-MM-DD ) [press Enter for today]:\t")
    endDate = convertStringDateToDateObject(dateInputChecker())
    roomData = rooms[roomName]
    if startDate > endDate:
        slowPrint(fastText, "Ending date is before starting date, please try again.\n")
        return
    
    slowPrint(fastText, f"# means reserved, . means available\n")
    
    while startDate <= endDate:
        hourVisualizer = []
        for i in range(24):
            hourVisualizer.append(".")
        stringStartDate = startDate.strftime('%Y-%m-%d')
        for reservation in roomData:
            if reservation.date == stringStartDate:
                for hour in range(reservation.startTime,reservation.endTime):
                    hourVisualizer[hour] = "#"
        stringVerHourVisualizer = ""
        for i in hourVisualizer:
            stringVerHourVisualizer += i
        # opted not to use slow print here due to performance issues with large outputs
        print(stringStartDate + " |  " + stringVerHourVisualizer)
        startDate += timedelta(days=1)
    print()
    enterToContinue()


def convertStringDateToDateObject(stringVer):
    stage = 0
    year = ""
    month = ""
    day = ""
    for i in stringVer:
        if i == "-":
            stage += 1
            continue
        if stage == 0:
            year += i
        if stage == 1:
            month += i
        if stage == 2:
            day += i
    return datetime.datetime(int(year),int(month),int(day))
            
# Used to visually separate text in the terminal 
def textSeparator():
    print('\n/************************************************************************/\n')

# Function to create a reservation
def createReservation():
    # Getting the User Input 
    slowPrint(fastText, "\nEnter the room you want to reserve [room101 to room199, smallGym, largeGym, library, compLab1, and compLab2]:\n\t")
    roomForReservation = validRoomInputChecker()
    textSeparator()
    slowPrint(fastText, "Enter your name:\t\t")
    tempName = inputChecker()
    slowPrint(fastText, "Enter your role:\t\t")
    tempRole = inputChecker()
    slowPrint(fastText, "Enter reason:\t\t\t")
    tempReason = inputChecker()
    slowPrint(fastText, "Enter date (YYYY-MM-DD) [press Enter for today]:\t")
    tempDate = dateInputChecker()
    timeRange = timesInputChecker()
    tempStartTime = timeRange[0]
    tempEndTime = timeRange[1]
    
    textSeparator()

    # Prepare a list of lists for the table printer
    reservation_data = [[
        tempDate,
        tempStartTime,
        tempEndTime,
        tempName,
        tempRole,
        tempReason
    ]]
    reservationInfoTablePrinter(reservation_data)

    print("Please confirm your reservation details:\n")
    slowPrint(fastText, "Confirm reservation? [y/n]: ")
    if not yesNoInputChecker():
        slowPrint(fastText, "Reservation cancelled.\n")
        return

    if checkTimeSlot(roomForReservation, tempDate, tempStartTime, tempEndTime):
        tempReservation = Reservation(tempName, tempRole, tempReason, tempDate, tempStartTime, tempEndTime)
        rooms[roomForReservation].append(tempReservation)
        slowPrint(fastText, "Reservation created successfully!\n")

def deleteReservation():
    textSeparator()
    slowPrint(fastText, "Which room would you like to delete a reservation from?\t")
    try:
        selectedRoom = inputChecker("", str)
        if not roomNumChecker(selectedRoom):
            slowPrint(fastText, "Invalid room name. Please try again.\n")
            return
    except ValueError:
        slowPrint(fastText, "Invalid input. Please enter a valid room name.\n")
        return
    textSeparator()
    viewReservations(selectedRoom)
    selectedReservation = inputChecker("Which reservation would you like to delete? [-1 to exit]\t",int)
    if selectedReservation == -1:
        slowPrint(fastText, "Exiting deletion process.\n")
        return
    if selectedReservation < 1 or selectedReservation > len(rooms[selectedRoom]):
        slowPrint(fastText, "Invalid reservation number. Please try again.\n")
        return
    slowPrint(fastText, "To confirm, you are deleting this reservation [y/n]:\t")
    if not yesNoInputChecker():
        slowPrint(fastText, "Deletion cancelled.\n")
        return
    else:
        slowPrint(fastText, "Deleting the reservation...\n")
    textSeparator()

# Check if the time slot is available
def checkTimeSlot(room, date, startTime, endTime):
    takenHours = []
    requestedHours = []
    selectedRoomSchedule = rooms[room]
    for reservation in selectedRoomSchedule:
        if reservation.date != date:
            continue
        for hour in range(reservation.startTime,reservation.endTime):
            takenHours.append(hour)
    for hour in range(startTime,endTime):
        requestedHours.append(hour)
    for i in requestedHours:
        if i in takenHours:
            textSeparator()
            slowPrint(fastText, "Time slot invalid. Try again please\n")
            return False
    textSeparator()
    slowPrint(0.1, ".......")
    slowPrint(fastText, "Booking successful.\n")
    time.sleep(0.5)
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

def timesChecker(startTime,endTime):
    if startTime >= 0 and endTime <= 24 and startTime < endTime:
        return True  
    else:
        return False

def timesInputChecker():
    while True:
        slowPrint(fastText, "Enter start time (ex. 10, minimum 0):\t")
        startTime = inputChecker("",int)
        slowPrint(fastText, "Enter end time (ex. 22, maximum 24):\t")
        endTime = inputChecker("",int)
        if timesChecker(startTime,endTime):
            return [startTime,endTime]
        else:
            print("Invalid time range, try again")
            continue
        
def yesNoInputChecker():
    while True:
        userInput = inputChecker('', str).lower()
        if userInput in ['yes', 'no', 'y', 'n']:
            return userInput in ['yes', 'y']
        else:
            slowPrint(fastText, "Invalid input. Please enter 'yes' or 'no'.")

def validRoomInputChecker():
    while True:
        userInput = inputChecker('', str)
        if userInput in rooms:
            return userInput
        else:
            print("Invalid input. Valid rooms are room101 to room199, smallGym, largeGym, library, compLab1, and compLab2.")
            continue

def dateInputChecker():
    while True:
        tempDate = inputChecker("", str)
        if tempDate.strip() == "":
            tempDate = currentDate
            break
        try:
            datetime.datetime.strptime(tempDate, "%Y-%m-%d")
            if tempDate < currentDate:
                slowPrint(fastText, "Date is in the past, are you sure you would like to proceed? [y/n].\n")
                if not yesNoInputChecker():
                    slowPrint(fastText, "Please enter a valid date.\n")
                    continue
            break
        except ValueError:
            print("Invalid date format. Please enter a valid YYYY-MM-DD.")
    return tempDate

def enterToContinue():
    slowPrint(fastText, "Press Enter to continue...")
    input()
    
def lengthCorrector(string, length):
    if len(string) < length:
        return string + " " * (length - len(string))
    elif len(string) > length:
        return string[:length-3] + "..."
    return string[:length]

def reservationInfoTablePrinter(roomList):
    slowPrint(fastText, "|------- Reservation Information --------------------------------------------------------------------------|\n")
    slowPrint(fastText, "|    | Date       | Start Time | End Time | Name          | Role        | Reason                           |\n")
    slowPrint(fastText, "|----|------------|------------|----------|---------------|-------------|----------------------------------|\n")
    for index,row in enumerate(roomList):
        # If row is a Reservation object, extract its attributes
        if hasattr(row, 'date') and hasattr(row, 'startTime'):
            fields = [
                str(index+1),
                row.date,
                f"{row.startTime}:00",
                f"{row.endTime}:00",
                row.name,
                row.role,
                row.reason
            ]
        else:
            fields = row
        row_str = "|"
        for i, field in enumerate(fields):
            row_str += f" {lengthCorrector(str(field), lengths[i])} |"
        slowPrint(fastText, row_str + "\n")
    slowPrint(fastText, "|----|------------|------------|----------|---------------|-------------|----------------------------------|\n\n")

main()

# generateInitialRooms()