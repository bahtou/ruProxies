# Define here the models for your processors that the items will pass through
#
from scrapy import log
import re
from datetime import datetime


class LocationParser(object):
    def __init__(self):
        self.crty = re.compile('(?:>)(\w+)')
        self.city = re.compile('(?:>\()(\w+)')
        self.bang = re.compile('!')

    def __call__(self, values):
        locRow = [(self.crty.findall(row), self.city.findall(row), self.bang.findall(row)) for row in values]
        unlist = self.unList(locRow)
        cityList = self.listCity(unlist)
        return cityList

    def unList(self, loc):
        tt = [[] for _ in range(len(loc))]
        for j in range(len(loc)):
            for i in loc[j]:
                if i:
                    tt[j].append(i[0])
        return tt

    def listCity(self, loc):
        kk = []
        for i in loc:
            if len(i) == 1:
                kk.append(i[0])
            elif len(i) == 2 and i[1] == '!':
                kk.append(i[0])
            else:
                kk.append(i[1])
        return kk


# modifies lastUpdate string for SQL data type
class lastUpdate(object):
    log.msg('last update edit', level=log.INFO)

    def __call__(self, values):
        lastUpdate = []
        for i in range(0, len(values), 2):
            dtime = datetime.strptime(values[i] + values[i + 1], "%d-%b-%Y %H:%M")
            lastUpdate.append(dtime.strftime("%Y-%m-%d %H:%M"))
        return lastUpdate


class Banging(object):
    def __init__(self):
        self.crty = re.compile('(?:>)(\w+)')
        self.city = re.compile('(?:>\()(\w+)')
        self.bang = re.compile('!')

    def __call__(self, values):
        locRow = [(self.crty.findall(row), self.city.findall(row), self.bang.findall(row)) for row in values]
        unlist = self.unList(locRow)
        bang = self.getBang(unlist)
        return bang

    def unList(self, loc):
        tt = [[] for _ in range(len(loc))]
        for j in range(len(loc)):
            for i in loc[j]:
                if i:
                    tt[j].append(i[0])
        return tt

    def getBang(self, loc):
        bang = []
        for i in loc:
            if '!' in i:
                bang.append(u'True')
            else:
                bang.append(u'False')
        return bang
