from bs4 import BeautifulSoup

#Helper method that finds the most recent company that a person has worked for and returns their time at the company in a string
#companyName should already be checked to ensure the right company is found
def getTimeAtCompany(soup, companyName):
    try:
        timeAtCompany = "None" #initilizes final return in case of error
        companyClass = soup.find(id='experience-section') #gets all education information
        allSummaries = companyClass.find_all('a', {'data-control-name': 'background_details_company'}) #quick summary of info for all jobs
    
         #goes through all jobs to find correct job listing
        for i in range(len(allSummaries)):
            postedCompany = allSummaries[i].find('p', {'class': 'pv-entity__secondary-title t-14 t-black t-normal'}) #gets the first type of company name
            
            #If the user has had multiple jobs at the company, name is under a different tag, so gets the different tag
            if postedCompany == None:
                postedCompany = allSummaries[i].find('h3', {'class': 't-16 t-black t-bold'}) #gets tag
                allSpans = postedCompany.find_all('span') #gets all span tags, one holds "Company Name", the other holds the actual company name
                postedCompany = allSpans[1].get_text().strip() #gets the actual company name
            
            #if user has only had one title at company, gets name of company
            else:
                postedCompany = postedCompany.get_text().strip() #gets all text
                newline = postedCompany.find('\n') #finds where the newline is, as after that is additional text
                postedCompany = postedCompany[:newline] #gets company name 
            
            #if the company name matches, gets time at company
            if (postedCompany == companyName):
                allSpans = allSummaries[i].find_all('span') #gets all span tags
                
                #looks at each span tag until the tags with the length of time are found
                for j in range (len(allSpans)):
                    if "mo" in allSpans[j].get_text().strip() or "yr" in allSpans[j].get_text().strip():
                        timeAtCompany = allSpans[j].get_text().strip()  #gets time at company from current page
                        break
                    
        return timeAtCompany
    
    #If there is a problem with finding the time at company, exits the method and retuns "N/A"
    except:
        return "None"
        
#Helper method that finds the age of the person by subtracting 2020 from the year they started their bachelors degree
def getAge(soup):
    try:
        age = 0 #initilizes final return in case of error
        educationClass = soup.find(id='education-section') #gets all education information
        allSchoolsGeneral = soup.find_all('div', {'class': 'pv-entity__summary-info pv-entity__summary-info--background-section'}) #gets a list of all general information of schools
        
        #looks at each school attended
        for i in range(len(allSchoolsGeneral)):
            allSpans =  allSchoolsGeneral[i].find_all(('span', {'class': 'visually-hidden'})) #finds all visually hidden tags, as degree name is a hidden tag
            
            #if current degree has the title Bachelor's, BA, BS, or Associates finds the start year of that school
            if "Bachelor" in allSpans[1].get_text().strip() or "BA" in  allSpans[1].get_text().strip() or "BS" in  allSpans[1].get_text().strip() or "Associate" in allSpans[1].get_text().strip():
                startYear = allSchoolsGeneral[i].find('time').get_text().strip() #gets start year of bachelors degree
                birthYear = int(startYear) - 18 #assuming they started college at 18, finds their birth year
                age = 2020 - int(birthYear) #finding their age by subtracting this year by their birth year
                
        return age #returns the age of the user    

     #If there is a problem with finding age, exits the method and retuns 0
    except:
        return 0

#Helper method that finds the user's alma mater by finding their bachelors degree and returns the name of their alma matter
def getCollege(soup):
    try:
        college = "None" #initilizes final return in case of error
        educationClass = soup.find(id='education-section') #gets all education information
        allSchools = educationClass.find_all('div', {'class': 'pv-entity__degree-info'}) #gets all basic information from schools attended
        
        #goes through all degrees to find bachelors degree
        for i in range(len(allSchools)):
            
            allSpans =  allSchools[i].find_all(('span', {'class': 'visually-hidden'})) #finds all visually hidden tags, as degree name is a hidden tag
            
            #if current degree has the title Bachelor's, BA, or BS, sets that as the Alma Mater and exits the loop
            if "Bachelor" in allSpans[1].get_text().strip() or "BA" in  allSpans[1].get_text().strip() or "BS" in  allSpans[1].get_text().strip(): 
                college = allSchools[i].find('h3', {'class': 'pv-entity__school-name t-16 t-black t-bold'}).get_text().strip()  #gets college
                
        return college #returns the alma mater
        
    #If there is a problem with finding the alma mater, exits the method and retuns "N/A"
    except:
        return "None"
        
