#!/usr/bin/env python
# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
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

class Driver:
    # driver = null
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
        chrome_driver = "/home/kimjadong2020/Documents/chromedriver"
        self.driver = webdriver.Chrome(chrome_driver, options=chrome_options)
        self.itemList = [3, 4, 5, 6, 8, 9, 14, 15, 16, 17, 19] # oil, ore, etc.

    def errorInfo(self, s_method):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print (now)
        print ("Unexpected error:", sys.exc_info()[0], "in "+ s_method)

    def getURL(self, url):
        try:
            self.driver.get(url)
            self.driver.refresh()
            self.driver.implicitly_wait(6)
            return 0;
        except:
            self.errorInfo( "getURL" )
            self.driver.refresh()
            self.driver.implicitly_wait(6)
            self.getURL(url);
            return -1;

    def refillGold(self):
        self.getURL("https://rivalregions.com/#parliament/offer")
        print ("explore state gold")
        time.sleep(7)
        try:
            self.driver.find_element_by_xpath("//div[@id='offer_dd']/div/div/div").click()
        except:
            self.getURL("https://rivalregions.com/#parliament/offer")
            time.sleep(7)
            self.driver.find_element_by_xpath("//div[@id='offer_dd']/div/div/div").click()

        self.driver.implicitly_wait(4)
        self.driver.find_element_by_link_text("Resources exploration: state").click()
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_id("offer_do").click()
        # time.sleep(1)

    def goldRefiller(self): # 금 채우기 검사 및 실행
        self.getURL("https://rivalregions.com/#listed/stateresources/3330")
        time.sleep(1)
        tempList = []
        gold_reserve = self.driver.find_elements_by_class_name("list_level")
        for element in gold_reserve:
            tempList.append(float(element.text))

        array_gold = np.array(tempList).reshape(-1, 4)

        df_gold = pd.DataFrame(
            array_gold,
           columns=["Explored", "Maximum", "Deep_exploration", "Limit_left"]
        )

        str_expr = "Limit_left > 0 and Explored < Maximum - 100"
        df_q = df_gold.query(str_expr)

        if df_q.empty:
            print("채우지 않음")
            return False
        else:
            print("do refill")
            try:
                self.refillGold()
            except:
                self.errorInfo( "goldRefiller" )
                return False

            return True

    def goldRefillPresident(self):
        if (self.goldRefiller()):
            try:
                # Pro bill
                self.driver.implicitly_wait(1)
                self.getURL("https://rivalregions.com/#parliament")
                self.driver.implicitly_wait(2)
                self.driver.find_element_by_xpath(
                        "//*[contains(text(), 'Resources exploration')]" ).click()
                self.driver.implicitly_wait(2)
                self.driver.find_element_by_xpath("//*[@id='offer_show_v']/div[5]/div").click()
            except:
                print("bill accept error")

    def budgetCheck(self):
        self.getURL("https://rivalregions.com/#state/details/3330")
        itemList = []
        budgetList = self.driver.find_element_by_css_selector(
            "#header_slide_inner > div.minwidth > div.slide_profile_photo > div.imp"
            ).find_elements_by_class_name("tip")

        for i in budgetList:
            item = int(i.text.split(" ")[0].replace(".",""))
            itemList.append(item)

        df = pd.DataFrame(
            np.array(itemList).reshape(1, 6),
            columns=["cash", "gold", "oil", "ore", "uranium", "diamond"]
        ).T
        return df

    def controller(self):
        self.work()
        self.priceLoging(self.itemList)

    def priceLoging (self, numList):
        self.getURL("https://rivalregions.com/#storage")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        priceList = []
        priceList.append( str(now) )
        time.sleep(3)

        for num in numList:
            time.sleep(3.5)
            s_xpath = f"//*[@id='content']/div[{num}]/div[3]"
            price = 0
            try:
                self.driver.find_element_by_xpath( s_xpath ).click() # 자원 클릭
                xpath = "//*[@id='storage_market']/div[2]/div[1]/div[3]/span/span"
                time.sleep(3)
                element_price = self.driver.find_element_by_xpath(xpath)
                price = int(element_price.text.split(" ")[0].replace(".",""))
            except:
                print(f"xpath is missing num : {num}")
                self.getURL("https://rivalregions.com/#storage")
                time.sleep(2)
                self.driver.find_element_by_xpath(
                        f"//*[@id='content']/div[{num}]/div[3]").click()
                time.sleep(7)
                xpath = "//*[@id='storage_market']/div[2]/div[1]/div[3]/span/span"
                element_price = self.driver.find_element_by_xpath(xpath)
                price = int(element_price.text.split(" ")[0].replace(".",""))
            if (price != 0):
                priceList.append(price)
            else:
                print ("price error")
                return -1

        with open("price_list.csv", "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow( priceList )

    def trainHourly(self):
        driver = self.driver
        self.getURL("https://rivalregions.com/#war")
        try:
            driver.find_element_by_xpath("//div[@id='content']/div[4]/div[2]/div").click()
            driver.find_element_by_id("war_my_alpha").click()
        except:
            self.errorInfo( "trainHourly" )

    def train(self):
        # war train
        self.getURL("https://rivalregions.com/#war")
        try:
            self.driver.find_element_by_xpath("//div[@id='content']/div[4]/div[2]/div").click()
            self.driver.find_element_by_id("war_my_alpha").click()
            self.driver.refresh()
            self.driver.implicitly_wait(3)
            self.driver.find_element_by_id("header_my_fill_bar").click()
            time.sleep(1)
            self.driver.find_element_by_id("war_my_alpha").click()
        except:
            print("train error")

    def work(self):
        self.getURL("https://rivalregions.com/#work")
        selector = "#content > div:nth-child(7) > div.work_w_5.work_square > div.tc.float_left.mini.work_exp_2 > div:nth-child(3) > div.work_factory_button.button_blue"
        try:
            self.driver.find_element_by_css_selector( selector).click()
        except:
            print("work error")
            try:
                self.getURL("https://rivalregions.com/#work")
                time.sleep(5)
                self.driver.find_element_by_css_selector( selector).click()
            except:
                print("work error2")
                self.getURL("https://rivalregions.com/#work")
                time.sleep(3)
                # self.driver.refresh()
                # time.sleep(3)
                self.driver.find_element_by_xpath("//*[@id='sa_add2']/div[2]/a[2]/div").click()
                print("click capcha")
                self.driver.implicitly_wait(5)
                self.getURL("https://rivalregions.com/#work")
                self.driver.find_element_by_css_selector( selector).click()
        self.driver.implicitly_wait(1)
        try:
            self.driver.find_element_by_id("header_my_fill_bar").click()
        except:
            print("Cannot refill energy")
        time.sleep(3)
        self.driver.refresh()
        time.sleep(3)
        try:
            self.driver.find_element_by_css_selector( selector).click()
        except:
            self.getURL("https://rivalregions.com/#work")
            self.driver.find_element_by_css_selector( selector).click()


    def educationUp(self):
        try:
            xpath = "//*[@id='index_perks_list']/div[5]/div[1]"
            self.driver.implicitly_wait(6)
            self.driver.find_element_by_xpath( xpath ).click()
            xpath = "//*[@id='perk_target_4']/div[1]/div[1]/div"
            self.driver.find_element_by_xpath( xpath ).click()
        except:
            self.errorInfo( "educationUp" )

if __name__ == "__main__":
    d = Driver()
    d.driver.implicitly_wait(2)
    d.getURL("https://rivalregions.com/#overview")

    for i in range(24):
        d.trainHourly()
        for j in range(6):
            d.getURL("https://rivalregions.com/#overview")
            d.educationUp()
            if (j==0):
                d.goldRefillPresident()
                time.sleep(1)
                j = j+1
                d.controller()
                time.sleep(60*8+18)
            else:
                d.controller()
                time.sleep(60*8+24)
