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


def write_excel_title(sheet, title_name):
    for i in range(len(title_name)):
        sheet.write(0, i, title_name[i])


start_url = 'https://www.tripadvisor.cn/Restaurants-g297407-Xiamen_Fujian.html#EATERY_OVERVIEW_BOX'
headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
herf = 'https://www.tripadvisor.cn'
url_queue = Queue.Queue()
url_queue.put(start_url)
res_info = []
title_name = ['Restaurant Name', 'City', 'Restaurant Score', 'Restaurant Rank', 'Restaurant Comments', 'Comments Info Href']
workbook = Workbook()
sheet = workbook.add_sheet('Restaurant food information')
write_excel_title(sheet, title_name)
base_count = 0
row_count = 1
file_count = 1

while not url_queue.empty():
    base_count += 1
    print(base_count)
    cur_url = url_queue.get()
    mainreq = urllib2.urlopen(urllib2.Request(cur_url, headers=headers))
    tree = lxml.html.fromstring(mainreq.read())
    # res_name:餐厅名、comments:餐厅总的评论数、comment_hrefs:餐厅评论主页
    # scores:餐厅打分五分制、herf主网址、next_rank:餐厅排名，next_page:下一个爬取的网页
    res_name = tree.xpath('//div[@class="title"]/a/text()')
    res_comments = tree.xpath('//div[@class="rating rebrand"]/span[@class="reviewCount"]/a/text()')
    comment_hrefs = tree.xpath('//div[@class="rating rebrand"]/span[@class="reviewCount"]/a/@href')
    res_scores = tree.xpath('//div[@class="rating rebrand"]/span/@alt')
    res_rank = tree.xpath('//div[@class="popIndex rebrand popIndexDefault"]/text()')
    next_page = tree.xpath('//div[@class="unified pagination js_pageLinks"]/a/@href')
    max_length = max(len(res_name), len(res_comments), len(comment_hrefs), len(res_scores), len(res_rank))
    res_name = res_name + ['NULL' for i in range(max_length-len(res_name))]
    res_comments = res_comments + ['NULL' for i in range(max_length-len(res_comments))]
    comment_hrefs = comment_hrefs + ['NULL' for i in range(max_length-len(comment_hrefs))]
    res_scores = res_scores + ['NULL' for i in range(max_length-len(res_scores))]
    res_rank = res_rank + ['NULL' for i in range(max_length-len(res_rank))]
    for i in range(max_length):
        res_info.append([res_name[i], '厦门', res_scores[i], res_rank[i], res_comments[i], herf+comment_hrefs[i]])
    if len(res_info) >= 3000:
        for i in range(len(res_info)):
            for j in range(len(res_info[i])):
                sheet.write(row_count, j, unicode(res_info[i][j]))
            row_count += 1
        print('Generate file count:' + str(file_count))
        workbook.save('Xiamen_Maotuying_Restaurant_Information%d.xls' % file_count)
        del res_info[:]
        workbook = Workbook()
        sheet = workbook.add_sheet('Restaurant food information')
        write_excel_title(sheet, title_name)
        row_count = 1
        file_count += 1
    if len(next_page) > 0:
        next_url = herf + next_page[-1]
        url_queue.put(next_url)

for i in range(len(res_info)):
    for j in range(res_info[i]):
        sheet.write(row_count, j, res_info[i][j])
    row_count += 1
workbook.save('Maotuying_Restaurant_Information%d.xls' % file_count)
del res_info



