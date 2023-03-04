#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：deskTip 
@File    ：AddDialog.py
@Author  ：Aidan Lew
@Date    ：2022/10/3 21:38 
"""

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QPushButton)


class AddDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("编辑待办事项")

        self.buttonBox = QHBoxLayout()
        button_1 = QPushButton("确定")
        button_1.clicked.connect(self.get_info)
        button_1.clicked.connect(self.accept)
        button_2 = QPushButton("取消")
        button_2.clicked.connect(self.reject)
        self.buttonBox.addWidget(button_1)
        self.buttonBox.addWidget(button_2)

        self.layout = QVBoxLayout()
        message = QLabel("请填写待办事项:")
        name_layout = QHBoxLayout()
        name = QLabel("事项(请简略):")
        self.name_info = QLineEdit()
        self.name_info.setObjectName("item_name")
        name_layout.addWidget(name)
        name_layout.addWidget(self.name_info)
        link_layout = QHBoxLayout()
        link = QLabel("超链接(可无):")
        self.link_info = QLineEdit()
        self.link_info.setObjectName("link")
        link_layout.addWidget(link)
        link_layout.addWidget(self.link_info)

        self.layout.addWidget(message)
        self.layout.addLayout(name_layout)
        self.layout.addLayout(link_layout)
        self.layout.addLayout(self.buttonBox)
        self.setLayout(self.layout)

        self.name_s = None
        self.link_s = None

    # 只能在按钮时捕获,不然主窗口获取不到
    def get_info(self):
        self.name_s = self.name_info.text()
        if "http" in self.link_info.text() or "https" in self.link_info.text():
            self.link_s = self.link_info.text()
        else:
            self.link_s = self.link_info.text().replace("\\", "\\\\")
