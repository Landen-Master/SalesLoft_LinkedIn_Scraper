#importing libraries
import requests #importing requests to call APIs
import configparser #library that stores credentials locally instead of on github/in code
from selenium import webdriver #library that automates browser tasks
from test.test_robotparser import PasswordProtectedSiteTestCase
import helper_classes
from sys import prefix
import selenium
from bs4 import BeautifulSoup
import random
import webbrowser
import os, sys
from urllib.parse import urlparse
from nt import link
from asyncio.tasks import wait
import time
import json

session = requests.Session() #gets a session to interact with the Salesloft API

#Helper class for final upload of custom fields
class customFieldHolder:
    age = 'Age: Unknown'
    timeAtCompany = 'Time at Company: Unknown'
    college = 'Alma Mater: Unknown'


#Helper Function that gets all JSON files that contain user information from Salesloft API
def GetUsers(head, url):
    first_page = session.get(url, headers=head).json() #gets the JSON file of the first page
    yield first_page #returns first page for first iteration
    total_pages = first_page['metadata']['paging']['total_pages'] #gets the rest of the information
    
    #if there are more than 1 page, gets the rest of the pages of information
    if total_pages > 1:
        for page in range(2, total_pages + 1):
            next_page = session.get(url, headers=head, params = {'page': page}).json() #gets the JSON file of the next page
            yield next_page #returns the new page
            
#Function takes all JSON files of SalesLoft Users and returns an array
def GetList(key, url, checked):
    users = [] #list of Users to find
    #runs through all SalesLoft users it can before it reaches problematic points
    try:
        head = {'Authorization': 'Bearer ' + key} #parameters passed in to search SalesLoft API
        for page in GetUsers(head, url):     #uses helper function to get all users
            for person in page['data']: #gets all users from current page
                first = person['first_name'] #gets current person's name
                last = person['last_name']
                if first != None and last != None:
                    name = first + ' ' + last
                    company = person['person_company_name'] #get current person's company
                    url = str(person['linkedin_url']) #get current person's LinkedIn URL
                    id = person['id']
                    newUser = helper_classes.CurrentUser(name, company, url, id) #initilizes a new user for this current person
                    if id not in checked: #if user has not been checked, adds them to the list
                        users.append(newUser) #adds it to the list

    except: #once the list is done, returns the final list
        return users 

#Uploads data from Linkedin back into Salesloft for future reference
def uploadUserData(users, key):
            
    salesloft_head = {'Authorization': 'Bearer ' + key} #gets the main hearer for Salesloft uploads
    ageParam = 'custom_fields[MailMerge Text 10]' #parameter to store the age of the user
    timeParam = 'custom_fields[MailMerge Text 11]' #parameter to store the time the user has worked at their company
    collegeParam = 'custom_fields[MailMerge Text 12]' #parameter to store the users college
    
    #uploads all users one at a time
    for x in users:
        temp = customFieldHolder() #uses temporary helper class to finalize upload data
        url = 'https://api.salesloft.com/v2/people/' + str(x.id) + '.json' #url of user being accessed
        newInfo = False
        
        #series of ifstatements that assign values to the temporary value if they are valid
        if (x.age != 0 and x.age != None):
            temp.age = 'Age: ' + str(x.age)
            newInfo = True
        if (x.timeAtCompany != 'None' and x.timeAtCompany != None):
            temp.timeAtCompany = 'Time at Company: ' + x.timeAtCompany
            newInfo = True
        if (x.college != 'None' and x.college != None):
            temp.college = 'Alma Mater: ' + x.college
            newInfo = True
            
        #if there is new data to upload, uploads it
        if (newInfo):
            
            #adding custom fields to unused fields
            custom_fields8 = {"MailMerge Text 3" : temp.age, "Marketing Initiative" : temp.timeAtCompany, "MailMerge Text 4" : temp.college}

            #parameters to use to push to SalesLoft
            params = {'id' : str(x.id), 'custom_fields[MailMerge Text 3]' : temp.age, 'custom_fields[Marketing Initiative]' : temp.timeAtCompany, 'custom_fields[MailMerge Text 4]' : temp.college} 

            session.put(url, params=params, headers=salesloft_head).json() #uploading the data
            
#main function, where all subfunctions are called
def main():
    
    url = 'https://api.salesloft.com/v2/people.json?per_page=100&include_paging_counts=true' #SalesLoft API URL
    
    checked = [] #list of checked IDs
    
    #reading in data file for information
    try:
        
        #getting login and Oauth data
        file = open('data.txt', 'r') #opens local data file with username, password, and key
        username = file.readline() #gets the username from the first line
        password = file.readline() #gets password from second line
        key = file.read() #gets OAUTH key from the last line
        file.close() #closing first file
        
        #reading in past users to not repeat information
        file = open('users.txt', 'r') #opens local data file with all user info
        for line in file:
            line = int(line[0:8]) #gets the first 8 digits from the file, that being the use ID
            checked.append(line) #adds the id to the list of checked ids 
        file.close() #closing second file
        
    except: #if the file can not be read, prints error and quits
        print('Can not read from file')
        quit();
    
    users = GetList(key, url) #gets a list of all users with valid LinkedIn URLS
    
    #if there are users, finds them on LinkedIn and updates information
    if users.__sizeof__() > 0:
        bot = helper_classes.LinkedInBot(username, password) #Creating LinkedIn Bot to get information
         
    #If there are no Users, prints error statement and quits
    else:
        print('Can not get users')
        quit()
          
    #opening the file to write user data to
    try:
        file = open('users.txt', 'a') #list of users succefully read so far
    except:
        print('Error writing to file')
        quit()
    
    #reads in LinekdIn Data by creating a bot and looking on LinkedIn
    try:
        bot.Login() #logs bot onto linkedin
        for current in users:
            time.sleep(random.randrange(4, 10)) #waits so LinkedIn does not get suspicious
            bot.NewInfo(current) #testing newinfo function
        
        #if the major information is still valid, prints all attributes to a file
        if (current.name != 'None' and  current.company != 'None' and current.url!= 'None'):
            file.write("%d, %s, %s, %s, %s, %s, %d\n" % (current.id, current.name, current.company, current.url, current.timeAtCompany, current.college, current.age))
    
        file.close()
    except: #if the LinkedIn Bot can not 
         print('Error using LinkedIn Bot')
         quit()
                
    uploadUserData(users, key) #uploads found data into Salesloft

# if the current module is the main module, runs the main code
if __name__ == '__main__':
    main()