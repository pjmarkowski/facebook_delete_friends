import datetime

def friend_number_list_from_json(json):
    return FriendNumberList(
        json["number"],
        json["date"]
    )
    
class FriendNumberList:
    def __init__(self, number, date):
        self.number = number
        self.date = date

    def serialize(self):
        return {
            "number": str(self.number),
            "date": str(self.date)
        }