#using selenium
import selenium.webdriver as webdriver #allows automation of web interactions
from selenium.webdriver.chrome.service import Service #manages the webdriver
import time
from bs4 import BeautifulSoup
import re

def scrape(website):
    print('Launchung chrome browser..')

    chrome_driver_path = './chromedriver.exe' #has the path for the chrome web driver
    options = webdriver.ChromeOptions() #any options like disabling images etc.
    options.add_argument('--ignore-certificate-errors') #to avoid ssl problems
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--headless') #to avoid csp restrictions (content security policy)
    options.add_argument('--inprivate') #websites can chill with their security for private browsing
    options.add_argument("--guest")  # Run in guest mode
    options.add_argument("--disable-features=EdgeWebAuthentication")  # Disable authentication



    #run a virtual broswer with path as the set path and the options to be the options set above
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options = options) 
    #driver can do the following:
    '''driver.get to navigate to website
        driver.find_element.text (for finding text in tags just like bs4)
        button = driver.find_element()
        button.click() //clicks the buttons
    '''

    try:
        driver.get(website) #get to the website
        print('page loaded')
        html = driver.page_source #return the html of said website
        time.sleep(5)
        return html
    
    
    finally: #cleanup function
        driver.quit()


#cleaning the html

#getting only the body of the html 
def extract_body(html):
    doc = BeautifulSoup(html, 'html.parser')
    body_content = doc.body
    if body_content:
        return str(body_content)
    else:
        return ''


#cleaning the body
def cleaning(body_content):
    doc = BeautifulSoup(body_content, 'html.parser') # reparse the content passed
    for content in doc(['script', 'style']):
        content.extract() # removes all <script> and <style> elements

    cleaned = doc.get_text(separator="\n") # converts remaining HTML into plain text with new line as a separator
    cleaned = "\n".join(line.strip() for line in cleaned.splitlines() if line.strip())
    # splitlines() breaks the text into separate lines
    # strip() removes leading and trailing whitespace from each line
    # rejoin the stripped and fixed lines with "\n"

    return cleaned

#AI have token limits

def splittingcontent(dom, max = 6000): #dom is the content being passed to ai
    #max is maximum no. of characters passable to AI
    
    #split content into batches of 6000 words
    return [dom[i: i + max] for i in range(0, len(dom), max)]
                            #the range steps up by max length each time so that each time for loop runs, runs on next 6000 words
    

