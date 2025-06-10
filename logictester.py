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
    # searhces for the information

global rooms

res1 = Reservation("a","b","c","d",4,7,) # hours 1 and 2
res2 = Reservation("a","b","c","d",7,10,) # hours 7, 8, and 9
rooms = {"room111":(res1,res2)}

def checkTimeSlot(room,startTime,endTime):
    takenHours = []
    requestedHours = []
    selectedRoomSchedule = rooms[room]
    for reservation in selectedRoomSchedule:
        for hour in range(reservation.startTime,reservation.endTime):
            # print(hour)
            takenHours.append(hour)
        # print("------------")
    for hour in range(startTime,endTime):
        # print(hour)
        requestedHours.append(hour)
    # print("------------")
    # print(takenHours)
    # print(requestedHours)
    # print("------------")
    for i in requestedHours:
        if i in takenHours:
            return False
    return True
    
print(checkTimeSlot("room111",10,20))