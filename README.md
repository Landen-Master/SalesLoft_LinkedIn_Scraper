# SalesLoft_LinkedIn_Scraper

This program reads in potential new clients from SalesLoft. The program goes through this list and finds the LinkedIn profile of any new users, goes to their profile, and finds helpful information such as age, alma mater, and time spent at their company. It then uploads this information back into SalesLoft under custom fields. 

## User Guide

This program is written in Python and uses the Chrome driver to scroll through LinkedIn pages. 

### Getting started
To start, you will need to create **data.txt**, a file that holds the following, each on its own separate line:
1. A LinkedIn email
2. The password to the LinkedIn account
3. A SalesLoft API key


### Running the program
To run the program, run the **main.py** file.

## For Future Developers

**main.py** - Main class that executes the program. Holds methods for getting and uploading to SalesLoft, checking if a user has been looked at before, and starting the scraping bot.

**helper_classes.py** - Holds class information on the current user being evaluated and the LinkedIn scraping bot. Holds methods for going to URLs, logging in, searching, scrolling on the page, and finding information on a new user. 

**scraping_methods.py** - Methods created for scraping specific information, including time at their company, age, alma mater, and if they still are employed by the company said in SalesLoft. In addition, there is a helper method to attempt to match the company stated on LinkedIn with the SalesLoft company by adding and removing generic prefixes and suffixes.

**data.txt** - Information needed to run the program, including a LinkedIn email, password, and SalesLoft API key.

**users.txt** - Information on users that have already been scraped. Used in main.py to check if a current user has been read before. If so, it will skip that user.
