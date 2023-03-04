#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：deskTip
@File    ：Item.py
@Author  ：Aidan Lew
@Date    ：2022/10/1 14:20
"""


class Item:
    """
        item_time：Date
    """

    def __init__(self, item_id, date, item_name, item_type, state=0, link=""):
        self.item_id = item_id
        self.item_date = date
        self.item_name = item_name
        self.item_type = item_type
        self.state = state
        self.link = link

    def __str__(self):
        ss = "-"
        return f"{ss * 50}\n" \
               f"item_id:{self.item_id}\n" \
               f"item_date:{self.item_date}\n" \
               f"item_name:{self.item_name}\n" \
               f"item_type:{self.item_type}\n" \
               f"state:{self.state}\n" \
               f"link:{self.link}\n" \
               f"{ss * 50}\n"

    # 在id相等的情况比较(此情况只用比较名字和状态)
    def __eq__(self, other):
        return self.item_name == other.item_name and self.state == other.state

    def str4DB(self):
        return f"'{self.item_id}','{self.item_date}','{self.item_name}',{self.item_type},{self.state},'{self.link}'"
