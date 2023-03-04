#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：deskTip 
@File    ：RecordDialog.py
@Author  ：Aidan Lew
@Date    ：2022/10/4 13:44 
"""

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDate

from widgets.MyCalendar import MyCalendar
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QCheckBox)


class RecordDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("导出记录")

        self.buttonBox = QHBoxLayout()
        button_1 = QPushButton("确定")
        button_1.clicked.connect(self.accept)
        button_2 = QPushButton("取消")
        button_2.clicked.connect(self.reject)
        self.buttonBox.addWidget(button_1)
        self.buttonBox.addWidget(button_2)

        self.layout = QVBoxLayout()

        self.calendar = MyCalendar()
        self.calendar.dateEdit.dateChanged.connect(self.choose_the_date)

        year = QCheckBox("当年记录")
        year.setCheckState(Qt.Unchecked)
        year.setObjectName("0")
        year.stateChanged.connect(self.choose_the_type)

        month = QCheckBox("当月记录")
        month.setCheckState(Qt.Unchecked)
        month.setObjectName("1")
        month.stateChanged.connect(self.choose_the_type)

        day = QCheckBox("当日记录")
        day.setCheckState(Qt.Unchecked)
        day.setObjectName("2")
        day.stateChanged.connect(self.choose_the_type)

        self.layout.addWidget(self.calendar)
        self.layout.addWidget(year)
        self.layout.addWidget(month)
        self.layout.addWidget(day)

        self.layout.addLayout(self.buttonBox)
        self.setLayout(self.layout)
        # 传递给主窗口的信息,日期、导出类型
        self.date = QDate.currentDate().toPyDate()
        self.chosen = [0,0,0]

    def choose_the_date(self, date):
        self.date = date.toPyDate()

    def choose_the_type(self, s):
        print(s)
        check_box = self.sender()
        choose_type = int(check_box.objectName())
        if s:
            self.chosen[choose_type] = 1
        else:
            self.chosen[choose_type] = 0
        print("type:",choose_type)
