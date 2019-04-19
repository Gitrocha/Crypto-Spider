from scrapping import Crypto, driver, CryptoSlugs, iterator
from multiprocessing import Pool
from functools import partial
import pandas as pd
from datetime import datetime, timedelta


if __name__ == '__main__':

    #all_slugs = CryptoSlugs().get_simple_list()

    #coin_list = [item[1] for item in all_slugs]

    with open('config/last-update.txt', 'r') as file:
        lastdate = file.read()

    startdate = (datetime.strptime(lastdate, '%Y%m%d') + timedelta(days=1)).strftime('%Y%m%d')

    print(startdate)

    df_coins = pd.read_csv('coin-list.csv')
    coin_list = df_coins['CRIPTONAMES'].values.tolist()
    nth_coin_list = coin_list[:100]
    print(nth_coin_list)

    #iterator('tether', date_start='20130301')

    xpool = Pool(processes=5)
    iterator_partial = partial(iterator, date_start=startdate)
    reqs = xpool.map_async(iterator_partial, nth_coin_list)
    xpool.close()
    xpool.join()

    update = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    print(update)

    with open('config/last-update.txt', 'w') as file:
        file.write(update)

    print(f'Updated from {startdate} to {update}')