#Cross checks name of company with what is posted in LinkedIn
def checkCompany(soup, userCompany):
    try:
        newCompany = userCompany #copy of company name so if anything goes wrong, the original company name is returned
        companyClass = soup.find(id='experience-section') #gets all education information
        allSummaries = companyClass.find_all('a', {'data-control-name': 'background_details_company'}) #quick summary of info for all jobs

         #goes through all jobs to find correct job listing
        for i in range(len(allSummaries)):
            postedCompany = allSummaries[i].find('p', {'class': 'pv-entity__secondary-title t-14 t-black t-normal'}) #gets the first type of company name
            
            #If the user has had multiple jobs at the company, name is under a different tag, so gets the different tag
            if postedCompany == None:
                postedCompany = allSummaries[i].find('h3', {'class': 't-16 t-black t-bold'}) #gets tag
                allSpans = postedCompany.find_all('span') #gets all span tags, one holds "Company Name", the other holds the actual company name
                postedCompany = allSpans[1].get_text().strip() #gets the actual company name
            
            #if user has only had one title at company, gets name of company
            else:
                postedCompany = postedCompany.get_text().strip() #gets all text
                newline = postedCompany.find('\n') #finds where the newline is, as after that is additional text
                postedCompany = postedCompany[:newline] #gets company name 
                
            #if the company does not match what is on Salesloft, updates company name
            if newCompany != postedCompany:
                newCompany = GenericCompanyNames(newCompany, postedCompany) #finds the generic form of the company
                
                #if company name now matches, returns updated form
                if (newCompany == postedCompany): 
                    return newCompany #returns the updated version of the company name
                
            #if the names match, returns the company name
            else:
                    return newCompany
            
    #If there is a problem with finding company name, exits the method and retuns "N/A"
    except:
        return userCompany
    
#If user's company name does not match with their linkedin profile, attempts a series of prefixes and suffixes on the company name until correct
def GenericCompanyNames(userCompany, postedCompany):
    
    suffixes = ["LLC", "Co", "Inc", "Agency", "Assn", "Assoc", "BV", "Comp", "Corp", "DMD", "Gmbh", "Group", "Intl", "LP", "LTD", "MFG", "PA", "PC", "PLC", "PLLC", "SA", "Svcs"] #list of generic company suffixes
    prefixes = ["The", "Dr"] #list of generic company prefixes
    
    found = False #loop break variable and return variable
    i = 0 #loop increment variable
    tempCompany = "" #temporary string to compare to
    
    
    comma = userCompany.find(',')
    if (comma != -1):
        userCompany = userCompany[:comma]
    
    #Goes through a list of generic suffixes to see if any of them cause match the one on the current page
    while i < suffixes.__len__() - 1 and found == False:
            
        tempCompany = userCompany + " " + suffixes[i] #temporary name
        
        #if the company name matches with the temporary name, updates company name and breaks loop
        if postedCompany == tempCompany:
            userCompany = tempCompany
            found = True
            
        #if the company name does not match, moves to the next suffix
        else:
            i = i + 1
            
    i = 0 #reset loop variable
    
    #Goes through a list of generic prefixes to see if any of them cause match the one on the current page
    while i < prefixes.__len__() and found == False:
    
        tempCompany =  prefixes[i] + " " + userCompany #temporary company name
        
         #if the company name matches with the temporary name, updates company name and breaks loop
        if postedCompany == tempCompany:
            found = True
        
        #if the company name does not match, moves to the next suffix
        else:
            i = i + 1

    #if the company name has still not been found, checks to see if the name on the page contains the original company name, and if it does, updates it to the company on the page
    tempPosted = postedCompany.lower()
    tempCompany = userCompany.lower()
    if found == False and ((tempCompany in tempPosted) or (tempPosted in tempCompany)):
        found = True
        userCompany = postedCompany #updates page name
        
    return userCompany #returns if the company name has updated