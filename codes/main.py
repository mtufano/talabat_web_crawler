import json
from os import makedirs
from pathlib import Path

import pandas as pd
import validators
from bs4 import BeautifulSoup
from requests import get

base = Path('../results/')


class ValidationError(TypeError):
    def __init__(self, error_msg: str):
        self.error_message = error_msg
        print(error_msg)


class TalabatCrawler:
    def __init__(self, link: str):
        self.raw = None
        self.details_json = None
        self.restaurant_details = {}
        self.cuisine_details = []

        if validators.url(link):
            self.url = link
        else:
            raise ValidationError(f"'{link}' is not an URL")

    def put_cuisine_details(self):
        l = len(self.details_json['props']['pageProps']['initialMenuState']['menuData']['items'])
        for i in range(l):
            temp = {
                'item_name':
                    self.details_json['props']['pageProps']['initialMenuState']['menuData']['items'][i][
                        'name'],
                'item_description':
                    self.details_json['props']['pageProps']['initialMenuState']['menuData']['items'][i][
                        'description'],
                'item_price':
                    float(self.details_json['props']['pageProps']['initialMenuState']['menuData']['items'][i][
                              'price']),
                'item_image':
                    self.details_json['props']['pageProps']['initialMenuState']['menuData']['items'][i][
                        'image']
            }
            self.cuisine_details.append(temp)

    def put_restaurant_details(self):
        self.restaurant_details['restaurant_name'] = \
            self.details_json['props']['pageProps']['initialMenuState']['restaurant']['name']
        self.restaurant_details['restaurant_logo'] = \
            self.details_json['props']['pageProps']['initialMenuState']['restaurant']['logo']
        self.restaurant_details['latitude'] = float(
            self.details_json['props']['pageProps']['initialMenuState']['restaurant']['latitude'])
        self.restaurant_details['longitude'] = float(
            self.details_json['props']['pageProps']['initialMenuState']['restaurant']['longitude'])
        self.restaurant_details['cuisine_tags'] = \
            self.details_json['props']['pageProps']['initialMenuState']['restaurant']['cuisineString']
        self.restaurant_details['menu_file'] = \
            self.details_json['props']['pageProps']['initialMenuState']['restaurant']['restaurantSlug'] + '.csv'

        if not self.cuisine_details:
            self.put_cuisine_details()

    def fetch_json_details(self):
        data = self.raw.select('#__NEXT_DATA__')[0].text
        self.details_json = json.loads(data)

    def fetch_webpage(self):
        headers = (
            {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
            }
        )
        data = get(self.url, allow_redirects=True, headers=headers)
        self.raw = BeautifulSoup(data.content, 'lxml')

    def save_crawled_data(self):
        res_file = base / 'restaurant_details.csv'
        menu_base = base / 'menu'
        restaurant_df = None

        makedirs(base, exist_ok=True)
        makedirs(menu_base, exist_ok=True)

        if self.raw is None:
            self.fetch_webpage()
        if self.details_json is None:
            self.fetch_json_details()
        if self.restaurant_details == {}:
            self.put_restaurant_details()

        res_name = self.restaurant_details['restaurant_name']
        menu_file = self.restaurant_details['menu_file']

        data_new = {k: [v] for k, v in self.restaurant_details.items()}
        data_new_df = pd.DataFrame(data_new)
        try:
            data_old_df = pd.read_csv(res_file)
            data_old_df = data_old_df.drop(data_old_df.index[data_old_df['restaurant_name'] == res_name])
            restaurant_df = pd.concat([data_old_df, data_new_df])
        except FileNotFoundError:
            restaurant_df = data_new_df
        except Exception as e:
            print(e)

        try:
            restaurant_df.to_csv(res_file, index=False)
        except Exception as e:
            print(e)

        try:
            menu_df = pd.DataFrame(self.cuisine_details)
            menu_df.to_csv(menu_base / menu_file)
        except Exception as e:
            print(e)


def main(links: list) -> None:
    for l in links:
        tc = TalabatCrawler(l)
        tc.save_crawled_data()


if __name__ == '__main__':
    talabat_links = [
        # Provided links
        "https://www.talabat.com/uae/restaurant/621133/ginos-deli-jlt?aid=1308",
        "https://www.talabat.com/uae/restaurant/645430/pasta-della-nona-jlt-jumeirah-lakes-towers?aid=1308",
        "https://www.talabat.com/uae/restaurant/50445/pizzaro-marina-3?aid=1308",
        "https://www.talabat.com/uae/restaurant/605052/the-pasta-guyz-dubai-marina?aid=1308",
        "https://www.talabat.com/uae/restaurant/621796/pizza-di-rocco-jumeirah-lakes-towers--jlt?aid=1308",
        # Other links
        'https://www.talabat.com/uae/restaurant/46443/cinnabon-dubai-marina?aid=1308',
        'https://www.talabat.com/uae/restaurant/606838/everyday-roastery-coffee-dubai-marina?aid=1308',
        'https://www.talabat.com/uae/restaurant/660366/cheat-day-jlt-jumeirah-lakes-towers?aid=1308',
        'https://www.talabat.com/uae/restaurant/650405/wingo--house-of-wings?aid=1308',
        'https://www.talabat.com/uae/restaurant/650386/gorilla-burger?aid=1308'
    ]
    main(talabat_links)
