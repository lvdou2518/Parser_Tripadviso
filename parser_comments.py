# -*- coding=utf-8 -*-
import os
import xlrd
import Queue
import sys
import json
import lxml.html
import urllib2
import requests
from xlwt import Workbook


reload(sys)
sys.setdefaultencoding('UTF-8')
headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}


def write_excel_title(sheet, title_name):
    for k in range(len(title_name)):
        sheet.write(0, k, title_name[k])


comment_info = []
title_name = ['User Id', 'User Location', 'Restaurant Name', 'Restaurant Location', 'Comment Title', 'Comment Content', 'Comment Time']
workbook = Workbook()
sheet = workbook.add_sheet('User Comments information')
write_excel_title(sheet, title_name)
row_count = 1
file_count = 1


path = '/nfs/private/zhanglei/2019/note_own/parser/data/hangzhou'
for filename in os.listdir(path):
    open_book = xlrd.open_workbook(os.path.join(path, filename))
    print(filename)
    open_sheet = open_book.sheet_by_index(0)
    for i in range(1, open_sheet.nrows):
        res_name = open_sheet.cell_value(rowx=i, colx=0)
        res_loc = open_sheet.cell_value(rowx=i, colx=1)
        comment_href = open_sheet.cell_value(rowx=i, colx=5)
        try:
            mainreq = urllib2.urlopen(urllib2.Request(comment_href, headers=headers))
        except urllib2.URLError, err:
            continue
        except urllib2.HTTPError, err:
            continue
        tree = lxml.html.fromstring(mainreq.read())
        user_id = tree.xpath('//div[@class="member_info"]/div/@id')
        user_id = [user_id[j] for j in range(0, len(user_id), 2)]
        user_loc = tree.xpath('//div[@class="userLoc"]/strong/text()')
        comment_title = tree.xpath('//span[@class="noQuotes"]/text()')
        comment_content = tree.xpath('//p[@class="partial_entry"]/text()')
        comment_time = tree.xpath('//span[@class="ratingDate"]/@title')
        # res_name:餐厅名、user_id:评论者id、user_loc:评论者居住地
        # comment_title:评论主题、comment_content:评论内容、comment_time:评论时间
        user_loc = user_loc + ['NULL' for j in range(len(user_id)-len(user_loc))]
        comment_title = comment_title + ['NULL' for j in range(len(user_id)-len(comment_title))]
        comment_content = comment_content + ['NULL' for j in range(len(user_id)-len(comment_content))]
        comment_time = comment_time + ['NULL' for j in range(len(user_id)-len(comment_time))]
        for j in range(len(user_id)):
            comment_info.append([user_id[j], user_loc[j], res_name, res_loc, comment_title[j], comment_content[j], comment_time[j]])
        print(len(comment_info), i)
        if len(comment_info) > 3000:
            for k in range(len(comment_info)):
                for j in range(len(comment_info[k])):
                    sheet.write(row_count, j, unicode(comment_info[k][j]))
                row_count += 1
            print('Generate file count:' + str(file_count))
            workbook.save('Hangzhou_Maotuying_Comments_Information%d.xls' % file_count)
            del comment_info[:]
            workbook = Workbook()
            sheet = workbook.add_sheet('User Comments information')
            write_excel_title(sheet, title_name)
            row_count = 1
            file_count += 1

for k in range(len(comment_info)):
    for j in range(len(comment_info[k])):
        sheet.write(row_count, j, comment_info[k][j])
    row_count += 1
workbook.save('Hangzhou_Maotuying_Comments_Information%d.xls' % file_count)
del comment_info
print('End!')







