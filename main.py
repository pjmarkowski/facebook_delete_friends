# -*- coding: utf-8 -*-
import sys 
import os 
import json
import time
import codecs
from datetime import date, timedelta
from models import FriendNumberList, friend_number_list_from_json, friend_from_json, Friend
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC


data = {}
data["FriendsNumber"]=[]
data["FriendsList"]=[]
data["DeleteFriendList"]=[]
friendnumbers = []
friends_html = 'database/index.html'

# def main():
    
    # scroll_down_until_friends_number(number_of_friends)
    # with open (friends_html, 'w') as f:
    #     f.write(driver.page_source)
    #     print('%s) Downloaded' % friends_html)

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


def parse_friends():
    # # print(os.getcwd() + '/' + friends_html)
    # print(os.getcwd() + '/' + 'database/index1200friends.html')
    # driver.get('file:///' + os.getcwd() + '/' + friends_html)
    list_of_friends = driver.find_elements_by_class_name('gfomwglr')
    print(len(list_of_friends))
    div_fb_link_counter = 1
    for e in list_of_friends:
        try:
            mutual_friends_number = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div[3]/div['+str(div_fb_link_counter)+']/div[2]/div[2]/span/div/div/a').text.split()
        except:
            print("No mutual friends")
            mutual_friends_number[0] = "0"
        try:
            text = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div[3]/div['+str(div_fb_link_counter)+']/div[2]/div[1]/a/span').text
            link = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div[3]/div['+str(div_fb_link_counter)+']/div[2]/div[1]/a').get_attribute('href')
            
            x = text.split()
            name = ''
            for i in x[:-1]:
                name += i
            surname = x[-1]
            create_friends_list(Friend(name, surname, mutual_friends_number[0],link))
        except:
            print("ELement not found")
        div_fb_link_counter += 1

        



def create_friends_list(friend):
    global data
    try:
        with codecs.open('database/friends_list.json', encoding='utf8') as json_file:
            data["FriendsList"] = json.load(json_file)
    except:
        print("There was no file")

    with codecs.open('database/friends_list.json', 'w', encoding='utf8') as json_file:
        should_add = True
        for d in data["FriendsList"]:
            if (d.get("link") == friend.link):
                should_add = False
        
        if should_add:
            data["FriendsList"].append(friend.serialize())
            print("User added to the list: " + friend.get_full_name())
        else:
            print("This user already on the list: " + friend.get_full_name())
            
        json.dump(data["FriendsList"], json_file, sort_keys=True, indent=4, ensure_ascii=False)


def start_browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(options=options,executable_path=r'/Users/piotrmar/piotr/Projekty/tools/chromedriver')
    return driver

def login_to_facebook():
    driver.get("http://www.facebook.com")
    driver.implicitly_wait(30)
    driver.find_element_by_xpath('//*[@id="u_0_h"]').click() # accept cookies
    username = os.getenv('FB_USERNAME')
    password = os.getenv('FB_PASS')
    time.sleep(3)
    driver.find_element_by_id('email').send_keys(username)
    driver.find_element_by_id('pass').send_keys(password)
    driver.find_element_by_name('login').click()
    driver.implicitly_wait(30)

def get_number_of_friends():
    driver.get("http://www.facebook.com/piotr.markowski.904/friends")
    number_of_friends = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/div/a[3]/div/span/span[2]')
    return number_of_friends.text    

def scroll_down_until_friends_number(friends_number):
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            friends_on_page = driver.find_elements_by_class_name('gfomwglr')
            if len(friends_on_page) > friends_number:
                print("End of the page")
                print("SCROLL TIME--- %s seconds ---" % (time.time() - start_time))
                break
        last_height = new_height

def create_friends_list_to_delete():
    try:
        with codecs.open('database/friends_list_my_final.json', encoding='utf8') as json_file:
            data["DeleteFriendList"] = json.load(json_file)
    except:
        print("There was no file")

    print("Number of friends on this list: %s" % len(data["DeleteFriendList"]))
    driver.get("http://www.facebook.com/piotr.markowski.904/friends")
    div_fb_link_counter = 1
    list_of_friends = driver.find_elements_by_class_name('gfomwglr')
    print("in loop: %s" % len(list_of_friends))
    element = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div[1]')
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(3)
    number_to_delete = 200
    already_deleted = 0
    a = 1
    b = 9
    while already_deleted < number_to_delete:	
        for x in range(a,b):
            try:
                link = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div[3]/div['+str(div_fb_link_counter)+']/div[2]/div[1]/a').get_attribute('href')
                print("Trying %s " % link)
                exist = False
                for e in data["DeleteFriendList"]:
                    if link == e.get("link"):
                        exist = True

                if exist==False:  
                    print("DELETE: %s" % link)
                    friends_button = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div[3]/div['+str(div_fb_link_counter)+']/div[3]')
                    friends_button.click()
                    time.sleep(2)
                    try:
                        delete_button_4place= driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/div/div[4]')
                        delete_button_4place.click()
                    except:
                        try:
                            usun_button_3place = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/div/div[3]')
                            usun_button_3place.click()
                        except:
                            usun_button_1place = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/div/div')
                            usun_button_1place.click()
                    time.sleep(2)
                    potwierdz_button = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div/div[1]')
                    potwierdz_button.click()
                    time.sleep(2)
                    already_deleted += 1
            except:
                print("Was not able to find href for %s" % div_fb_link_counter)
            
            div_fb_link_counter += 1
        try:
            element = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div[3]/div['+str(b-2)+']') 
            driver.execute_script("arguments[0].scrollIntoView();", element)
        except:
            print("Scroll down failed... %s" % str(b-2))
            driver.execute_script("arguments[0].scrollIntoView();", element)
        a += 8
        b += 8
        time.sleep(3)
    print("Deleted: %s" % already_deleted)
    
        



if __name__ == "__main__":
    start_time = time.time()

    driver = start_browser()
    print("1.Update your number of friends for today")
    print("2.Get list of all friends")
    print("3.Delete friends from list")

    option = input("What do you want to do ?")
    if  option == '1': 
        print("Starting update of your friends number...")
        login_to_facebook()    
        number_of_friends = get_number_of_friends()
        add_to_friend_list(number_of_friends)
    elif option == '2':
        print("Getting all of the friends...")
        login_to_facebook()
        time.sleep(3)
        number_of_friends = get_number_of_friends()
        scroll_down_until_friends_number(int(number_of_friends))
        parse_friends()
        print("--- %s seconds ---" % (time.time() - start_time))
    elif option == '3':
        print("Reading list to delete:")
        login_to_facebook()
        time.sleep(3)
        create_friends_list_to_delete()
        print("--- %s seconds ---" % (time.time() - start_time))
    elif option == 'q':
        print("Exit!")
        driver.quit()
        sys.exit()

    else:
        print("Wrong number!")
    # main()
    # parse_friends()