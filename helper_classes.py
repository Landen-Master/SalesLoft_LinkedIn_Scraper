#User profile from Salesloft API to find on LinkedIn
import selenium
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys #library that automates browser tasks
import time
import requests #importing requests to call APIs
from idlelib import browser
from html.parser import HTMLParser
import random
import scraping_methods
from _ast import Try
from selenium.common.exceptions import NoSuchAttributeException
from distutils.command.check import check
from builtins import none

class CurrentUser:
    age = 0 #age of user
    timeAtCompany = "" #years and months spent at the current company
    college = "" #name of user's college
    family_In_Company = False #finding if there is a family member in the company
    changed = False #checks if company name is different than the one on LinkedIn
    def __init__(self, name, company, url, id):
        self.name = name #setting the name of the current user
        self.company = company #setting the company of the current user
        self.url = url #if the user has a URL, includes their linkedin URL
        self.id = id #id from SalesLoft
        
#LinkedIn Bot class that the scraping service runs on
class LinkedInBot:

    #initializes bot as a using Google Chrome, creates necessary URLs, and set user name and password
    def __init__(self, username, password):
        
        self.driver = selenium.webdriver.Chrome('./chromedriver.exe') #initializes the bot as using Google Chrome
        
        self.base_url = 'https://www.linkedin.com' #web site to navigate
        self.login_url = self.base_url + '/login' #URL to log into
        self.feed_url = self.base_url + '/feed' #TODO: is this needed?
        self.search_people_url = self.base_url + '/search//results/all/?keywords' #TODO: see how this does

        self.username = username #sets username of account
        self.password = password #sets password of account
        
    #Goes to a specific URL on Google Chrome
    def GoTo(self, url):
        self.driver.get(url) #goes to specific URL
        time.sleep(2) #waits for the page to load
        
    #logs into LinkedIn Account
    def Login(self):
        self.driver.get(self.login_url) #goes to log-in page
        time.sleep(2)
        
        #logs into linkedin through inputting username and password
        try:
            self.driver.find_element_by_id('username').send_keys(self.username) #inputs username
            self.driver.find_element_by_id('password').send_keys(self.password) #inputs password
            self.driver.find_element_by_id('password').send_keys(Keys.RETURN)
            time.sleep(2) #waits for the page to load
            
        
        #if there is an error logging in, prints an error message and quits
        except NoSuchAttributeException:
            print("Error logging in")
            quit()
        
    #Searches from feed
    def Search(self, person, connect=False):
        self.driver.get(self.feed_url) #goes to main feed
        time.sleep(1) #wait for page to load
        
        #attempts to find person
        try:
            search = self.driver.find_element_by_class_name('search-global-typeahead__input') #navigates to the search bar
            search.send_keys(person.name) #enters text into search bar
            search.send_keys(Keys.ENTER) #presses enter after text is inputted
            time.sleep(3) #waits for the page to load
            
            self.driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div[1]/nav/div/div[1]/div/div[2]/ul/li[1]/button').click() #narrows it down to people
            time.sleep(3) #waits for the page to load again
            
            soup = BeautifulSoup(self.driver.page_source, 'lxml') #loads page source
            allPeople = soup.find_all('li', {'class': 'reusable-search__result-container'}) #gets all profile cards on the search page
            
            #loops through all people on the page to find the user's linkedin url
            for i in allPeople:
                name = i.find('span', {'dir': 'ltr'}).get_text().strip() #gets the name of the next user on the page
                title = i.find('div', {'class': 'entity-result__primary-subtitle t-14 t-black'}).get_text().strip() #gets the title of the next user on the page

                #if the names match, and the company is in their title, sets the url and exits the loop
                if (person.name in name) and (person.company in title):
                    person.url = i.find('a', {'class': 'app-aware-link ember-view'}).get('href').strip() #gets the url
                    print(person.url)
                    break; #breaks the loop
                
        #if any errors happen, prints error and quits program
        except NoSuchAttributeException:
            print("Error searching user")
            quit()
        
    def ScrollThroughPage(self):
        
        current_height = self.driver.execute_script("return document.body.scrollHeight") #height of web page before loading
        
        time.sleep(random.randrange(4, 6)) #waits so LinkedIn does not get suspicious and for the page to load
        
        randomConnect = random.randrange(1, 100) #picks a random number
        
        #gives a 5% chance to connect so it looks less suspicious
        if randomConnect >= 95:
            try:
                #finding the number connection
                soup = BeautifulSoup(self.driver.page_source, 'lxml') #loads page source
                header = soup.find('ul', {'class': 'pv-top-card--list inline-flex align-items-center'}) #gets the header information
                connection = header.find('span', {'class': 'dist-value'}).get_text().strip() #gets the type of connection
                
                #if the connetion is 3rd+, the connect button does not appear. To connect, there is a button on a dropdown menu, and this will follow that to connect
                if connection == '3rd':
                    
                    #clicking the dropdown menue
                    dropdown = self.driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[1]/div[2]/div/div/div[2]/div') #clicks the drop down menue
                    self.driver.execute_script("arguments[0].click();", dropdown)
                    time.sleep(random.randrange(1, 3)) #waits for drop down menue to load
                    
                    #clicking the connect button on the dropdown
                    connect = self.driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div/ul/li[4]/div/div')
                    self.driver.execute_script("arguments[0].click();", connect)
                    time.sleep(random.randrange(1, 3)) #waits for connection to pop up
                    
                    self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click() #connects with the user
                        
                #if the user is a 2nd connection, there is a button to connect, and clicks it
                elif connection == '2nd':
                    self.driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[1]/div[2]/div/div/div[1]/div/button').click() #clicks the connect button
                    self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click() #connects with the user
            
            #if anything goes wrong or if there is a pending connection, quits the attempt
            except:
                print('Pending or error')
                print('haha')
                     
        #continues to scroll down on the page until all is loaded
        for i in range(4):
            self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)/2)") #scrolls to the bottem of the current page
            
            time.sleep(random.randrange(4, 6)) #waits so LinkedIn does not get suspicious and for the page to load

            new_height = self.driver.execute_script("document.body.scrollHeight") #finds the new height o fthe page  
            
            #if there is no more page to load, break the loop
            if new_height == new_height:
                break
            #if page still needs to load, updates new height
            else:
                new_height = new_height
                
    #webscraping function that updates information
    def NewInfo(self, person):
        
         #if the person does not have a LinkedIn URL, searches them on LinkedIn
        if (person.url == "None"):
            self.Search(person) #using the search function to find the person
            
        #If the person's URL has been found, updates their information
        if (person.url != "None"):
            
            #attempts to get user's source code for their LinkedIn page
            try:
                self.driver.get(person.url) #goes to the URL of the person
                self.ScrollThroughPage() #scrolls through the page to get all of their information
                source = self.driver.page_source #gets the page source
                soup = BeautifulSoup(source, 'lxml') #gets the current page as lxml code
            except:
                print("Error getting soup")
                return
            
            #finding information on user
            checkChange = perosn.company #checks if company name changes
            person.company = scraping_methods.checkCompany(soup, person.company) #checks the persons current company
            
            #if change has occured in the company name, sets changed to true
            if checkChange != person.company and person.company != None:
                person.changed = True
            
            person.college = scraping_methods.getCollege(soup) #gets the persons alma mater
            person.age = scraping_methods.getAge(soup) #gets the persons age
            person.timeAtCompany = scraping_methods.getTimeAtCompany(soup, person.company) #gets the persons time at the company
