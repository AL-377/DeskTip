#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：deskTip 
@File    ：MyFrame.py
@Author  ：Aidan Lew
@Date    ：2022/10/3 16:22 
"""

from PyQt5.QtWidgets import (
    QVBoxLayout,
    QFrame
)


class MyFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setLayout(QVBoxLayout())


    def addWidget(self, widget):
        self.layout().addWidget(widget)


