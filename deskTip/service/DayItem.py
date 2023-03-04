#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from DAO.Database import Database as DB

"""
@Project ：deskTip
@File    ：DayItem.py
@Author  ：Aidan Lew
@Date    ：2022/10/1 14:49

"""


class DayItem:

    def __init__(self, date):
        self.date = date.toPyDate()
        self.items = DB.get_items(self.date)
        # for item in self.items:
        #     print(item)

    def get_items(self, date):
        self.date = date.toPyDate()
        self.items = DB.get_items(self.date)
        for item in self.items:
            print(item)
        return self.items

    def add_item(self, new_item):
        self.items.append(new_item)
        # db
        res = DB.add_item(new_item)
        return res

    def delete_item(self, item_id):
        for item in self.items:
            if item.item_id == item_id:
                self.items.remove(item)
                break
        # db
        res = DB.delete_item(item_id)
        return res

    def edit_item(self, new_items):
        results = []
        for item in new_items:
            print(str(item))
            old = DB.get_item_by_id(item.item_id)
            if old == item:
                continue
            # self.items update
            for self_item in self.items:
                if self_item.item_id == item.item_id:
                    self.items.remove(self_item)
                    self.items.append(item)
            # db
            res = DB.update_item_by_id(item.item_id, item.state, item.item_name)
            results.append(res)
        return not (False in results)
