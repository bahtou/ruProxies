from scrapy.contrib.loader.processor import Identity
from scrapy.contrib.loader import XPathItemLoader
from scrapy import log

from jsIp.items import (proxyInfo, ipCountry)
from jsIp.processors import (lastUpdate, LocationParser, Banging)


class RootItemLoader(XPathItemLoader):
    log.msg("Root Loader", level=log.INFO)
    default_input_processor = Identity()
    default_ouput_processor = Identity()


class ProxyInfoLoader(RootItemLoader):
    default_item_class = proxyInfo
    location_out = LocationParser()
    bang_out = Banging()
    lastUpdate_in = lastUpdate()


class CountryLoader(RootItemLoader):
    default_item_class = ipCountry
