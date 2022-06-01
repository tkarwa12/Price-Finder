import pandas as pd

from fuzzywuzzy import fuzz

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def BestBuyBot(userinput,q):
    df=pd.DataFrame(columns=['Item','Price','Website'])
    #print(df)
    #accesses chrome
    #browser=webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    browser=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    browser.get('https://www.bestbuy.com') #opens the website

    searchbar = browser.find_element(by=By.XPATH,value='//*[@id="gh-search-input"]')
    searchbar.send_keys(userinput)
    searchbar.send_keys(Keys.ENTER)
    print(browser.current_url)

    title=browser.find_elements(By.CSS_SELECTOR,".sku-title")
    title_list=[x.text for x in title]

    price=browser.find_elements(By.CSS_SELECTOR,".sku-list-item-price")
    price_list=[x.text for x in price]

    counter=0

    for listing in title_list:
        if fuzz.partial_ratio(listing, userinput)>=65:
            df=df.append({'Item': listing, 'Price': price_list[counter].split('\n')[0], 'Website': 'BestBuy'}, ignore_index=True)
        
        counter+=1

    #print(df)
    browser.quit()
    
    q.put(df)
    return df