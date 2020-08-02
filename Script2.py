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
from selenium.webdriver.common.action_chains import ActionChains
import csv
import pyautogui

#INPUT
#EMAIL_ID 
#PASSWORD
#PROFILE_LINKS_FILE_LIST = [*****]
#ADMIT_REJECT_DATA = "*****"
#EXISTING_DATA = '*****'

LOGIN_URL =  '*****'
LOGOUT_URL = '*****'


#FUNCTION FOR LOGIN
def login_now(driver,LOGIN_URL,EMAIL_ID,PASSWORD):

    #Login - Step-1
    driver.get(LOGIN_URL)
    driver.refresh()
    u=WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="overlay"]/div/div[1]/div/div[2]/form/div[2]/input')))
    u.send_keys(EMAIL_ID)

    time.sleep(10)
    continue_button =  WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="overlay"]/div/div[1]/div/div[2]/form/div[3]/button/span[1]/span[1]')))
    driver.implicitly_wait(15)
    continue_button.click()

    #Login - Step-2
    driver.implicitly_wait(10) 
    p=WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="overlay"]/div/div[1]/div/div[3]/form/div[2]/div[2]/input')))

    driver.implicitly_wait(15)
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
    
def get_student_data(driver,profile_url,country,ADMIT_REJECT_DATA):
    
    data=[]
    data.append('*****')
    data.append(country)
    data.append(profile_url)
    count=0
    time.sleep(7)
    try:
        student_soup = BeautifulSoup(driver.page_source, 'html.parser')
    except Exception as e:
        print('Page Soup error')
        print(e)
        
    try:
        data1 = student_soup.select('div.col-sm-12')[2]
    except Exception as e:
        print('Soup error',e)

    try:
        for i in data1.select('h1'):     #***** *****
            name = i.text
            name = name.split('@')
            print(count,name[0].strip())    
            count+=1
            data.append(name[0].strip())
            
    except Exception as e:
        print('Name Error',e)
        data.append(' ')
          
    try:        
        for j in data1.select('h3'):    #***** *****
            dream_univ = j.text
            remove_words = ['*****','*****','*****','*****']
            for word in remove_words:
                dream_univ = dream_univ.replace(word,'')
            print(count,dream_univ.strip())
            count+=1
            data.append(dream_univ.strip())
            
    except Exception as e:
        print("dream Univ Error",e)
        data.append(' ')

    try:        
        for k in data1.select('h4'):                       #***** *****
            course = (k.text).replace('Interested in','')
            course = course.strip()
            course = course[0:len(course)-1]
            index = course.find('Fall')
            if index!=-1:
                program = course[:(index-1)]
                print(count,program)
                count+=1
                data.append(program.strip())
                print(count,'Fall')
                count+=1
                data.append('Fall')
                year = course[ (index+5) : ]
                print(count,year.strip())
                count+=1
                data.append(year.strip())

            else:
                index = course.find('Spring')
                program = course[:(index-1)]
                print(count,program)
                count+=1
                data.append(program.strip())
                data.append('Spring')
                print(count,'Spring')
                count+=1
                year = course[(index+7) :]
                print(count,year.strip())
                data.append(year.strip())
                count+=1
           
    except Exception as e:
        print('Dream Course Error',e)
        data.append(' ')
        data.append(' ')
        data.append(' ')
        
    try:
        data2 = student_soup.select('div.col-sm-3.col-xs-3')
    except Exception as e:
        print('Basic Details 2 soup error',e)

    try:
        x=0
        for d in data2:                                        #Exam scores,Work Exp. , Tech papers
            val=''
            for j in d.find_all('h4'):
                if isinstance(j, NavigableString):
                   continue
                if isinstance(j, Tag):
                    val = str(j.text).strip()
                    word_list = ['GRE/GMAT','/','ENG TEST','IELTS/TOEFL','IELTS','TOEFL','Work Exp.','Tech Papers','TOEFL','IELTS','GRE','GMAT']
                    for word in word_list:
                        val=val.replace(word,'')
                    val=val.strip()
                    
                    if x==0:
                        val = val.replace(' ','')
                        val = val.replace('Quant:',' ')
                        val = val.replace('Verbal:',' ')
                        val = val.split(' ')
                        if len(val)==1:
                            print(val[0].strip())
                            data.append(val[0].strip())
                            data.append(' ')
                            data.append(' ')
                        else:
                            print(count,val[0].strip())
                            print(val[1].strip())
                            print(val[2].strip())
                            data.append(val[0].strip())
                            data.append(val[1].strip())
                            data.append(val[2].strip())
                            
                    elif x==1:
                        try:
                            val = val.strip()
                            if val=='NA':
                                data.append(' ')
                                data.append(' ')
                                data.append(val)
                                print(count,val)
                            elif float(val)>9:
                                data.append(' ')
                                data.append(float(val))
                                data.append(' ')
                                print(count,float(val))
                            else:
                                data.append(float(val))
                                data.append(' ')
                                data.append(' ')
                                print(count,float(val))
                                
                        except Exception as e:
                            print('Error in English Exam score')
                            print(e)
                            data.append(' ')
                            data.append(' ')
                            data.append(' ')
                    else:
                        try:
                            print(count,val)
                            data.append(val)
                        except:
                            data.append(' ')
                            
                    count+=1
                    
            x+=1
                
    except Exception as e:
        print('Exam scores error',e)

    try:  
        for d in data2[4]:                                      #UG details
            if isinstance(d, NavigableString):
                continue
            if isinstance(d, Tag):
                ug = str(d.text).strip()
                print(count,ug)
                count+=1
                data.append(ug)
    except Exception as e:
        print('UG score error',e)
        print(e)
        data.append(' ')
        data.append(' ')

    try:
        grad_data = student_soup.select('div.col-sm-9.col-xs-9')
    except Exception as e:
        print('UG details Soup Error',e)

    try:
        for i in grad_data:
            for j in i.find_all('p'):
                graddetails = str(j.text).strip()
                print(count,graddetails)
                count+=1
                data.append(graddetails)
                
    except Exception as e:
        print('UG Details Loop Error' , e)
        print(e)
        data.append(' ')
        data.append(' ')
        data.append(' ')

    table_data = student_soup.find('table',{'class':'table'})   #Universities Applied
    for row in table_data.find_all('tr'):
        datalist=[]
        try:
            for i in data:
                datalist.append(i)
           
            for name in row.select('h4'):

                for m in name.select('a'):
                    univname = m.text.strip()
                for n in name.select('small'):
                    coursename = n.text.strip()

            coursename = coursename.replace(',','')
            univname = univname.replace(coursename,'')
            datalist.append(univname.strip())
            datalist.append(coursename.strip())
                   
            for info in row.select('div.row'):
                temp=0
                apply_date=''
                decision_date=''
                comment=''
                for dates in info.find_all('strong'):
                    if temp==0:
                        apply_date = dates.text.strip()
                        
                    if temp==1:
                        decision_date = dates.text.strip()
                        
                    temp+=1
                
                for comments in info.select('div.col-sm-12'):
                    comment = str(comments.text).strip()

            if apply_date=='':
                datalist.append(str(' '))
            else:
                datalist.append(apply_date)

            if decision_date=='':
                datalist.append(str(' '))
            else:
                datalist.append(decision_date)
                            
            if comment == '':
                datalist.append(str(' '))
            else:
                datalist.append(comment)
                    
            for result in row.select('td.text-center'):
                decision = result.text.strip()
                datalist.append(decision)
        except Exception as e:
            print(e)
            print("Error in Univ. Applied Table data")
            for i in range(0,28):
                datalist.append(' ')
        
        print(datalist)
        
        file_exists = os.path.isfile(ADMIT_REJECT_DATA)
        headers = ['Source' , 'Country' , '*****','Student Name' ,'Dream University','Dream Program','Intake','Intake Year','GRE/GMAT Total',
                   'Quant','Verbal','IELTS','TOEFL','IELTS/TOEFL','Work Experience','Tech Paper', 'UG Score','CGPA/%','UG Program','UG College','UG College City',
                   'University Applied','Course','Apply Date','Decision Date','Comments','Status']
                
        with open (ADMIT_REJECT_DATA,'a',newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                try:
                    writer.writerow(headers)  # file doesn't exist yet, write a header
                    writer.writerow(datalist)
                except Exception as e:
                    print('CSV write error',e)
            else:
                try:
                    writer.writerow(datalist)
                except Exception as e:
                    print('CSV write error',e)

def get_data_now(driver,all_student_profile_links,ADMIT_REJECT_DATA):
    
    for index,row in all_student_profile_links.iterrows():
        url = '*****' + row['*****']
        print(row['Country'],url)
        try:
            time.sleep(17)
            driver.get(url)    
        except Exception as e:
            print("Error in loading...")
            print(e)
         
        try:
            get_student_data(driver,row['*****'],row['Country'],ADMIT_REJECT_DATA)
        except Exception as e:
            print("Error in getting data...")
            print(e)

def remove_duplicates(df):
 
    df = df[['Country','*****']]
    df.drop_duplicates(subset ="*****", inplace = True)
    print(df.describe())
    return df

def open_file (filename):
    
    get_file_type = filename.split(".")
    input_dataframe = pd.DataFrame()

    if get_file_type[1]=="csv":
        input_dataframe = pd.read_csv(filename,engine='python')
    elif get_file_type[1]=="xlsx":
        input_dataframe = pd.read_excel(filename)
    else:
        print("File type not supported. Only .xlsx or .csv")

    return input_dataframe

#MAIN
def get_data_function(EMAIL_ID,PASSWORD,PROFILE_LINKS_FILE_LIST,EXISTING_DATA,ADMIT_REJECT_DATA):

    get_file_type = ADMIT_REJECT_DATA.split(".")
    if get_file_type[1] != "csv":
        print("OUTPUT File type not supported. Only .csv")
 
    dataframe = pd.DataFrame()
    for i in PROFILE_LINKS_FILE_LIST:
        data = open_file(i)
        df = remove_duplicates(data)
        dataframe = pd.concat([df,dataframe])

    dataframe = remove_duplicates(dataframe)
    
    df_new = open_file(ADMIT_REJECT_DATA)
    print(df_new)
    df_new1 = remove_duplicates(df_new)
    
    df = open_file(EXISTING_DATA)
    df1 = remove_duplicates(df)

    df_old = pd.concat([df1,df_new1])
    df_old = remove_duplicates(df_old)

    dataframe = pd.concat([df_old,dataframe] , keys = ['old','new'])
    dataframe = remove_duplicates(dataframe)
    
    print(dataframe.loc['old'])
    print(dataframe.loc['new'])

    df = dataframe.loc['new']

    #MAKE A DRIVER SESSION
    chrome_options = Options()
    prefs = {"profile.default_content_setting_values.notifications" : 2}  #block notifications
    chrome_options.add_experimental_option("prefs",prefs)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--load-extension=" + r"C:\Users\Hardik Airen\AppData\Local\Google\Chrome\User Data\Default\Extensions\ookhnhpkphagefgdiemllfajmkdkcaim\2.14.9_0") #<== loading unpacked extension
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument('--disable-features=VizDisplayCompositor')
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1050, 708)
    #extn = pyautogui.locateOnScreen("icon64-gray.png",grayscale=True,confidence = 0.4)   # click on extension
    #print(extn)

    print(driver.get_window_size())

    #CLICK EXTENSION USING pyautogui
    #NOT WORKING IN HEADLESS BROWSER
    try:
        print(pyautogui.size())
        pyautogui.click(x=957,y=70,clicks=1,interval=10,button="left")
        driver.implicitly_wait(5)
        pyautogui.click(x=890,y=195,clicks=1,interval=5,button="left")
        pyautogui.click(x=957,y=70,clicks=1,interval=10,button="left")
        #name_button=WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.CLASS_NAME,'slider.round.center-xs')))
        #name_button.click()
    except Exception as e:
        print(e)

    #CHECK IP ADDRESS CHANGED BY EXTENSION
    try:
        driver.get("https://whatismyipaddress.com/")
        check_ip = BeautifulSoup(driver.page_source, 'html.parser')
        print(check_ip.beautify())
        #print( check_ip.select("div.ipv4"))
    except Exception as e:
        print(e)

    #LOGIN
    try:
        login_now(driver,LOGIN_URL,EMAIL_ID,PASSWORD)
        time.sleep(15)
        print("LOG IN DONE")
    except Exception as e:
        print('Error in login. Problem in WebDriver or Wrong Credentials')
        print(e)
        driver.close()
        driver.quit()

    #LOOP TO GET A PROFILE LINK AND WRITE DATA INTO A CSV FILE #start from 150th row
    get_data_now(driver,df,ADMIT_REJECT_DATA)
    time.sleep(10)
    
    #LOGOUT
    logout_now(driver)
    
 


 

 

 
