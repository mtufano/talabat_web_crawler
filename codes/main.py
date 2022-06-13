import json

import validators
from bs4 import BeautifulSoup
from requests import get


class ValidationError(TypeError):
    def __init__(self, error_msg: str):
        self.error_message = error_msg
        print(error_msg)


class TalabatCrawler:
    def __init__(self, link: str):
        self.raw = None
        self.details_json = None
        self.restaurant_details = {}

        if validators.url(link):
            self.url = link
        else:
            raise ValidationError(f"'{link}' is not an URL")

    def put_restaurant_details(self):
        self.restaurant_details['restaurant_name'] = self.details_json['name']
        self.restaurant_details['restaurant_logo'] = self.details_json['image']
        self.restaurant_details['latitude'] = float(self.details_json['geo']['latitude'])
        self.restaurant_details['longitude'] = float(self.details_json['geo']['longitude'])
        self.restaurant_details['cuisine_tags'] = self.details_json['servesCuisine']
        print(self.restaurant_details)

    def fetch_json_details(self):
        json_data = self.raw.head.select('[type="application/ld+json"]')
        for j in json_data:
            j = json.loads(str(j.text))
            if j['@type'] == 'Restaurant':
                self.details_json = j
                self.put_restaurant_details()

    def fetch_webpage(self):
        headers = (
            {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
            }
        )
        data = get(self.url, allow_redirects=True, headers=headers).content
        self.raw = BeautifulSoup(data, 'lxml')
        self.fetch_json_details()


def main(links: list) -> None:
    for l in links:
        tc = TalabatCrawler(l)
        tc.fetch_webpage()
        print('\n\n')


if __name__ == '__main__':
    talabat_links = [
        # Provided links
        "https://www.talabat.com/uae/restaurant/621133/ginos-deli-jlt?aid=1308",
        "https://www.talabat.com/uae/restaurant/645430/pasta-della-nona-jlt-jumeirah-lakes-towers?aid=1308",
        "https://www.talabat.com/uae/restaurant/50445/pizzaro-marina-3?aid=1308",
        "https://www.talabat.com/uae/restaurant/605052/the-pasta-guyz-dubai-marina?aid=1308",
        "https://www.talabat.com/uae/restaurant/621796/pizza-di-rocco-jumeirah-lakes-towers--jlt?aid=1308",
        # Other links
    ]
    main(talabat_links)
