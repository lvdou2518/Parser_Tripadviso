# -*- coding=utf-8 -*-
import Queue
import sys
import json
import lxml.html
import urllib2
import requests
from xlwt import Workbook

reload(sys)
sys.setdefaultencoding('UTF-8')


def city_page(city_url, city_name, headers):
    log_count = 1
    city_total_urls = [city_url]
    url_queue = Queue.Queue()
    url_queue.put(city_url)
    while not url_queue.empty():
        cur_url = url_queue.get()
        print(city_name + '子网页' + str(log_count))
        log_count += 1
        mainreq = urllib2.urlopen(urllib2.Request(cur_url, headers=headers))
        tree = lxml.html.fromstring(mainreq.read())
        href_list = tree.xpath('//div[@class="b_paging"]/a[@class="page next"]/@href')
        if len(href_list) > 0:
            next_url = href_list[0]
            url_queue.put(next_url)
            city_total_urls.append(next_url)
    return city_total_urls


def parse_page(city_url, headers):
    mainreq = urllib2.urlopen(urllib2.Request(start_url, headers=headers))
    tree = lxml.html.fromstring(mainreq.read())
    jingdian_name = tree.xpath('//div[@class="strategy_sum"]/text()')
    jingdian_rank = tree.xpath('//div[@class="qn_main_ct_l"]//span[@class="ranking_sum"]/span[@class="sum"]/text()')
    print('zhanglei')
    print(len(jingdian_name))
    print(len(jingdian_rank))

def parse_city(start_url, headers):
    mainreq = urllib2.urlopen(urllib2.Request(start_url, headers=headers))
    tree = lxml.html.fromstring(mainreq.read())
    href_list = tree.xpath('//div[@class="contbox current"]//li[@class="item "]/a/@href')
    dest_list = tree.xpath('//div[@class="contbox current"]//li[@class="item "]/a/text()')
    city_url_list = []
    for i in range(len(href_list)):
        if dest_list[i] == '中国':
            break
        city_url_list.append(href_list[i] + '-jingdian')
    #tlist = city_page(city_url_list[0], dest_list[0], headers)
    #total_urls = []
    #for i in range(len(city_url_list)):
    #    city_url, city_name = city_url_list[i], dest_list[i]
    #    temp_list = city_page(city_url, city_name, headers)
    #    total_urls.append(temp_list)
    print(city_url_list[0])
    parse_page(city_url_list[0], headers)




if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    start_url = 'http://travel.qunar.com/place/?from=header'
    parse_city(start_url, headers)



