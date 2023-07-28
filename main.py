from talabat_crawler.crawler import Crawler

if __name__ == '__main__':
    talabat_links = [
        # Provided links
        "https://www.talabat.com/uae/restaurant/621133/ginos-deli-jlt?aid=1308",
        "https://www.talabat.com/uae/restaurant/645430/pasta-della-nona-jlt-jumeirah-lakes-towers?aid=1308",
        "https://www.talabat.com/uae/restaurant/50445/pizzaro-marina-3?aid=1308",
        "https://www.talabat.com/uae/restaurant/605052/the-pasta-guyz-dubai-marina?aid=1308",
        "https://www.talabat.com/uae/restaurant/621796/pizza-di-rocco-jumeirah-lakes-towers--jlt?aid=1308",
        "https://www.talabat.com/uae/restaurant/37540/gazebo-difc?aid=1258",
        "https://www.talabat.com/uae/restaurant/619971/kamat-vegetarian-restaurant-business-bay?aid=1258",
        "https://www.talabat.com/uae/restaurant/704170/highway311-business-bay?aid=1258",
        "https://www.talabat.com/uae/restaurant/27485/huff-puff-burger-umm-suqeim-1?aid=1258",
        "https://www.talabat.com/uae/restaurant/50573/aseer-time-jumeriah-umm-suqeim-2?aid=1258",
        "https://www.talabat.com/uae/restaurant/699669/2in1-pizza-and-burger-business-bay?aid=1258",
        "https://www.talabat.com/uae/restaurant/683880/something-healthy-business-bay-2--9-tower?aid=1258",
        "https://www.talabat.com/uae/restaurant/603962/pizzaexpress-dubai-world-trade-centre?aid=1258",
        "https://www.talabat.com/uae/restaurant/37686/mandarin-oak-business-bay?aid=1258",
        "https://www.talabat.com/uae/restaurant/683818/operation-falafel-downtown-burj-khalifa?aid=1258",
        "https://www.talabat.com/uae/restaurant/666106/pinkberry-business-bay?aid=1258",
        "https://www.talabat.com/uae/restaurant/649876/sushido-business-bay?aid=1258",
        "https://www.talabat.com/uae/restaurant/702183/shawerma-alfarooj-restaurant-dubai-world-trade-center--dwtc?aid=1258",
        "https://www.talabat.com/uae/restaurant/25099/al-ijaza-cafeteria-jumeirah-1?aid=1258",









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
