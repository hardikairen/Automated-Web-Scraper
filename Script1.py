from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, NavigableString, Tag
import pandas as pd
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException
import csv
from selenium.webdriver.common.action_chains import ActionChains

#INPUT
#EMAIL_ID =   '***'
#PASSWORD =   '***'
#TARGET_NAME = '***'
#TARGET_URL = '***'


LOGIN_URL =  '***'
LOGOUT_URL = '***'

#FUNCTION FOR LOGIN
def login_now(driver,LOGIN_URL,EMAIL_ID,PASSWORD):

    #Login - Step-1
    driver.get(LOGIN_URL)
    u=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="overlay"]/div/div[1]/div/div[2]/form/div[2]/input')))
    u.send_keys(EMAIL_ID)

    time.sleep(5)
    continue_button =  WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="overlay"]/div/div[1]/div/div[2]/form/div[3]/button/span[1]/span[1]')))
    driver.implicitly_wait(10)
    continue_button.click()

    #Login - Step-2
    driver.implicitly_wait(10) 
    p=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="overlay"]/div/div[1]/div/div[3]/form/div[2]/div[2]/input')))

    driver.implicitly_wait(10)
    p.send_keys(PASSWORD)

    time.sleep(5)
    login_button=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="overlay"]/div/div[1]/div/div[3]/form/div[3]/button')))
    driver.implicitly_wait(10)
    login_button.click()
    driver.implicitly_wait(15)


#FUNCTION FOR LOGOUT
def logout_now(driver):
    driver.get(LOGOUT_URL)
    time.sleep(5)
    driver.quit()

    
  
def target_country(driver,TARGET_URL):
    time.sleep(10)
    driver.implicitly_wait(10)
    driver.get(TARGET_URL)
    show_all_element = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="show_all"]')))
    show_all_element.click()
    while True:
        time.sleep(15)
        button = driver.find_elements_by_xpath('//*[@id="load-more"]/a')
        if len(button)<1:
            print('no university pages left')
            break
        else:
            print('Clicking Load More.')
            load_more = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="load-more"]/a')))
            ActionChains(driver).move_to_element(load_more).click(load_more).perform()
            
    all_univ_links = []
    soup = BeautifulSoup(driver.page_source , 'html.parser')
    count=1
    for i in soup.select('p.lead.text-center.card-top-head'):   #get links 
        for j in i.select("a"):
            print(count,j['href'])
            all_univ_links.append(str(j['href']))
            count=count+1
 
    def get_unique_univ(x):
        return list(dict.fromkeys(x))

    all_links = get_unique_univ(all_univ_links)
    first_page_url=[]
    count=1
    for i in all_links:
        name = i.split('/')[4]
        number = name.split('-')[-1]
        x = name.replace('-'+ str(number),'')
        url =  '***'+x+'***'
        first_page_url.append(url)
        count=count+1
        
    return first_page_url

                  
def get_all_student_profile_links(driver,TARGET_COUNTRY,CSV_FILE_NAME):
    try:
        page_soup = BeautifulSoup(driver.page_source, 'html.parser')
        each_univ_student_links = page_soup.select('div.panel-body')
        
    except Exception as e:
        print('Page Soup error')
        print(e)
    
    for i in each_univ_student_links:
        count=1
        student_row = []
        for link in i.select('a'):
            try:
                profilelink =  link['href']
                profilelink = profilelink.strip()
                profilelink = profilelink.split("/")
                profilelink = profilelink[2]
                print(profilelink)
                student_row.append(profilelink)
            except Exception as err:
                print(err)
            student_row.append(TARGET_COUNTRY)
            
        for univ in i.select('small'):
            data = univ.text
            student_row.append(str(data.strip()))
                    
        for decision in i.select('label'):
            student_row.append(str(decision.text).strip())
                               
        for data in i.select('div.col-sm-3.col-xs-6'):
            details = str(data.text)
            student_row.append(details.strip())

        file_exists = os.path.isfile(CSV_FILE_NAME)
        headers =   ['***'  , '***' , '*** ***,*** *** ***' ,'***','***',
                             '***','*** ***','*** ***.']

        try:      
            with open (CSV_FILE_NAME,'a',newline="") as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(headers)  # file doesn't exist yet, write a header
                    writer.writerow(student_row)
                else:
                    writer.writerow(student_row)
        except Exception as e:
            print('Error in writing into csv')
            print(e)


#FUNCTION OF NAVIGATE THROUGH ALL PAGES
def navigate_through_pages(driver,first_page_urls,TARGET_COUNTRY,CSV_FILE_NAME):
    all_student_profile_links=[]
    x=1
    for next_url in first_page_urls:
        try:
            time.sleep(10)
            driver.implicitly_wait(15)
            count=1
            while True:
                url = str(next_url.split('?')[0]) + '?' + 'page=' + str(count)
                time.sleep(25)
                driver.get(url)
                driver.implicitly_wait(10)
                if driver.title=='***':
                    x=x-1
                    break

                currenturl = driver.current_url
                print(currenturl)
                try:
                    get_all_student_profile_links(driver,TARGET_COUNTRY,CSV_FILE_NAME)
                    #with open(TARGET_COUNTRY + 'CompletedPages.txt', 'a') as f:
                     #   f.write("%s\n" % currenturl)

                except Exception as e:
                    print(e)
                    print('Error in getting profile links on a page')

                count=count+1
            x=x+1
        except Exception as e:
            print('Error in getting page url')

#MAIN
def main_profile_links(EMAIL_ID,PASSWORD,TARGET_COUNTRY,TARGET_URL):
    
    #OUTPUT FILE NAME
    CSV_FILE_NAME = TARGET_COUNTRY + 'ProfileLinks.csv'

    #MAKE A DRIVER SESSION
    chrome_options = Options()
    prefs = {"profile.default_content_setting_values.notifications" : 2}  #block notifications
    chrome_options.add_experimental_option("prefs",prefs)
    #PROXY = { "103.194.192.29": "60165"}
    #chrome_options.add_argument('--proxy-server=%s' % PROXY)
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
     
    #LOGIN
    try:
        login_now(driver,LOGIN_URL,EMAIL_ID,PASSWORD)
        time.sleep(10)
    except Exception as e:
        print('Error in login. Problem in WebDriver or Wrong Credentials')
        print(e)
        driver.quit()
        
    #TARGET COUNTRY
    first_page_urls = target_country(driver,TARGET_URL)
    time.sleep(20)

    #GET PROFILE URLS
    navigate_through_pages(driver, first_page_urls,TARGET_COUNTRY,CSV_FILE_NAME)
    time.sleep(20)

    #LOGOUT
    logout_now(driver)




   


 

 
