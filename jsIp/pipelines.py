from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb

from jsIp.items import (ipCountry, proxyInfo)


class JsIpPipeline(object):
    def __init__(self):
        log.msg('Pipes Ready!', level=log.INFO)
        self.FPsql = "INSERT INTO ipcountry(TLD, country, count, dlTimestamp) VALUES (%s, %s, %s, %s)"
        self.Pgsql = "INSERT INTO proxies(ipPort, proxyType, anonymity, city, bang, hostName, lastUpdate, dlTimestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            db="ru_proxies",
            user='user',
            passwd='password',
            charset='utf8'
            )

    def process_item(self, item, spider):
        log.msg('Pipe processing', level=log.INFO)

        if isinstance(item, ipCountry):
            fpage = self.dbpool.runInteraction(self.frontPage_insert, item)
            fpage.addErrback(self.handle_error, item)
        elif isinstance(item, proxyInfo):
            page = self.dbpool.runInteraction(self.page_insert, item)
            page.addErrback(self.handle_error, item)

    def frontPage_insert(self, tw, item):
        log.msg('FrontPage', level=log.INFO)
        for i in range(len(item['TLD'])):
            try:
                tw.execute(self.FPsql, (item['TLD'][i], item['country'][i], item['count'][i], item['dlTimestamp'][0]))
            except MySQLdb.Error, e:
                log.msg("Error %d: %s" % (e.args[0], e.args[1]), level=log.DEBUG)

    def page_insert(self, tw, item):
        log.msg('OtherPage', level=log.INFO)
        for i in range(len(item['bang'])):
            try:
                tw.execute(self.Pgsql, (item['proxyIP'][i], item['proxyType'][i], item['anon'][i], item['location'][i], item['bang'][i], item['hostName'][i], item['lastUpdate'][i], item['dlTimestamp'][0]))
            except MySQLdb.Error, e:
                log.msg("Error %d: %s" % (e.args[0], e.args[1]), level=log.DEBUG)

    def handle_error(self, e, item):
        log.err("Error: %s %s" % (e, item))
