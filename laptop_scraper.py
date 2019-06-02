# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import pickle
import sys
from scrapy.crawler import CrawlerProcess
class LaptopScraperSpider(scrapy.Spider):   
  name = 'laptop_scraper'
  start_urls = ['https://www.flipkart.com/search?q=Laptop&page=1']
  all_laptop_data = []
  no_laptops = (int(sys.argv[1]))-1
  pickled_dir = sys.argv[2]
  def parse(self, response):
        flag=True
        for laptop in response.xpath("//div[@class='_1UoZlX']"):
            laptop_name = laptop.xpath(".//div/div[@class='_3wU53n']/text()").get()
            laptop_price = laptop.xpath(".//div/div[@class='_1vC4OE _2rQ-NK']/text()").get()
            laptop_rating = laptop.xpath(".//div[@class='hGSR34']/text()").get()
            data = {'name': laptop_name, 'price': laptop_price, 'rating': laptop_rating}
            self.all_laptop_data.append(data)
            yield data
            if len(self.all_laptop_data) <= self.no_laptops:
                pass
            else:
                flag=False
                break
        # to go to the next page
        next_page= response.css('a._3fVaIS::attr(href)').extract_first()
        if next_page and flag:
            next_page_url = response.urljoin(next_page[-1]) # pick the "next" url
            yield Request(next_page_url, callback=self.parse)
        pickle.dump(self.all_laptop_data,(open("pickled_dir","wb")))
begin = CrawlerProcess()
begin.crawl(LaptopScraperSpider)
begin.start()

        