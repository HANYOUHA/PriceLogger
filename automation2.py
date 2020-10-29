#!/usr/bin/env python
# coding: utf-8

from automation import *

class MyDriver(Driver):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "localhost:9223")
        chrome_driver = "/home/kimjadong2020/Documents/chromedriver"
        self.driver = webdriver.Chrome(chrome_driver, options=chrome_options)

d = MyDriver()
d.driver.implicitly_wait(2)
d.getURL("https://rivalregions.com/#overview")

for i in range(24):
    for j in range(6):
        d.getURL("https://rivalregions.com/#overview")
        d.educationUp()
        d.work()
        time.sleep(600-5)
