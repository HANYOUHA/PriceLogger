#!/usr/bin/env python
# coding: utf-8

from automation import *

class MyDriver(Driver):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "localhost:9223")
        chrome_driver = "/home/kimjadong2020/Documents/chromedriver"
        self.driver = webdriver.Chrome(chrome_driver, options=chrome_options)

    def department(self):
        driver = self.driver
        driver.find_element_by_xpath("//div[@id='quests_wrap']/div[5]").click()
        driver.implicitly_wait(5)
        for i in range(10):
            driver.find_element_by_xpath(
                    "//div[@id='region_scroll']/div/div/div[17]/div[3]/div/div/div[3]").click()
        driver.find_element_by_xpath("//div[@id='header_slide_inner']/div[4]/div").click()
        driver.find_element_by_id("slide_close").click()

    def trainHourly(self):
        # war train
        self.getURL("https://rivalregions.com/#war")
        try:
            self.driver.find_element_by_xpath(
                    "//div[@id='content']/div[4]/div[2]/div").click()
            self.driver.find_element_by_id("war_my_alpha").click()
        except:
            print("train error")

d = MyDriver()
d.getURL("https://rivalregions.com/#overview")

for i in range(24):
    d.trainHourly()
    for j in range(6):
        d.getURL("https://rivalregions.com/#overview")
        d.educationUp()
        d.work()
        time.sleep(600-5)
