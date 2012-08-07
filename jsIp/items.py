# Data item containers

from scrapy.item import Item, Field


class proxyInfo(Item):
    proxyIP = Field()
    proxyType = Field()
    anon = Field()
    location = Field()
    bang = Field()
    lastUpdate = Field()
    hostName = Field()
    dlTimestamp = Field()


class ipCountry(Item):
    TLD = Field()
    country = Field()
    count = Field()
    dlTimestamp = Field()
