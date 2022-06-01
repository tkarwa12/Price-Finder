from Amazon_selenium import Amazonbot
from bestbuy_selenium import BestBuyBot
from ulta import Ultabot

import pandas as pd

import multiprocessing
from multiprocessing import Process

#user_input=input("What are you looking for? ")
user_input='neutrogena acne face wash'

#df_Amazon=Amazonbot(user_input)
#df_BestBuy=BestBuyBot(user_input)

if __name__=='__main__':
    q=multiprocessing.Queue()
    
    p1 = Process(target = Amazonbot, args=(user_input,q))
    p2 = Process(target = BestBuyBot, args=(user_input,q))
    p3 = Process(target = Ultabot, args=(user_input,q))
    
    p1.start()
    p2.start()
    p3.start()
    
    df_amazon=q.get()
    p1.join()

    df_bestbuy=q.get()
    p2.join()
    
    df_ulta=q.get()
    p3.join()
    
    print(pd.concat([df_amazon,df_ulta,df_bestbuy]))