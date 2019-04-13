from scrapping import Crypto, driver, CryptoSlugs
from datetime import datetime


all_slugs = CryptoSlugs().get_list()

print(all_slugs[0])

'''
today = datetime.now().strftime('%Y%m%d')

coin = 'bitcoin'

crawler = Crypto(driver=driver('Chrome'),
                 date_start='20190412',
                 date_end=today,
                 crypto=coin)

crawler.navigate()

elements = crawler.get_table_rows()

crawler.end_process()

with open(f'database/{coin}.csv', 'w+') as file:
    for row in elements:
        file.write(row.text)
        file.write('\n')
'''