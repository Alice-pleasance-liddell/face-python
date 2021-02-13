# -*- coding: utf-8 -*-

import sqlite3

FACE_SQL_NAME = "face.db"

SQL_CREATE_TABLE = \
    '''
    CREATE TABLE IF NOT EXISTS FACE_INFO (
        ID integer PRIMARY KEY autoincrement NOT NULL,
        NAME TEXT NOT NULL,
        FACE_FEATURE array not null
    );'''

SQL_INSERT_DATA = [
    "INSERT INTO FACE_INFO (ID,NAME,IMAGE_PATH) VALUES (1, 'Paul',null )",
    "INSERT INTO FACE_INFO (ID,NAME,IMAGE_PATH) VALUES (2, 'Allen',null )",
    "INSERT INTO FACE_INFO (ID,NAME,IMAGE_PATH) VALUES (3, 'Teddy',null )",
    "INSERT INTO FACE_INFO (ID,NAME,IMAGE_PATH) VALUES (4, 'Mark',null )"
]

SQL_QUERY_DATA = "SELECT id, name FROM FACE_INFO"

SQL_UPDATE_DATA = "UPDATE FACE_INFO set IMAGE_PATH = null where ID=1"

SQL_DELETE_DATA = "DELETE from FACE_INFO where ID=2;"


def create_sqlite3(sql_name):
    '''
    根据数据库名字 创造 或者 连接 数据库
    :param sql_name:要创造或者连接的数据库名
    :return:conn 返回的是这个数据库的对象
    '''
    conn = sqlite3.connect(sql_name)
    return conn

def create_table(conn, sql):
    '''
    向 该数据库创建一个表
    :param conn: 需要操作的表
    :param sql: 需要执行的语句
    :return: 创建成功返回true， 失败返回false
    '''
    sqlite_exec_sql(conn, sql)
    return True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def sqlite_exec_sql(conn, sql):
    '''
    执行指定的SQL语句
    :param conn: 数据库的对象（他是哪个数据库）
    :param sql: 需要执行的语句时什么
    :return: cursor 返回受影响的行数
    '''
    # cursor用来执行命令的方法
    c = conn.cursor()
    cursor = c.execute(sql)
    # c.close()

    return cursor

def init_data():
    conn = create_sqlite3(FACE_SQL_NAME)
    create_table(conn, SQL_CREATE_TABLE)
    conn.commit()
    conn.close()

 