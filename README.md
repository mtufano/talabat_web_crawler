# Talabat Web Crawler
Web Crawler to fetch Restaurant and Menu details from [talabat](https://www.talabat.com/).

## Repository Structure
```
talabat_web_crawler/
└── main/
    ├── crawled_data/
    │   ├── crawled_data.csv
    │   └── menus/
    │       ├── cheat-day-jlt.csv
    │       ├── cinnabon-tgo.csv
    │       ├── everyday-roastery-business-bay.csv
    │       ├── ginos-deli-khalifa-city.csv
    │       ├── gorilla-burgers.csv
    │       ├── pasta-della-nona.csv
    │       ├── pizza-di-rocco.csv
    │       ├── pizzaro.csv
    │       ├── the-pasta-guyz.csv
    │       └── wingo--house-of-wings.csv
    ├── LICENSE
    ├── main.py
    ├── README.md
    ├── requirements.txt
    └── talabat_crawler/
        ├── __init__.py
        └── crawler.py
```
## Before starting
Make sure you have -
1. [Python v3.10.x](https://www.python.org/downloads/) installed in your system.
2. Run `pip install -r requirements.txt` to install required packages.

## How to use?
```python
# Import the Crawler class
from talabat_crawler.crawler import Crawler

# The URL to the restaurant page
url = "https://www.talabat.com/uae/restaurant/621133/ginos-deli-jlt?aid=1308"

# Create a Crawler instance
# crawler_instance = Crawler(url, base_dir, f_name, menu_dir)
# url -> The url from talabat.com
# base_dir -> Directory where the files will be saved [default='crawled_data']
# f_name -> File name for the csv file [default='crawled_data']
# menu_dir -> Directory to save the menus [default='menus']
tc = Crawler(url)

# Call write_to_csv() to write the crawled data into csv file
tc.write_to_csv()
```