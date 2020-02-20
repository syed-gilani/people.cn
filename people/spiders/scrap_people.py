# -*- coding: utf-8 -*-
import scrapy
import urllib
from selenium import webdriver
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
from people.items import PeopleItem


class ScrapPeopleSpider(scrapy.Spider):
    name = 'scrap_people'
    allowed_domains = ['en.people.cn']
                      #'search.people.com.cn/language/search.do',
                      #'search.people.com.cn/language/english/getResult.jsp']
    start_urls = ['http://en.people.cn/']

    #initalize the webdriver
    def __init__(self):
        self.driver = webdriver.Chrome()


    def parse(self, response):
        self.driver.get(response.url)
        formdata = {'dataFlag':'false',
                    'siteName': 'english',
                    'pageNum': '1',
                    'keyword': '-'}
        yield FormRequest.from_response(response,
                            formname='searchForm',
                            formdata=formdata,
                            dont_filter=True,
                            callback=self.parse1)

    def parse1(self, response):
        print(response.url)
        #self.driver.get(response.url)
        for node in response.xpath("//div[@class='clear']/ul[@class='on1 clear']"):
            article_name = node.xpath("./li/b/a/text()").extract()
            publish_date = node.xpath("./li[3]/text()").extract()[0].replace(u"\xa0", "")
            article_text = node.xpath("./li/a/@href").extract()
            p = PeopleItem(article_name="".join(article_name), publish_date=publish_date, article_text=article_text[0])
            yield Request(article_text[0], callback=self.getArticleText, meta={'item': p}, dont_filter=True)
        next_button = response.xpath("//div[contains(@class, 'wb_18')]/a[contains(text(), 'Next ')]/@href").extract()
        print("Click Next Button")
        if len(next_button) > 0:
            print("scraping next page")
            yield Request(response.urljoin(next_button[0]), callback=self.parse1, dont_filter=True)
        print("Next Button clicked")
        
    def getArticleText(self, response):
        sel = Selector(response) 
        article_text = sel.xpath("//*[contains(@class, 'wb_12 clear')]")
        people_item = response.meta['item']
        if len(article_text) > 0:
            people_item['article_text'] = article_text[0].extract()
        else:
            article_text = sel.xpath("//*[contains(@id, 'p_content')]")
            if len(article_text) > 0 :
                people_item['article_text'] = article_text[0].extract()
        yield people_item

