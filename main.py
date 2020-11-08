import sys 
import os 
import json
from datetime import date, timedelta
from models import FriendNumberList, friend_number_list_from_json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

data = {}
data["FriendsNumber"]=[]
friendnumbers = []


def main():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=options,executable_path=r'/Users/piotrmar/piotr/Projekty/tools/chromedriver')
    driver.get("http://www.facebook.com")
    driver.implicitly_wait(30)
    driver.find_element_by_xpath('//*[@id="u_0_h"]').click() # accept cookies
    username = os.getenv('FB_USERNAME')
    password = os.getenv('FB_PASS')
    driver.find_element_by_id('email').send_keys(username)
    driver.find_element_by_id('pass').send_keys(password)
    driver.find_element_by_name('login').click()
    driver.implicitly_wait(30)
    driver.get("http://www.facebook.com/piotr.markowski.904/friends")
    friends_table = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/div/a[3]/div/span/span[2]')
    print("tets")
    add_to_friend_list(friends_table.text)
    print(friends_table.text)

def add_to_friend_list(number_of_friends):
    global data
    try:
        with open('database/friend_number_list.json') as json_file:
            data = json.load(json_file)
    except:
        print("There was no file")

    with open('database/friend_number_list.json', 'w') as json_file:
        should_add = True
        for d in data["FriendsNumber"]:
            if (d.get("date") == str(date.today())):
                should_add = False
        
        if should_add:
            data["FriendsNumber"].append(FriendNumberList(number_of_friends,date.today()).serialize())
        else:
            print("Data for today already exist")
            
        json.dump(data, json_file, sort_keys=True, indent=4)

    
if __name__ == "__main__":
    main()
