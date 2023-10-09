from talabat_crawler.crawler import Crawler
import time
from random import randrange

counter = 0
with open('restaurant_urls.txt') as file:
    for url in file:
        counter += 1

        if counter <= 29000:
            continue
        
        tc = Crawler(url.strip())
        tc.write_to_csv()
        
        time.sleep(randrange(1,4))
                
        if counter % 500 == 0:
            print(counter)
            time.sleep(randrange(150, 250))
            
    file.close()
