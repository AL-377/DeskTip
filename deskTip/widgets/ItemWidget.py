#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：deskTip 
@File    ：ItemWidget.py
@Author  ：Aidan Lew
@Date    ：2022/10/3 16:21 
"""
import os
import webbrowser
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QRadioButton,
    QLineEdit
)


class ItemWidget(QWidget):
    def __init__(self, item_id, item_type, item_finish, name, link_target):
        super().__init__()
        self.layout = QHBoxLayout()
        # 虽然不显示id，但是在更新的时候用到
        self.item_id = item_id
        self.item_type = item_type
        # 初始化
        self.state = item_finish
        self.item_name = None
        # 监控是否需要被更新
        self.isChanged = False
        self.link = link_target

        self.edit_state = QRadioButton()
        self.edit_state.setChecked(item_finish)
        self.edit_state.toggled.connect(self.toggle_handle)

        self.edit_name = QLineEdit(name)
        self.edit_name.textChanged.connect(self.edit_handle)
        self.item_link = QPushButton("📂")
        self.item_link.clicked.connect(self.link_handle)

        self.item_del = QPushButton("🚮")
        self.item_del.setObjectName(self.item_id)
        # 主窗口内绑定删除键
        # self.item_del.clicked.connect(self.delete_handle)

        self.link_target = link_target
        self.layout.addWidget(self.edit_state)
        self.layout.addWidget(self.edit_name)
        self.layout.addWidget(self.item_link)
        self.layout.addWidget(self.item_del)

        self.setLayout(self.layout)

    def toggle_handle(self):
        self.item_name = self.edit_name.text()
        self.state = int(self.edit_state.isChecked())
        self.isChanged = True

    def edit_handle(self):
        self.item_name = self.edit_name.text()
        self.state = int(self.edit_state.isChecked())
        self.isChanged = True

    def link_handle(self):
        if len(str(self.link_target)) == 0:
            pass
        elif "http" in str(self.link_target) or "https" in str(self.link_target):
            webbrowser.open_new_tab(str(self.link_target))
        else:
            print("explorer.exe /n," + str(self.link_target))
            os.system("explorer.exe /n," + str(self.link_target))
