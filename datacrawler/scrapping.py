from selenium import webdriver
from datetime import datetime
import time as t


def driver(name):
    if name == 'Firefox':
        return webdriver.Firefox(executable_path=r'.\drivers\geckodriver.exe')
    elif name == 'Chrome':
        return webdriver.Chrome(executable_path=r'.\drivers\chromedriver.exe')
    else:
        return 'No driver found'

class Crypto:
    def __init__(self, driver, date_end=None, crypto=None):
        self.driver = driver
        self.date_start = '20190101'
        self.date_end = date_end
        self.crypto = crypto
        self.url = 'https://coinmarketcap.com/currencies'
        self.box = 'container main-section'  # Class - Table of Cryptos
        self.price_test2 = '//*[@id="historical-data"]/div/div[2]'

    def navigate(self):
        print('* ------------ Starting navigation ----------------- ')
        url = f'{self.url}/{self.crypto}/historical-data/?start={self.date_start}&end={self.date_end}'
        self.driver.get(url)
        t.sleep(5)
        print('* ------------ Page has loaded ----------------- ')

    def test3(self):
        return self.driver.find_elements_by_tag_name('tr')


today = datetime.now().strftime('%Y%m%d')

crawler = Crypto(driver=driver('Chrome'),
                 date_end=today,
                 crypto='ripple')

crawler.navigate()

elements = crawler.test3()

with open('ripple.csv', 'w+') as file:
    for row in elements:
        file.write(row.text)
        file.write('\n')