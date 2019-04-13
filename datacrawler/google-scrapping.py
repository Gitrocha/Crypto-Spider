from selenium import webdriver
from pathlib import Path
import time as t


class XSpider:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'http://google.com.br'
        self.search_bar = 'lst-ib'  # id
        self.btn_search = 'btnK'  # name
        self.btn_lucky = 'btnI'  # name

    def navigate(self):
        self.driver.get(self.url)

    def search(self, word='None'):
        self.driver.find_element_by_name('q').send_keys(word)
        t.sleep(0.5)
        self.driver.find_element_by_name(self.btn_search).click()

def driver(name):
    if name == 'Firefox':
        return webdriver.Firefox(executable_path=r'.\drivers\geckodriver.exe')
    elif name == 'Chrome':
        return webdriver.Chrome(executable_path=r'.\drivers\chromedriver.exe')
    else:
        return 'No driver found'

browser = driver('Chrome')

Google = XSpider(browser)
Google.navigate()
Google.search('Live de Python')

#browser.quit()