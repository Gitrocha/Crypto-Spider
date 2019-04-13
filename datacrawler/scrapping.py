from selenium import webdriver
import time as t
from requests import get

#------- REQUESTS PERFORMANCE CONFIG OPTIMIZATION AND RETRIES
stream = False
chunks = 10485760

#Timeout connection and read times for single and heavy requests
singlereq_to = 20
heavyreq_to = 300


def driver(name):
    if name == 'Firefox':
        return webdriver.Firefox(executable_path=r'.\drivers\geckodriver.exe')
    elif name == 'Chrome':
        return webdriver.Chrome(executable_path=r'.\drivers\chromedriver.exe')
    else:
        return 'No driver found'


class Crypto:
    def __init__(self, driver, date_start=None, date_end=None, crypto=None):
        self.driver = driver
        self.date_start = date_start
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
        print('* ------------ Page has loaded --------------------- ')

    def get_table_rows(self):
        return self.driver.find_elements_by_tag_name('tr')

    def end_process(self):
        return self.driver.close()


class CryptoSlugs:

    def __init__(self):
        self.url = 'https://s2.coinmarketcap.com/generated/search/quick_search.json'

    def get_headers(self):
        header = dict()
        header['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        return header

    def get_list(self):
        header = self.get_headers()
        response = get(url=self.url, headers=header, stream=stream, timeout=heavyreq_to)
        json_data = response.json()

        return json_data

'''
class ApiAuth:
class ApiSales:

    def __init__(self, token=None,
                 stonecode=None,
                 startdate=None,
                 finaldate=None,
                 outformat=None,
                 splitmode=None,
                 url='https://portalapi.stone.com.br/v1/transactions'):

    def get(self):
        try:
            header = self.get_headers()
            response = requests.get(url=self.url, headers=header, stream=stream, timeout=heavyreq_to)
        except:
            rsc = 500
            return rsc

'''