#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 21:32:24 2024

@author: Stephen
"""




import datetime
from datetime import date, timedelta

#Change below inputs
search_word = "HKD" #HKD or CNY
d1 = date(2024, 10, 1) # the start date
d2 = date(2024, 10, 31) # the end date
login_id = "angela_kw_sze@hkma.gov.hk" 
login_pw = "Hkma1488!"
driver_PATH =  '/mnt/prototypehkmastorage1/DO-Data Science/utils/chromedriver'

#import libraries

import time
import random

import glob
import urllib.parse as urllib
import pandas as pd
from time import gmtime, strftime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from datetime import date, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os, shutil







#Global Variables:
error = ""
input_table = pd.DataFrame()
output_table = pd.DataFrame()

def Test_Multiple_Currencies():
    
    #2
    ActionChains(driver).send_keys('USD').perform()
    time.sleep(3)
    ActionChains(driver).send_keys(Keys.RETURN).perform()
    
    #3 
    time.sleep(4)
    ActionChains(driver).send_keys('CNY').perform()
    time.sleep(3)
    ActionChains(driver).send_keys(Keys.RETURN).perform()
    
    #4
    time.sleep(4)
    ActionChains(driver).send_keys('JPY').perform()
    time.sleep(3)
    ActionChains(driver).send_keys(Keys.RETURN).perform()
    
    #5
    time.sleep(4)
    ActionChains(driver).send_keys('GBP').perform()
    time.sleep(3)
    ActionChains(driver).send_keys(Keys.RETURN).perform()



    
def update_DF():
    
    global error, input_table, output_table
    
    error = driver.find_element("xpath","//*[@id='error']").text
    
    if error == "":
        input_table = pd.read_html(driver.page_source, attrs={'class': 'sortable'})[0]
        output_table = pd.concat([output_table, input_table])


#Program starts here
delta = d2 - d1
one_day = datetime.timedelta(days=1)
one_mo = datetime.timedelta(weeks=4)
one_year = datetime.timedelta(weeks=48)

Cant_use_Method_1 = False
warning = False



# Setting options
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without opening a browser window)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--start-maximized")  # Start Chrome maximized
chrome_options.add_argument("--incognito")  # Start Chrome in incognito mode

browpath2 = r'/Users/Stephen/Desktop/Learning_code/textmin_proj/testsel/testing/webscrap/chromedriver' 



driver = webdriver.Chrome(browpath2, options= chrome_options) 




url = "https://my.euroclear.com/apps/en/bank-securities-search.html"
#wait = WebDriverWait(driver, 30)

# Accept cookies & Enter credentials
driver.get(url)
print("start website...")
time.sleep(random.uniform(5.5, 6.5))



driver.find_element("xpath","//*[@id='js-modal-content']/div[1]/div[3]/div/div[1]/button/span").click()

driver.find_element("xpath","//*[@id='username']").send_keys(login_id)
driver.find_element("xpath","//*[@id='password']").send_keys(login_pw)
driver.find_element("xpath","//*[@id='password']").send_keys(Keys.RETURN)



time.sleep(random.uniform(3.5,4.5))

driver.find_element("xpath","//*[@class='searchToggler _moreOptions']").click()

time.sleep(random.uniform(3.5,4.5))


dloop = 0
retryno = 0
while dloop < (delta.days + 1):

    dloop_previous = pd.to_numeric(dloop)

#reset
    driver.find_element("xpath","//*[@type='reset']").click() 

#Date Input
    date = d1 + dloop*one_day
    
    datestr = date.strftime('%d/%m/%y')

    driver.find_element("xpath","//*[@id='firstclosingdate_1_container']").click() 

    time.sleep(random.uniform(0.95,1.1))

    ActionChains(driver).send_keys(datestr).perform()

    driver.find_element("xpath","//*[@id='firstclosingdate_2_container']").click()
    
    time.sleep(random.uniform(0.95,1.1))

    ActionChains(driver).send_keys(datestr).perform()
    
    time.sleep(random.uniform(0.95,1.1))

    ActionChains(driver).send_keys(Keys.RETURN).perform()

    driver.find_element("xpath","//*[@class='securitytype jsonDropdown']").click()

    time.sleep(random.uniform(0.95,1.1))

    ActionChains(driver).send_keys("Debt: all").perform()
    
    time.sleep(random.uniform(0.95,1.1))

    ActionChains(driver).send_keys(Keys.RETURN).perform() 
    
    
#Currency Input
    driver.find_element("xpath","//*[@class='currency jsonDropdown']").click()

    time.sleep(random.uniform(0.95,1.1))

    ActionChains(driver).send_keys(search_word).perform()
    
    time.sleep(random.uniform(0.95,1.1))

    ActionChains(driver).send_keys(Keys.RETURN).perform() 

    time.sleep(random.uniform(4,5) + retryno*30)
    
    #Test_Multiple_Currencies()
    
    now_test = True #for testing purposes

#Results
    error = driver.find_element("xpath","//*[@id='error']").text
    
    if "Too many results" in error: #or now_test == True:
                
        #Check if it is workable to divide the maturity period into [<=1 year], [>1 year]
        
        #Mature within 1 year
        temp_table1 = pd.DataFrame()
        temp_table2 = pd.DataFrame()
        
        driver.find_element("xpath","//*[@id='modifier_maturitydate_chzn']").click()
        time.sleep(random.uniform(0.3,0.5))
        driver.find_element("xpath","//*[@id='modifier_maturitydate_chzn_o_0']").click()
        time.sleep(random.uniform(0.3,0.5))
        
        driver.find_element("xpath","//*[@id='maturitydate_1_date']").clear()
        time.sleep(random.uniform(0.5,0.6))
        
        driver.find_element("xpath","//*[@id='maturitydate_2_date']").clear()
        time.sleep(random.uniform(0.5,0.6))
        
        driver.find_element("xpath","//*[@id='maturitydate_1_date']").click()
        time.sleep(random.uniform(1,1.2))
        ActionChains(driver).send_keys(date.strftime('%d/%m/%y')).perform()    
        time.sleep(random.uniform(1,1.2))
        
        mday0 = date + 1*one_year
        
        driver.find_element("xpath","//*[@id='maturitydate_2_date']").click()
        time.sleep(random.uniform(1,1.2))
        ActionChains(driver).send_keys(mday0.strftime('%d/%m/%y')).perform()    
        time.sleep(random.uniform(1,1.2))
        
        ActionChains(driver).send_keys(Keys.RETURN).perform() 
        time.sleep(random.uniform(4.5,5))
        
        if "Too many results" in driver.find_element("xpath","//*[@id='error']").text:
            Cant_use_Method_1 = True
            print(1)
        
        else:
            if "not been found" not in driver.find_element("xpath","//*[@id='error']").text:
                temp_table1 = pd.read_html(driver.page_source, attrs={'class': 'sortable'})[0]
        
        #Mature after than 1 year or more
        driver.find_element("xpath","//*[@id='modifier_maturitydate_chzn']").click()
        time.sleep(random.uniform(0.3,0.5))
        driver.find_element("xpath","//*[@id='modifier_maturitydate_chzn_o_2']").click()
        time.sleep(random.uniform(0.3,0.5))
        
        driver.find_element("xpath","//*[@id='maturitydate_1_date']").clear()
        time.sleep(random.uniform(0.5,0.6))
        
        driver.find_element("xpath","//*[@id='maturitydate_1_date']").click()
        time.sleep(random.uniform(0.6,0.8))
        ActionChains(driver).send_keys(mday0.strftime('%d/%m/%y')).perform()    
        time.sleep(random.uniform(1,1.2))
        
        ActionChains(driver).send_keys(Keys.RETURN).perform() 
        time.sleep(random.uniform(4.5,5))
        
        if "Too many results" in driver.find_element("xpath","//*[@id='error']").text:
            Cant_use_Method_1 = True
            print(1)
        
        else:
            if "not been found" not in driver.find_element("xpath","//*[@id='error']").text:
                temp_table2 = pd.read_html(driver.page_source, attrs={'class': 'sortable'})[0]
        
        
        
        if Cant_use_Method_1 == False:
            output_table = pd.concat([output_table, temp_table1, temp_table2])
            
        else:
            #Method 2: [>2 years], [every 3-month in the remaining period]
            
            #Capture all entities maturing after 2 years or more
            time.sleep(random.uniform(1,1.2))
            driver.find_element("xpath","//*[@id='modifier_maturitydate_chzn']").click()
            time.sleep(random.uniform(0.5,0.6))
            driver.find_element("xpath","//*[@id='modifier_maturitydate_chzn_o_2']").click()  
            time.sleep(random.uniform(0.5,0.6))
            driver.find_element("xpath","//*[@id='maturitydate_1_date']").clear()
            time.sleep(random.uniform(0.5,0.6))
            driver.find_element("xpath","//*[@id='maturitydate_1_date']").click()
            time.sleep(random.uniform(0.5,0.6))
        
            mday1 = date + 2*one_year
        
            ActionChains(driver).send_keys(mday1.strftime('%d/%m/%y')).perform()
            time.sleep(random.uniform(1.1,1.2))
            ActionChains(driver).send_keys(Keys.RETURN).perform()        
            time.sleep(random.uniform(4.5,5))
        
            update_DF()
                
            if error == 'Too many results':
                warning = True
                #break

            
            #Capture all entities maturing on the ceiling day
            time.sleep(random.uniform(1,1.2))
            driver.find_element("xpath","//*[@id='modifier_maturitydate_chzn']").click()
            time.sleep(random.uniform(0.5,0.6))
            driver.find_element("xpath","//*[@id='modifier_maturitydate_chzn_o_3']").click()  
            time.sleep(random.uniform(0.5,0.6))
            driver.find_element("xpath","//*[@id='maturitydate_1_date']").click()
            time.sleep(random.uniform(0.5,0.6))
            ActionChains(driver).send_keys(Keys.RETURN).perform()        
            time.sleep(random.uniform(4.5,5))
        
            update_DF()
            
            if error == 'Too many results':
                warning = True
                #break
            
            
            #Capture all entities maturing within every 1-month in the remaining period
            driver.find_element("xpath","//*[@id='modifier_maturitydate_chzn']").click()
            time.sleep(random.uniform(0.2,0.3))
            driver.find_element("xpath","//*[@id='modifier_maturitydate_chzn_o_0']").click()
        
            while mday1 - 3*one_mo >= date:
                driver.find_element("xpath","//*[@id='maturitydate_1_date']").clear()
                driver.find_element("xpath","//*[@id='maturitydate_2_date']").clear()
                time.sleep(random.uniform(0.95,1.1))
            
                driver.find_element("xpath","//*[@id='maturitydate_2_date']").click()
                time.sleep(random.uniform(0.2,0.3))
                ActionChains(driver).send_keys((mday1-one_day).strftime('%d/%m/%y')).perform()    
                time.sleep(random.uniform(0.95,1.1))
            
                mday1 = mday1 - 3*one_mo
            
                driver.find_element("xpath","//*[@id='maturitydate_1_date']").click()
            
                time.sleep(random.uniform(0.95,1.1))
            
                ActionChains(driver).send_keys(mday1.strftime('%d/%m/%y')).perform()
                time.sleep(random.uniform(0.95,1.1))
                ActionChains(driver).send_keys(Keys.RETURN).perform() 
                time.sleep(random.uniform(4.5,5))
            
                update_DF()

                if error == 'Too many results':
                    warning = True
                    #break
                
        if warning == True:
            print("!!! unable to scrap data for ", datestr, " please input data manually")
        else:
            print(datestr, " Done. has too many results, please double check manually") # has too many results, please double check manually

    elif error == "":
        update_DF()
        
        print(datestr, " Done.")
        
    elif "not been found" in error:
        
        retryno += 1
        if date.weekday() < 5:
            if retryno <=3: 
                print(datestr, " No results. Weekday, retrying...(added ", retryno*30, " sec waiting time.)")
                dloop -= 1
            else:
                print(datestr, " No results. Weekday, Please double check manually")
        else: 
            print(datestr, " No results.")
    else:
        print(datestr, " ERR. Check code")
    
    dloop += 1
    if dloop != dloop_previous:
        retryno = 0
#Save File

filename = "Euroclear_" + search_word + "_" + str(d1.strftime("%y%m%d")) + "_" + str(d2.strftime("%y%m%d"))



#output_table.to_csv(filename + '.csv', columns=['Name','ISIN','Common code','Rate','Nominal currency','First Closing','Payment date','Record date','Market','Instrument','Last update'], index=False)


output_table.to_csv( '/Users/Stephen/Desktop/Learning_code/bonddatabase/' + filename + '.csv', columns=['Name','ISIN','Common code','Rate','Nominal currency','First Closing','Payment date','Record date','Market','Instrument','Last update'], index=False)












