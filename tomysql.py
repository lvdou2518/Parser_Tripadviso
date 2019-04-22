import os
import io
import sys
import mysql.connector


class ToMysql:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def main(self):
        print('Insert data starting!')
        self.cur.execute("Load Data InFile '/var/lib/mysql-files/Maotuying_Restaurant_Total_Information_Use.csv' Into Table restaurant_info lines terminated by '\r\n'")
        self.conn.commit()
        print('Insert data ending!')


if __name__ == '__main__':
    conn = mysql.connector.connect(user='root', password='root', db='maotuying_food')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS restaurant_info(res_name TEXT, res_city TEXT, res_score TEXT, res_rank TEXT, res_comment TEXT, comment_href TEXT)')
    toMysql = ToMysql(conn, cur)
    toMysql.main()
    conn.close()
    cur.close()
