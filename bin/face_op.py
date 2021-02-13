# -*- coding: utf-8 -*-

import io
import zlib
import sqlite3
import sql as sql_op
import numpy as np


def sql_con():
    '''
    建立数据库的连接
    :return: 返回给数据库的对象
    '''
    return sql_op.create_sqlite3(sql_op.FACE_SQL_NAME)

def face_query_all(conn):
    '''
    查询所有数据库
    :param conn:需要连接数据库的对象
    :return:查到数据返回cursor，受影响的哪一行
    '''
    sql = "select * from FACE_INFO"
    cursor = sql_op.sqlite_exec_sql(conn, sql)
    result = cursor.fetchall()
    cursor.close()

    return result

def face_del(conn, face_name):
    '''
    根据图片名字删除指定的人脸数据
    :param conn: 数据库
    :param face_name:需要删除的图片的名字
    :return:如果删除成功返回True
    '''
    sql = "DELETE from FACE_INFO where NAME='" + face_name + "'"
    cursor = sql_op.sqlite_exec_sql(conn, sql)
    conn.commit()

def face_query(conn, face_name):
    '''
    根据姓名查询此人的人脸图片
    :param conn: 该数据库的对象
    :param face_name：需要查询的人名
    :return: cursor：返回的是收到影响的行
    '''
    sql = "select ID,NAME,IMAGE_PATH from FACE_INFO where NAME='" + face_name + "'"
    cursor = sql_op.sqlite_exec_sql(conn, sql)
    return cursor

def face_query_by_name(conn, name):
    '''
    根据姓名查询此人相关信息
    :param coon: 需要连接的数据库名
    :param id: 需要查询的id
    :return:  查到数据返回cursor，受影响的哪一行
    '''
    sql = "select ID, NAME, FACE_FEATURE from FACE_INFO where NAME='" +str(name) + "'"
    cursor = sql_op.sqlite_exec_sql(conn, sql)
    result = cursor.fetchall()
    cursor.close()

    return result

def face_insert(conn, name, face_feature):
    '''
    将人的相关信息（id，name，人脸图片）插入到数据库之中去
    :param conn: 该数据库的对象
    :param id: 唯一id
    :param name: 人脸的姓名
    :param img_path: 人脸的图片路径
    :return:True数据插入成功，Talse数据插入失败
    '''
    cur = conn.cursor()  # 得到游标对象

    try:
        cur.execute("insert into FACE_INFO (NAME,FACE_FEATURE) values(?,?)",(name,adapt_array(face_feature)))
    except sqlite3.IntegrityError as result:
        print("数据插入失败，原因：", result)
        return False
    else:
        conn.commit()
        return True

def face_del_by_name(conn, name):
    '''
    根据名字删除指定的人脸数据
    :param conn: 数据库
    :return:如果删除成功返回True
    '''
    try:
        sql = "DELETE from FACE_INFO where NAME='" + str(name) + "'"
        cursor = sql_op.sqlite_exec_sql(conn, sql)
        conn.commit()
    except Exception as e:
        print("发生异常",e)
        conn.rollback()
        return False
    else:
        return True
    finally:

        conn.close()

def face_recognition():
    """
    实现人脸识别算法(打桩)
    :return: 返回此人的姓名
    """
    return 'Aaron_Eckhart_0001'

def adapt_array(arr):
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)

        dataa = out.read()
        # 压缩数据流
        return sqlite3.Binary(zlib.compress(dataa, zlib.Z_BEST_COMPRESSION))

