from talabat_crawler.crawler import Crawler

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

    for l in talabat_links:
        tc = Crawler(l)
        tc.write_to_csv()
