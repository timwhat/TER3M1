import ast

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

def retrieveRooms():
    # TODO adda what if this file doesnt exist
    with open ("rooms.txt","r") as f:
        return ast.literal_eval(f.read())

# Used to visually seperate text in the terminal
def textSeperator():
    print('\n/************************************************************************/\n')

#main()

testerObject1 = Reservation(1,2,3,4,5,6)
testerObjectDict1 = Reservation.dict(testerObject1)

testerObject2 = Reservation(10,20,30,40,50,60)
testerObjectDict2 = Reservation.dict(testerObject2)

dict = {
  "room101": (testerObjectDict1,testerObjectDict2),"library":()
}

with open ("rooms.txt","w") as f:
    f.write(str(dict))

readeth = retrieveRooms()

print(readeth["room101"][1])