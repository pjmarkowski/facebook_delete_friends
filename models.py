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

def friend_from_json(json):
    return Friend(
        json["name"],
        json["surname"],
        json["mutual_friends"],
        json["link"]
    )

class Friend:
    def __init__(self, name, surname, mutual_friends, link):
        self.name = name
        self.surname = surname
        self.mutual_friends = mutual_friends
        self.link = link


    def serialize(self):
        return {
            "name": str(self.name),
            "surname": str(self.surname),
            "mutual_friends": str(self.mutual_friends),
            "link": str(self.link)
        }
    
    def get_full_name(self):
        return str(self.name)+" "+str(self.surname)