import automation

class MyDriver(automation.Driver):
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
        if (j==0):
            d.goldRefillPresident()
            time.sleep(1)
            j = j+1
            d.controller()
            time.sleep(60*8+28)
        else:
            d.controller()
            time.sleep(60*8+36)
