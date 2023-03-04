#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：deskTip 
@File    ：MyCalendar.py
@Author  ：Aidan Lew
@Date    ：2022/10/3 16:41
@Reference : https://blog.csdn.net/huayunhualuo/article/details/101036370
"""
import datetime
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDateTimeEdit


class MyCalendar(QWidget):
    def __init__(self):
        super().__init__()
        # 默认设置为今天
        self.dateEdit = QDateTimeEdit(datetime.date.today())
        # self.btn = QPushButton("获得日期和时间")
        # 设置显示的格式
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        # 设置最小日期
        self.dateEdit.setMinimumDate(QDate.currentDate().addDays(-365))
        # 设置最大日期
        self.dateEdit.setMaximumDate(QDate.currentDate().addDays(365))
        # 单击下拉箭头就会弹出日历控件，不在范围内的日期是无法选择的
        self.dateEdit.setCalendarPopup(True)

        layout = QVBoxLayout()
        layout.addWidget(self.dateEdit)
        self.setLayout(layout)

    def onButtonClick(self):
        # 最大日期
        maxDate = self.dateEdit.maximumDate()
        # 最小日期
        minDate = self.dateEdit.minimumDate()

        print("\n 选择日期时间")
        print("minDate=%s" % str(minDate))
        print("maxDate=%s" % str(maxDate))
