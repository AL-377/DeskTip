#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：adminInfo 
@File    ：InfoDialog.py
@Author  ：Aidan Lew
@Date    ：2022/10/5 15:29 
"""
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QPushButton, QApplication, QMessageBox)

info_path = "usr/info.txt"


# 最简单的加密方式
def encoder(codes):
    before = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
              'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
              'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '.']
    after = ['s', 'd', 'C', 'l', 'U', '3', '4', 'r', 'N', '0', 'p', 'T', 'u', 'G', 'Y', 'D', 'q', 'a', 'S', 'O', 'M',
             '7', 'i', 'g', 'z', 'L', 'v', 'I', 'X', 'c', 'A', 'Q', 'P', 'B', 'h', '6', 'w', 'f', 'e', 'R', 'J', '2',
             'x', '5', 'E', 'o', '1', 'H', '9', '8', 'm', 'k', 'Z', 'W', 'b', 'F', 't', 'n', 'j', 'V', 'y', 'K', '.']
    dicts = {}
    for i in range(len(after)):
        dicts[before[i]] = after[i]

    res = ""
    for code in codes.strip():
        if dicts.__contains__(code):
            res += dicts[code]
        else:
            res += code
    return res


class InfoDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("录入Mysql信息")
        self.setWindowIcon(QIcon("icons/2.ico"))
        self.setFixedSize(300, 200)

        self.buttonBox = QHBoxLayout()
        button_1 = QPushButton("确定")
        button_1.clicked.connect(self.get_info)
        button_1.clicked.connect(self.accept)
        button_2 = QPushButton("取消")
        button_2.clicked.connect(self.reject)
        self.buttonBox.addWidget(button_1)
        self.buttonBox.addWidget(button_2)

        self.layout = QVBoxLayout()

        message = QLabel("您的隐私受法律保护,请放心填写sql账户信息")

        ip_layout = QHBoxLayout()
        ip = QLabel("主机IP:      ")
        self.ip_info = QLineEdit()
        ip_layout.addWidget(ip)
        ip_layout.addWidget(self.ip_info)

        user_layout = QHBoxLayout()
        user = QLabel("Mysql用户名: ")
        self.user_info = QLineEdit()
        user_layout.addWidget(user)
        user_layout.addWidget(self.user_info)

        code_layout = QHBoxLayout()
        code = QLabel("Mysql密码:   ")
        self.code_info = QLineEdit()
        self.code_info.setEchoMode(QLineEdit.Password)
        code_layout.addWidget(code)
        code_layout.addWidget(self.code_info)

        db_layout = QHBoxLayout()
        db = QLabel("新建数据库名:")
        self.db_info = QLineEdit()
        db_layout.addWidget(db)
        db_layout.addWidget(self.db_info)

        self.layout.addWidget(message)
        self.layout.addLayout(ip_layout)
        self.layout.addLayout(user_layout)
        self.layout.addLayout(code_layout)
        self.layout.addLayout(db_layout)

        self.layout.addLayout(self.buttonBox)
        self.setLayout(self.layout)

    # 只能在按钮时捕获,不然主窗口获取不到
    def get_info(self):
        ip = encoder(self.ip_info.text())
        user = encoder(self.user_info.text())
        code = encoder(self.code_info.text())
        db = encoder(self.db_info.text())
        with open(info_path, "w") as f:
            f.write(ip + "\n")
            f.write(user + "\n")
            f.write(code + "\n")
            f.write(db + "\n")
            f.flush()
            f.close()

        dlg = QMessageBox(self)
        dlg.setWindowTitle("安装完成")
        dlg.setText("当您需要修改数据库信息时，点击文件夹下‘adminInfo.exe’\n"
                    "现在可以双击deskTip.exe打开程序，开启你的冒险之旅吧")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Information)
        button = dlg.exec()

        if button == QMessageBox.Yes:
            print("Yes!")
        else:
            print("No!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InfoDialog()
    window.show()
    app.exec()
