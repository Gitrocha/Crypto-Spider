from scrapping import Crypto, driver, CryptoSlugs, iterator
from multiprocessing import Pool
from functools import partial


if __name__ == '__main__':

    all_slugs = CryptoSlugs().get_simple_list()

    coin_list = [item[1] for item in all_slugs]

    nth_coin_list = coin_list[0:99]

    print(nth_coin_list)

    xpool = Pool(processes=4)
    #iterator_partial = partial(iterator, date_start='20130101')
    reqs = xpool.map_async(iterator, nth_coin_list)
    xpool.close()
    xpool.join()
