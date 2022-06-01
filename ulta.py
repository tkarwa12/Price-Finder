import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from fuzzywuzzy import fuzz

def Ultabot(userinput,q):
    df=pd.DataFrame(columns=['Item','Price','Website'])
    #print(df)
    #accesses chrome
    #browser=webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    browser=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    searchbar=browser.get('https://www.ulta.com') #opens the website

    searchbar = browser.find_element(by=By.XPATH,value='//*[@id="searchInput"]')
    searchbar.send_keys(userinput)
    searchbar.send_keys(Keys.ENTER)
    print(browser.current_url)

    title=browser.find_elements(By.CSS_SELECTOR,".prod-title-desc")
    title_list=[x.text.replace("\n",' - ') for x in title]
    #print(title_list)

    price=browser.find_elements(By.CSS_SELECTOR,".regPrice")
    price_list=[x.text for x in price]

    counter=0

    for listing in title_list:
        df=df.append({'Item': listing, 'Price': price_list[counter].split('\n')[0], 'Website': 'Ulta'}, ignore_index=True)
        
        counter+=1

    browser.quit()
    
    #print(df)
    q.put(df)
    return df