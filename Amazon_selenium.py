import pandas as pd

from fuzzywuzzy import fuzz

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def Amazonbot(userinput,q):
    df=pd.DataFrame(columns=['Item','Price','Website'])
    #print(df)
    #accesses chrome
    #browser=webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    browser=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    browser.get('https://www.amazon.com') #opens the website

    searchbar = browser.find_element(by=By.XPATH,value='//*[@id="twotabsearchtextbox"]')
    searchbar.send_keys(userinput)
    searchbar.send_keys(Keys.ENTER)
    print(browser.current_url)

    test=browser.find_elements(By.CSS_SELECTOR,"div[data-component-type='s-search-result']:not(.AdHolder)")

    test_list=[x.text for x in test]
    results=[x.replace('\n','___') for x in test_list]
    #print(test_list)
    #print(len(test_list))

    results_lists=[listing.split('___') for listing in results]
    #print(results_lists)

    for listing in results_lists:
        found=0
        for item in listing:
            if found==1:
                break
            elif item[0]=='$' and fuzz.partial_ratio(listing, userinput)>=20:
                #print(listing[0],item)
                df = df.append({'Item': listing[0], 'Price': item, 'Website': 'Amazon'}, ignore_index=True)
                found=1 

    browser.quit() #closes out of chrome

    #print(df)
    q.put(df)
    return df