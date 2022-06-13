import inspect
import logging
import os.path as path
from json import loads
from os import makedirs
from pathlib import Path

import validators
from bs4 import BeautifulSoup
from pandas import DataFrame, read_csv, concat
from requests import get, HTTPError

logging.basicConfig(format="%(asctime)s - [%(levelname)s]\t%(message)s",
                    datefmt='%d-%b-%y %H:%M:%S')


class Crawler:
    @staticmethod
    def url_validator(link: str) -> bool:
        """
        The function validates whether a given string is a valid URL of talabat.com or not
        :rtype: bool
        :param link: A string to be validated as URL or not
        :return: True if URL, else False
        """
        if validators.url(link) and (link.startswith('https://www.talabat.com/')):
            return True
        else:
            return False

    def __init__(self, url: str, base_dir: str = 'crawled_data',
                 f_name: str = 'crawled_data', menu_dir: str = 'menus') -> None:
        """
        :rtype: None
        :param url: URL for data crawl
        :param base_dir: Directory to save data
        :param menu_dir: Directory to save menus
        """
        self.__flag = True
        self.__details_json = None
        self.__bs4_data = None

        self.__restaurant_details = {}
        self.__restaurant_menu_details = []

        frame = inspect.stack()[1]
        filename = frame[0].f_code.co_filename
        filepath = Path(path.dirname(filename))

        self.__filename = f_name

        if path.isabs(base_dir):
            self.__base_dir = Path(base_dir)
        else:
            self.__base_dir = filepath / base_dir

        if path.isabs(menu_dir):
            self.__menu_dir = Path(menu_dir)
        else:
            self.__menu_dir = self.__base_dir / menu_dir

        try:
            if self.url_validator(url):
                self.url = url
            else:
                self.url = url
                raise TypeError(f"'{url}' is not a valid URL")

        except TypeError as e:
            self.url = None
            self.__flag = False
            logging.error(e)

        except Exception as e:
            self.url = None
            self.__flag = False
            logging.debug(e)

        # calling other function(s)
        if self.__flag:
            self.__fetch_details()

    def __fetch_details(self):
        try:
            raw = get(self.url, allow_redirects=True, headers=(
                {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                  '(KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
                }
            ))

            status_code = raw.status_code
            reason = raw.reason

            if status_code != 200:
                raise HTTPError(status_code, reason)

            self.__bs4_data = BeautifulSoup(raw.content, 'lxml')

        except HTTPError as e:
            self.__flag = False
            err = f"{self.url} - {e.strerror} [{e.errno}]"
            self.__bs4_data = None
            logging.error(err)

        except Exception as e:
            self.__flag = False
            self.__bs4_data = None
            logging.debug(e)

        # call other function(s)
        if self.__flag:
            self.__make_json()

    def __make_json(self):
        try:
            try:
                data = self.__bs4_data.select('#__NEXT_DATA__')[0].text
                self.__details_json = loads(data)

            except Exception as e:
                self.__flag = False
                self.__details_json = None
                logging.error(e)

        except Exception as e:
            self.__flag = False
            self.__details_json = None
            logging.error(e)

        # call other function(s)
        if self.__flag:
            self.__fetch_restaurant_details()

    def __fetch_restaurant_details(self):
        try:
            restaurant_json = self.__details_json['props']['pageProps']['initialMenuState']['restaurant']
            self.__restaurant_details['restaurant_name'] = [restaurant_json['name']]
            self.__restaurant_details['restaurant_logo'] = [restaurant_json['logo']]
            self.__restaurant_details['latitude'] = [float(restaurant_json['latitude'])]
            self.__restaurant_details['longitude'] = [float(restaurant_json['longitude'])]
            self.__restaurant_details['cuisine_tags'] = [restaurant_json['cuisineString']]
            self.__restaurant_details['menu_file'] = [restaurant_json['restaurantSlug'] + '.csv']

        except KeyError as e:
            self.__flag = False
            self.__restaurant_details = {}
            logging.error(f'Invalid key {e}')

        except Exception as e:
            self.__restaurant_details = {}
            self.__flag = False
            logging.error(e)

        # call other function(s)
        if self.__flag:
            self.__fetch_restaurant_menu_details()

    def __fetch_restaurant_menu_details(self):
        try:
            menu_json = self.__details_json['props']['pageProps']['initialMenuState']['menuData']['items']

            if len(menu_json) < 1:
                self.__flag = False
                return

            for menu in menu_json:
                temp = {
                    'item_name': menu['name'],
                    'item_description': menu['description'],
                    'item_price': float(menu['price']),
                    'item_image': menu['image']
                }
                self.__restaurant_menu_details.append(temp)

        except KeyError as e:
            self.__flag = False
            # self.__restaurant_menu_details = []
            logging.error(f'Invalid key {e}')

        except Exception as e:
            self.__flag = False
            # self.__restaurant_menu_details = []
            logging.error(e)

    def get_restaurant_details(self) -> {}:
        return self.__restaurant_details

    def get_restaurant_menu(self) -> list:
        return self.__restaurant_menu_details

    def write_to_csv(self):
        if self.__flag and self.__restaurant_details != {} and self.__restaurant_menu_details != []:
            self.__write_restaurant_details()
            self.__write_restaurant_menu()

        else:
            logging.error(f'Cannot write into file')

    def __write_restaurant_details(self):
        makedirs(self.__base_dir, exist_ok=True)
        filename = self.__base_dir / (self.__filename + '.csv')

        try:
            df_1 = read_csv(filename)
            df_2 = DataFrame(self.__restaurant_details)
            df = concat([df_1, df_2])
            df.drop_duplicates(inplace=True)
            df.to_csv(filename, index=False)

        except FileNotFoundError:
            df = DataFrame(self.__restaurant_details)
            df.to_csv(filename, index=False)

        except Exception as e:
            logging.error(f'{e}\nCannot write restaurant details')

    def __write_restaurant_menu(self):
        makedirs(self.__menu_dir, exist_ok=True)
        filename = self.__menu_dir / self.__restaurant_details['menu_file'][0]

        try:
            df = DataFrame(self.__restaurant_menu_details)
            df.to_csv(filename, index=False)
        except Exception as e:
            logging.error(f'{e}\nCannot write restaurant menu details')
