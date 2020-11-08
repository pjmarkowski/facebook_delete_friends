import sys 
import os 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(chrome_options=options,executable_path=r'/Users/piotrmar/piotr/Projekty/tools/chromedriver')
    driver.get("http://www.facebook.com")
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="u_0_h"]').click() # accept cookies
    username = os.getenv('FB_USERNAME')
    password = os.getenv('FB_PASS')
    print(password)
    driver.find_element_by_id('email').send_keys(username)
    driver.find_element_by_id('pass').send_keys(password)
    driver.find_element_by_name('login').click()

if __name__ == "__main__":
    main()
