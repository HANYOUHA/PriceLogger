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
            time.sleep(5)
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
    time.sleep(1)
    driver.refresh()
    driver.implicitly_wait(4)
    time.sleep(3)
    try:
        driver.find_element_by_css_selector( selector).click()
    except:
        getURL("https://rivalregions.com/#work")
        driver.find_element_by_css_selector( selector).click()

driver.implicitly_wait(2)
getURL("https://rivalregions.com/#overview")

# control plane
for i in range(24):
    for j in range(6):
        work()
        time.sleep(600)
