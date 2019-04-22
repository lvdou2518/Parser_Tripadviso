# -*- coding=utf-8 -*-
import os
import xlrd
from xlwt import Workbook


def write_excel_title(sheet, title_name):
    for i in range(len(title_name)):
        sheet.write(0, i, title_name[i])


def in_out_file(input_file_path, output_file_path):
    title_name = ['Restaurant Name', 'City', 'Restaurant Score', 'Restaurant Rank', 'Restaurant Comments', 'Comments Info Href']
    work_book = Workbook()
    sheet = work_book.add_sheet('Restaurant food information')
    #write_excel_title(sheet, title_name)
    row_count = 0
    for filename in os.listdir(input_file_path):
        open_book = xlrd.open_workbook(os.path.join(input_file_path, filename))
        open_sheet = open_book.sheet_by_index(0)
        for i in range(1, open_sheet.nrows):
            res_score = open_sheet.cell_value(rowx=i, colx=2)
            res_rank = open_sheet.cell_value(rowx=i, colx=3)
            res_comment = open_sheet.cell_value(rowx=i, colx=4)
            if res_score == 'NULL' and res_rank == 'NULL' and res_comment == 'NULL':
                continue
            for j in range(open_sheet.ncols):
                sheet.write(row_count, j, open_sheet.cell_value(rowx=i, colx=j))
            row_count += 1
    print('Generating file Done')
    work_book.save(os.path.join(output_file_path, 'Maotuying_Restaurant_Total_Information_Use.xls'))


if __name__ == '__main__':
    input_file_path = '/nfs/private/zhanglei/2019/note_own/parser/data_restaurant'
    output_file_path = '/nfs/private/zhanglei/2019/note_own/parser'
    in_out_file(input_file_path, output_file_path)





