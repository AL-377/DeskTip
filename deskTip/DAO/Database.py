#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：deskTip
@File    ：Database.py
@Author  ：Aidan Lew
@Date    ：2022/10/1 14:44
"""
import pymysql
from entity.Item import Item
import cryptography

# 数据表名字和属性信息
table_name = "item"
param_name = "(item_id, item_date, item_name, item_type, state, link)"
info_path = "usr/info.txt"


# 最简单的加密方式
def decoder(codes):
    before = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
              'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
              'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '.']
    after = ['s', 'd', 'C', 'l', 'U', '3', '4', 'r', 'N', '0', 'p', 'T', 'u', 'G', 'Y', 'D', 'q', 'a', 'S', 'O', 'M',
             '7', 'i', 'g', 'z', 'L', 'v', 'I', 'X', 'c', 'A', 'Q', 'P', 'B', 'h', '6', 'w', 'f', 'e', 'R', 'J', '2',
             'x', '5', 'E', 'o', '1', 'H', '9', '8', 'm', 'k', 'Z', 'W', 'b', 'F', 't', 'n', 'j', 'V', 'y', 'K', '.']
    dicts = {}
    for i in range(len(after)):
        dicts[after[i]] = before[i]

    res = ""

    for code in codes.strip():
        if dicts.__contains__(code):
            res += dicts[code]
        else:
            res += code
    print(res)

    return res


# 初始化
def pre_init():
    sql_info = []
    with open(info_path, "r") as f:
        for line in f.readlines():
            res = decoder(line)
            if len(res) > 0:
                sql_info.append(res)

    dbc = pymysql.connect(
        host=sql_info[0],
        user=sql_info[1],
        password=sql_info[2],
        charset="utf8")
    cursors = dbc.cursor()
    # 若不存在库则建库
    sql = f"CREATE DATABASE IF NOT EXISTS {sql_info[3]}"
    print(sql)
    cursors.execute(sql)
    dbc.close()

    # 重新连接数据库
    dbc = pymysql.connect(
        host=sql_info[0],
        user=sql_info[1],
        password=sql_info[2],
        database=sql_info[3],
        charset="utf8")
    cursors = dbc.cursor()

    # 在库中建表
    sql = f"""
    CREATE TABLE IF NOT EXISTS `item`  (
      `item_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
      `item_date` date NOT NULL,
      `item_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
      `item_type` int(0) NOT NULL,
      `state` int(0) NULL DEFAULT 0,
      `link` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '',
      PRIMARY KEY (`item_id`) USING BTREE
    ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic
    """
    print(sql)
    cursors.execute(sql)

    return dbc


# 连接数据库
db = pre_init()

# 使用cursor()方法获取操作游标
cursor = db.cursor()


class Database:

    @classmethod
    def get_items(cls, item_date):
        # 要带引号
        sql = f"""select * from {table_name} where item_date = "{item_date}" """
        print("sql:", sql)
        # 四个象限的items
        items = []
        try:
            # 执行 sql 语句
            cursor.execute(sql)
            # 显示出所有数据
            data_result = cursor.fetchall()
            for row in data_result:
                item_id = row[0]
                item_date = row[1]
                item_name = row[2]
                item_type = row[3]
                state = row[4]
                link = row[5]
                newItem = Item(item_id, item_date, item_name, item_type, state, link)
                # 增加
                items.append(newItem)
            # check
            for item in items:
                print(item)

        except Exception as e:
            print(e.args)

        return items

    @classmethod
    def add_item(cls, new_item):

        sql = f"""INSERT INTO {table_name}{param_name}
                 VALUES ({new_item.str4DB()})"""
        print(sql)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()

        except Exception as e:
            print(e.args)
            # 回滚
            db.rollback()
            return False
        return True

    @classmethod
    def delete_item(cls, item_id):
        sql = f"DELETE FROM {table_name} where item_id = '{item_id}' "
        print(sql)

        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except Exception as e:
            print(e.args)
            # 发生错误时回滚
            db.rollback()
            return False
        return True

    @classmethod
    def get_item_by_id(cls, item_id):
        sql = f"""select * from {table_name} where item_id = "{item_id}" """
        print("sql:", sql)
        newItem = None
        try:
            # 执行 sql 语句
            cursor.execute(sql)
            # 显示数据
            row = cursor.fetchone()
            item_id = row[0]
            item_date = row[1]
            item_name = row[2]
            item_type = row[3]
            state = row[4]
            link = row[5]
            newItem = Item(item_id, item_date, item_name, item_type, state, link)

        except Exception as e:
            print(e.args)

        return newItem

    # 目前仅支持更新state和name
    @classmethod
    def update_item_by_id(cls, item_id, new_state, new_name):
        sql = f"""UPDATE {table_name} SET state = '{new_state}', item_name = '{new_name}' WHERE item_id = '{item_id}'"""
        print("sql:", sql)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except Exception as e:
            print(e.args)
            # 发生错误时回滚
            db.rollback()
            return False
        return True

    @classmethod
    def get_item_by_date(cls, target_date, date_range):
        target_date_info = [target_date.strftime("%Y"), target_date.strftime("%Y%m"), target_date.strftime("%Y%m%d")]
        print(target_date_info)
        sql = ""
        if date_range == 0:
            sql = f"""select * from {table_name} where DATE_FORMAT(item_date,'%Y') = '{target_date_info[date_range]}' """
        if date_range == 1:
            sql = f"""select * from {table_name} where DATE_FORMAT(item_date,'%Y%m') = '{target_date_info[date_range]}' """
        if date_range == 2:
            sql = f"""select * from {table_name} where DATE_FORMAT(item_date,'%Y%m%d') = '{target_date_info[date_range]}' """

        print("sql:", sql)
        # 满足要求的items
        items = []
        try:
            # 执行 sql 语句
            cursor.execute(sql)
            # 显示出所有数据
            data_result = cursor.fetchall()
            for row in data_result:
                item_id = row[0]
                item_date = row[1]
                item_name = row[2]
                item_type = row[3]
                state = row[4]
                link = row[5]
                newItem = Item(item_id, item_date, item_name, item_type, state, link)
                # 增加
                items.append(newItem)

            # check
            for item in items:
                print(item)

        except Exception as e:
            print(e.args)

        return items
