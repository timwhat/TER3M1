class Reservation:
    def __init__(self, name, id, role, reason, startTime, endTime):
        self.name = name
        self.id = id
        self.role = role
        self.reason = reason
        self.timeRange = timeRange
    def dict(self):
        return {
            "name":self.name,
            "id":self.id,
            "role":self.role,
            "reason":self.reason,
            "timeRange":self.timeRange
        }
    def createReservation(self):
        # Logic to create a reservation
        input("Enter your name: ")
        input("Enter your ID: ")
        input("Enter your role: ")
        input("Enter the reason for reservation: ")
        input("Enter the time range for reservation: ")
    
def main():
    normalRooms = retrieveNormalRooms()
    specialRooms = retrieveSpecialRooms()
    # Options Menu
    textSeperator()
    print("Welcome to the Reservation System")
    print("1. Create a Reservation")
    print("2. View Reservations")
    print("3. Search Available Rooms")
    print("4. Generate Report")
    print("5. Exit")
    choice = input("Please select an option (1-5): ")
    textSeperator()
    # Handle user choice
    if choice == '1':
        # createReservation()
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

def retrieveNormalRooms():
    # TODO adda what if this file doesnt exist
    with open ("rooms.txt","r") as f:
        roomFile = f.read()
    print(roomFile)
    
def retrieveSpecialRooms():
    pass

# Used to visually seperate text in the terminal
def textSeperator():
    print('\n/************************************************************************/\n')

#main()

testerObject = Reservation(1,2,3,4,(5,6))
testerObjectDict = Reservation.dict(testerObject)
dict = {
  "room101": testerObjectDict,
}

with open ("rooms.txt","w") as f:
    f.write(str(dict))    