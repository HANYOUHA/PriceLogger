#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import csv
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
chrome_driver = "/home/kimjadong2020/Documents/chromedriver"
driver = webdriver.Chrome(chrome_driver, options=chrome_options)

def getURL(url):
    driver.get(url)
    driver.implicitly_wait(2)
    driver.refresh()

def refillGold():
    getURL("https://rivalregions.com/#parliament/offer")
    driver.implicitly_wait(4)
    # time.sleep(4)
    print ("explore state gold")
    driver.find_element_by_xpath("//div[@id='offer_dd']/div/div/div").click()
    driver.implicitly_wait(4)
    # time.sleep(3)
    driver.find_element_by_link_text("Resources exploration: state").click()
    driver.find_element_by_id("offer_do").click()
    time.sleep(1)
    
def goldRefiiler(): # 금 채우기 검사 및 실행
    getURL("https://rivalregions.com/#listed/stateresources/3330")
    time.sleep(3)
    tempList = []
    gold_reserve = driver.find_elements_by_class_name("list_level")
    for element in gold_reserve:
        tempList.append(float(element.text))

    array_gold = np.array(tempList).reshape(-1, 4)

    df_gold = pd.DataFrame(
        array_gold, 
       columns=["Explored", "Maximum", "Deep_exploration", "Limit_left"]
    )

    str_expr = "Limit_left > 0 and Explored < Maximum - 80"
    df_q = df_gold.query(str_expr) 

    if df_q.empty:
        print("채우지 않음")
        return False
    else:
        print("do refill")
        refillGold()
        return True

def goldRefillPresident():
    if (goldRefiiler()):
        # Pro bill
        url = "https://rivalregions.com/#parliament"
        driver.get(url)
        driver.refresh()
        time.sleep(1)
        driver.find_element_by_xpath("//*[contains(text(), 'Resources exploration')]").click()
        driver.find_element_by_xpath("//*[@id='offer_show_v']/div[5]/div").click()

def budgetCheck():
    url = "https://rivalregions.com/#state/details/3330"
    driver.get(url)
    driver.refresh()
    time.sleep(4)

    itemList = []

    budgetList = driver.find_element_by_css_selector(
        "#header_slide_inner > div.minwidth > div.slide_profile_photo > div.imp").find_elements_by_class_name("tip")

    for i in budgetList:
        item = int(i.text.split(" ")[0].replace(".",""))
        itemList.append(item)

    df = pd.DataFrame(
        np.array(itemList).reshape(1, 6), 
        columns=["cash", "gold", "oil", "ore", "uranium", "diamond"]
    ).T
    return df

def priceLoging (numList):
    priceList = []
    now = str( datetime.datetime.now() )
    priceList.append(now)
    
    for num in numList:
        s_xpath = "//div[@url='"+ str(num) +"']"
        driver.find_element_by_xpath( s_xpath ).click() # 자원 클릭
        time.sleep(3)
        element_price = driver.find_element_by_xpath("/html/body/div[6]/div[1]/div[1]/div[2]/div[1]/div[3]/span/span")
        time.sleep(2)
        price = int(element_price.text.split(" ")[0].replace(".",""))
        priceList.append(price)
        
    with open("price_list.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow( priceList )

def train():
    # war train
    getURL("https://rivalregions.com/#war")
    driver.find_element_by_xpath("//div[@id='content']/div[4]/div[2]/div").click()
    driver.find_element_by_id("war_my_alpha").click()
    driver.refresh()
    driver.find_element_by_id("header_my_fill_bar").click()    
    driver.find_element_by_id("war_my_alpha").click()
    
def work():    
    getURL("https://rivalregions.com/#work")
    xpath = "//*[@id='content']/div[6]/div[2]/div[2]/div[3]/div[1]/span/span[1]"
    driver.find_element_by_xpath(xpath).click()
    '''
    driver.find_element_by_id("header_my_fill_bar").click()
    driver.refresh()
    driver.find_element_by_xpath(xpath).click()
    '''

def controller():   
    # price logging
    driver.implicitly_wait(3)
    getURL("https://rivalregions.com/#storage")
    priceLoging(itemList)    
    work()    

itemList = [3, 4, 11, 15, 26] # 석유 광물 우라늄 다이아 라이벌륨
driver.implicitly_wait(2)
getURL("https://rivalregions.com/#overview")

# control plane
for i in range(24):
    goldRefillPresident()
    for j in range(5):
        controller()
        time.sleep(580)
