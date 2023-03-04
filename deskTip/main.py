#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：deskTip 
@File    ：main.py
@Author  ：Aidan Lew
@Date    ：2022/10/7 15:10 
"""
import sys

from PyQt5.QtWidgets import QApplication

from DeskTip import DeskTip
from CircleTip import CircleTip


if __name__ == '__main__':
    app = QApplication(sys.argv)
    deskTip = DeskTip()
    circle = CircleTip()

    # 绑定窗口
    deskTip.shape2circle.clicked.connect(lambda:circle.show_percent(deskTip.today_finish))
    deskTip.shape2circle.clicked.connect(lambda:circle.move(int(deskTip.pos().x()+deskTip.geometry().width()/2),
                                                            int(deskTip.pos().y()+deskTip.geometry().height()/2)))
    deskTip.shape2circle.clicked.connect(deskTip.hide)

    circle.action_unfold.triggered.connect(deskTip.show)
    circle.action_unfold.triggered.connect(circle.hide)

    deskTip.show()
    app.exec()
