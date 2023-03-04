#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：deskTip 
@File    ：Recorder.py
@Author  ：Aidan Lew
@Date    ：2022/10/4 13:40 
"""
import tkinter as tk
from tkinter import filedialog

# 打开保存路径
from DAO.Database import Database as DB


def open_path():
    root = tk.Tk()
    root.withdraw()
    f_path = filedialog.askdirectory()
    return f_path


"""
    风格化保存
"""


def format_save(records, f_path, file_name):
    with open(f"{f_path}/record_{file_name}.txt", "w") as f:
        for record in records:
            f.write(str(record))
        f.close()


class Recorder:
    def __init__(self, record_date, record_types):
        self.record_date = record_date
        self.record_types = record_types

    """
        从数据库得到records并保存
    """

    def export_records(self):
        f_path = open_path()
        print("文件夹", f_path)
        record_items = [[], [], []]
        for i in range(3):
            if self.record_types[i]:
                print(f"i:{i} export")
                record_items[i] = DB.get_item_by_date(self.record_date, i)

        # 写入文件，保存到文件夹
        file_names = [self.record_date.strftime("%Y"), self.record_date.strftime("%Y%m"),
                            self.record_date.strftime("%Y%m%d")]

        # 不同range全部存进对应位置
        for i in range(3):
            if self.record_types[i]:
                format_save(record_items[i], f_path, file_names[i])
                print(f"保存路径 {i} : {file_names[i]}")
