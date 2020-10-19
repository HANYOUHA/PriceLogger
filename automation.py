#!/usr/bin/env python
# coding: utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, re, sys
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
    driver.refresh()
    driver.implicitly_wait(6)

def refillGold():
    getURL("https://rivalregions.com/#parliament/offer")
    print ("explore state gold")
    driver.implicitly_wait(7)
    try:
        driver.find_element_by_xpath("//div[@id='offer_dd']/div/div/div").click()
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        getURL("https://rivalregions.com/#parliament/offer")
        time.sleep(5)
        driver.find_element_by_xpath("//div[@id='offer_dd']/div/div/div").click()

    driver.implicitly_wait(4)
    driver.find_element_by_link_text("Resources exploration: state").click()
    driver.implicitly_wait(1)
    driver.find_element_by_id("offer_do").click()
    # time.sleep(1)

def goldRefiiler(): # 금 채우기 검사 및 실행
    getURL("https://rivalregions.com/#listed/stateresources/3330")
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
        try:
            refillGold()
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            return False

        return True

def goldRefillPresident():
    if (goldRefiiler()):
        try:
            # Pro bill
            driver.implicitly_wait(1)
            getURL("https://rivalregions.com/#parliament")
            driver.implicitly_wait(2)
            driver.find_element_by_xpath("//*[contains(text(), 'Resources exploration')]").click()
            driver.implicitly_wait(2)
            driver.find_element_by_xpath("//*[@id='offer_show_v']/div[5]/div").click()
        except:
            print("bill accept error")

def budgetCheck():
    getURL("https://rivalregions.com/#state/details/3330")

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
    getURL("https://rivalregions.com/#storage")
    priceList = []
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    priceList.append( str(now) )
    time.sleep(3)

    for num in numList:
        time.sleep(2)
        s_xpath = f"//*[@id='content']/div[{num}]/div[3]"
        driver.find_element_by_xpath( s_xpath ).click() # 자원 클릭
        xpath = "//*[@id='storage_market']/div[2]/div[1]/div[3]/span/span"
        time.sleep(3)
        price = 0
        try:
            element_price = driver.find_element_by_xpath(xpath)
            price = int(element_price.text.split(" ")[0].replace(".",""))
        except:
            print(f"xpath is missing num : {num}")
            getURL("https://rivalregions.com/#storage")
            time.sleep(2)
            driver.find_element_by_xpath(f"//*[@id='content']/div[{num}]/div[3]").click()
            time.sleep(8)
            xpath = "//*[@id='storage_market']/div[2]/div[1]/div[3]/span/span"
            element_price = driver.find_element_by_xpath(xpath)
            price = int(element_price.text.split(" ")[0].replace(".",""))
        if (price != 0):
            priceList.append(price)
        else:
            print ("price error")
            return -1

    with open("price_list.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow( priceList )

def train():
    # war train
    getURL("https://rivalregions.com/#war")
    try:
        driver.find_element_by_xpath("//div[@id='content']/div[4]/div[2]/div").click()
        driver.find_element_by_id("war_my_alpha").click()
        driver.refresh()
        driver.implicitly_wait(3)
        driver.find_element_by_id("header_my_fill_bar").click()
        time.sleep(1)
        driver.find_element_by_id("war_my_alpha").click()
    except:
        print("train error")

def work():
    getURL("https://rivalregions.com/#work")
    selector = "#content > div:nth-child(7) > div.work_w_5.work_square > div.tc.float_left.mini.work_exp_2 > div:nth-child(3) > div.work_factory_button.button_blue"
    try:
        driver.find_element_by_css_selector( selector).click()
    except:
        print("work error")
        try:
            getURL("https://rivalregions.com/#work")
            time.sleep(5)
            driver.find_element_by_css_selector( selector).click()
        except:
            print("work error2")
            getURL("https://rivalregions.com/#work")
            driver.find_element_by_xpath("//*[@id='sa_add2']/div[2]/a[2]/div").click()
            print("click capcha")
            driver.implicitly_wait(5)
            getURL("https://rivalregions.com/#work")
            driver.find_element_by_css_selector( selector).click()
    driver.implicitly_wait(1)
    try:
        driver.find_element_by_id("header_my_fill_bar").click()
    except:
        print("Cannot refill energy")
    time.sleep(2)
    driver.refresh()
    driver.implicitly_wait(4)
    time.sleep(2)
    try:
        driver.find_element_by_css_selector( selector).click()
    except:
        getURL("https://rivalregions.com/#work")
        driver.find_element_by_css_selector( selector).click()

def controller():
    work()
    # price logging
    priceLoging(itemList)

itemList = [3, 4, 5, 6, 9] # 석유 광물 우라늄 다이아 라이벌륨
driver.implicitly_wait(2)
getURL("https://rivalregions.com/#overview")

# control plane
for i in range(24):
    goldRefillPresident()
    time.sleep(1)
    for j in range(6):
        controller()
        time.sleep(573)
