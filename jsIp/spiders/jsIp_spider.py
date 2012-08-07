from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy import log

from selenium import webdriver

from datetime import datetime
from pytz import timezone
from urlparse import urljoin
import time

from jsIp.loaders import (CountryLoader, ProxyInfoLoader)


class jsIp(BaseSpider):
    name = 'jsIp'
    allowed_domains = ['spys.ru', 'spys.ru/en/']
    base_domain = 'http://spys.ru'

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self):
        log.msg("Openning browser", level=log.INFO)
        self.browser = webdriver.Firefox()
        pass

    def spider_closed(self):
        self.browser.quit()
        log.msg("Browser closed", level=log.INFO)
        pass

    # This gets your start page and directs it to get parse manager
    def start_requests(self):
        return [Request("http://spys.ru/en/proxy-by-country/", callback=self.parseMgr)]

    # the parse manager deals out what to parse and start page extraction
    def parseMgr(self, response):
        log.msg("ParseManager", level=log.INFO)

        # Front page
        yield self.frontPage(response)

        # Extract TLD pages to follow
        paths = HtmlXPathSelector(response).select("//tr[@class='spy1x']/td[3]/a/@href").extract()
        for path in paths:
            yield Request(urljoin(self.base_domain, path), callback=self.pageParser)

    def frontPage(self, response):
        log.msg("FronPage: %s" % response.url, level=log.INFO)

        loader = CountryLoader(response=response)
        loader.add_xpath('TLD', "//td[2]/font[@class='spy4']/text()")
        loader.add_xpath('country', "//td[3]/a/font[@class='spy6']/text()")
        loader.add_xpath('count', "//td[3]/font[@class='spy4']/text()")
        loader.add_value('dlTimestamp', datetime.now(timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S %z"))
        return loader.load_item()

    def pageParser(self, response):
        log.msg("Page: %s" % response.url, level=log.INFO)

        yield self.pageLoader(response)

        # Follow pages
        pages = HtmlXPathSelector(response).select("//tr[@class='spy1xx'][1]/td[1]/a/@href").extract()[1:-1]
        if pages:
            for page in pages:
                yield Request(urljoin(self.base_domain, page), callback=self.pageLoader)

    def pageLoader(self, response):
        log.msg("Loading page: %s" % response.url, level=log.INFO)

        # Initiate Selenium for javascript
        br = self.browser
        br.get(response.url)

        log.msg("loading JS", level=log.INFO)
        time.sleep(2.5)

        loader = ProxyInfoLoader(response=response)
        loader.add_value('dlTimestamp', datetime.now(timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S %z"))
        loader.add_value('proxyIP', [i.text for i in br.find_elements_by_xpath("//tr[@class='spy1xx']/td[1]/font[@class='spy14']")])
        loader.add_xpath('proxyType', "//tr[@onmouseover]/td[2]/font[@class='spy1']/text()")
        loader.add_xpath('anon', "//tr[@onmouseover]/td[3]/child::*/text()")
        loader.add_xpath('location', "//tr[@class='spy1xx']/td[4]/node()")
        loader.add_xpath('bang', "//tr[@class='spy1xx']/td[4]/node()")
        loader.add_xpath('hostName', "//tr[@class='spy1xx']/td[5]/font[@class='spy1']/text()")
        loader.add_xpath('lastUpdate', "//tr[@class='spy1xx']/td[6]/font//text()")

        return loader.load_item()
