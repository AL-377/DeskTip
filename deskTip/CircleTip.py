#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：deskTip 
@File    ：CircleTip.py
@Author  ：Aidan Lew
@Date    ：2022/10/7 10:36 
"""
import sys

from PyQt5.QtGui import QMouseEvent, QCursor
from PyQt5.QtWidgets import QPushButton, QAction, QMenu
from PyQt5.QtCore import Qt, QPoint, QCoreApplication


class CircleTip(QPushButton):
    def __init__(self):
        super().__init__()

        # 窗口位置
        self._tracking = False
        self._endPos = None
        self._startPos = None
        self.setObjectName("Circle_button")
        self.setStyleSheet("background-color:rgb(135,206,250);"
                           "border:1px groove gray;"
                           "border-radius:24px;"
                           )
        # 窗口大小
        self.setMinimumWidth(48)
        self.setMaximumWidth(48)
        self.setMinimumHeight(48)
        self.setMaximumHeight(48)
        # 窗口类型
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.7)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 右键菜单
        self.action_unfold = QAction("展开")
        self.action_exit = QAction("退出")
        self.menu_box = QMenu(self)
        self.setup_ui()

    def show_percent(self,today_finish):
        self.setText(today_finish)
        print(today_finish)
        self.show()

    def setup_ui(self):

        # 右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # 连接到菜单显示函数显示内容
        self.customContextMenuRequested.connect(self.create_menu)

    # 右键弹出的菜单
    def create_menu(self):
        self.menu_box.setStyleSheet("background-color:rgb(245,245,245);"
                                    "border:1px groove gray;"
                                    "border-radius:1px;"
                                    "padding:2px 4px;")

        self.action_exit.setShortcut("Ctrl+Z")
        self.action_exit.triggered.connect(QCoreApplication.quit)

        self.action_unfold.setShortcut("Ctrl+S")
        # 主窗口定义
        # self.action_unfold.triggered.connect(self.unfold)

        self.menu_box.addAction(self.action_exit)
        self.menu_box.addAction(self.action_unfold)

        # 鼠标位置弹出
        self.menu_box.popup(QCursor.pos())

    # 重写移动事件
    def mouseMoveEvent(self, e: QMouseEvent):
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True
            print("now at:", e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None
