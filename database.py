import  requests
import sqlite3
import re
from bs4 import BeautifulSoup
import numpy as np

class Db:
    conn = None
    cur = None

    def getConn():
        Db.conn = sqlite3.connect("illegator.db")
        Db.cur = Db.conn.cursor()

    def create_main():
        Db.cur.execute('''DROP TABLE IF EXISTS illegator''')
        Db.cur.execute('''
        CREATE TABLE IF NOT EXISTS illegator(id integer,
        url text,
        screenshot text)
        ''')

    #tag keyword externalLink
    def create(type):
        Db.cur.execute("DROP TABLE IF EXISTS "+type)
        Db.cur.execute('''
        CREATE TABLE IF NOT EXISTS {}(
        id integer,
        {} text)
        '''.format(type, type))

    #id url screenshot
    def insert_main(A, B, C):
        ins_sql="insert into illegator values(?,?,?)"
        Db.cur.execute(ins_sql,(A, B, C))

    def insert(type, A, B):
        ins_sql="insert into {} values(?,?)".format(type)
        Db.cur.execute(ins_sql,(A, B))

    def select(type, id):
        if(type == "url" or type == "screenshot"):
            sql="select * from illegator where id = '{}'".format(id)
            Db.cur.execute(sql)
            search = Db.cur.fetchone()
            return search
        else:
            sql = "select {} from {} where id = {}".format(type, type, id)
            Db.cur.execute(sql)
            search = Db.cur.fetchall()
            return search

    def endConn():
        Db.conn.commit()
        Db.conn.close()

if __name__=='__main__':