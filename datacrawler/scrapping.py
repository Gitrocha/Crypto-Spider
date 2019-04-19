from selenium import webdriver
import time as t
from requests import get
from datetime import datetime
import pandas as pd

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
        try:
            self.driver.get(url)
            t.sleep(10)
            print('* ------------ Page has loaded --------------------- ')
            return 200
        except:
            return 500

    def get_table_rows(self):
        return self.driver.find_elements_by_tag_name('tr')

    def end_process(self):
        print('* ------------ Crawler finished -------------------- ')
        return self.driver.close()


class CryptoSlugs:

    def __init__(self):
        self.url = 'https://s2.coinmarketcap.com/generated/search/quick_search.json'

    def get_headers(self):
        header = dict()
        header['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        header['Origin'] = 'https://coinmarketcap.com'
        header['Refer'] = 'https://coinmarketcap.com/'
        header['User-Agent'] = ': Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        return header

    def get_full_list(self):
        header = self.get_headers()
        response = get(url=self.url, headers=header, stream=stream, timeout=heavyreq_to)
        json_data = response.json()

        return json_data

    def get_simple_list(self):
        full_list = self.get_full_list()
        return [[item['rank'], item['slug']] for item in full_list]


def iterator(coin, date_start):

    today = datetime.now().strftime('%Y%m%d')
    filename = f'database/{coin}.csv'

    print(f'* ------------ Crawling {coin} data ------------------- ')

    crawler = Crypto(driver=driver('Firefox'),
                     date_start=date_start,
                     date_end=today,
                     crypto=coin)

    response = crawler.navigate()
    elements = crawler.get_table_rows()

    while len(elements) < 19 or response != 200:
        print(f'* ------------ Retrying {coin} data gathering ---')
        t.sleep(3)
        response = crawler.navigate()
        elements = crawler.get_table_rows()

    print('* ------------ Table crawled --------------------- ')
    print('len elements', len(elements))

    lastrow = len(elements) - 19
    table = elements[1:lastrow]
    aux_list = []
    for row in table:
        rowdata = row.text.split(' ')
        aux_list.append(rowdata)

    months = [item[0] for item in aux_list]
    days = [item[1].replace(',', '') for item in aux_list]
    years = [item[2] for item in aux_list]
    closes = [(item[6]) for item in aux_list]
    volumes = [(item[7]) for item in aux_list]
    mktcaps = [(item[8]) for item in aux_list]

    df_aux = pd.DataFrame(data={'Month': months,
                                'Day': days,
                                'Year': years,
                                'Close': closes,
                                'Volume': volumes,
                                'Market Cap': mktcaps})
    print('coin \n', df_aux[0:5])

    df_past = pd.read_csv(filename, sep=';')
    df_past = df_past.append(df_aux, sort=False)

    df_past.to_csv(filename, sep=';', index=False)

    print('* ------------ DF saved --------------------- ')
    crawler.end_process()
