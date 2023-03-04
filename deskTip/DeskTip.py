#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：deskTip 
@File    ：DeskTip.py
@Author  ：Aidan Lew
@Date    ：2022/10/1 14:58 
"""
import uuid

from PyQt5.QtCore import QDate, Qt, QPoint, QCoreApplication
from PyQt5.QtGui import QIcon, QMouseEvent, QCursor, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QGridLayout, QVBoxLayout, QHBoxLayout, QMenu, QAction
)

from dialogs.RecordDialog import RecordDialog
from entity.Item import Item
from entity.Recorder import Recorder
from widgets.ItemWidget import ItemWidget
from widgets.MyCalendar import MyCalendar
from widgets.MyFrame import MyFrame
from service.DayItem import DayItem
from dialogs.AddDialog import AddDialog


def create_id():
    uid = uuid.uuid1()
    return uid.hex


class DeskTip(QMainWindow):

    # 今日已完成

    def __init__(self):
        super(DeskTip, self).__init__()
        # 窗口位置
        self._tracking = False
        self._endPos = None
        self._startPos = None
        # 最外层
        self.layout_total = QVBoxLayout()
        self.layout_down = QGridLayout()
        self.layout_up = QHBoxLayout()
        # 内层四个象限
        self.layout_1 = MyFrame()
        self.layout_2 = MyFrame()
        self.layout_3 = MyFrame()
        self.layout_4 = MyFrame()
        # 形态转换
        self.shape2circle = QPushButton("🎈")

        # 日历
        self.calendar = MyCalendar()
        # 同步按钮
        self.sync_btn = QPushButton("修改后同步")
        # 导出按钮
        self.export_btn = QPushButton("导出记录")
        # 初次加载今日数据
        self.now = QDate.currentDate()
        # 记录当日数据
        self.day_item = None
        # 记录增加数据
        self.new_name = None
        self.new_link = None
        # 右键菜单
        self.action_down = QAction("置于底层")
        self.action_top = QAction("置于顶层")
        self.action_free = QAction("置于自由")
        self.action_frame = QAction("调整大小/显示边框")
        self.action_no_frame = QAction("隐藏边框")
        self.action_exit = QAction("退出")

        # 调整不透明度
        self.menu_transparent = QMenu("调整不透明度")
        self.trans_100 = QAction("100%")
        self.trans_90 = QAction("90%")
        self.trans_80 = QAction("80%")
        self.trans_70 = QAction("70%")
        self.trans_60 = QAction("60%")
        self.trans_50 = QAction("50%")

        # 右键调整后的大小
        self.fixSize = None
        self.menu_box = QMenu(self)
        # 画
        self.setup_ui()
        # 记录今日（若此处赋值则无法得到最新的）
        # self.today_finish = None

    """
        初始化数据
    """

    def setup_ui(self):
        # 窗口设置
        self.setWindowTitle("FourAxis")
        self.setWindowIcon(QIcon("icons/4.ico"))
        # 窗体透明度
        self.setStyleSheet("background-color:rgb(255,255,255);"
                           "border:2px groove gray;"
                           "border-radius:10px;"
                           "padding:2px 4px;")
        self.setWindowOpacity(0.8)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 窗口无边框(初始化)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 窗口位置
        desktop = QApplication.desktop()
        self.move(int(desktop.width() * 0.55), int(desktop.height() * 0.05))

        # 日历链接
        self.calendar.dateEdit.dateChanged.connect(self.load_the_day)
        # 同步链接
        self.sync_btn.clicked.connect(self.sync)
        # 导出链接
        self.export_btn.clicked.connect(self.export)
        # 日历、保存、导出加入布局
        self.layout_up.addWidget(self.calendar)
        self.layout_up.addWidget(self.sync_btn)
        self.layout_up.addWidget(self.export_btn)
        # 右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # 连接到菜单显示函数显示内容
        self.customContextMenuRequested.connect(self.create_menu)
        # layouts加入布局
        self.layout_down.addWidget(self.layout_1, 0, 0)
        self.layout_down.addWidget(self.layout_2, 0, 2)
        self.layout_down.addWidget(self.layout_3, 2, 0)
        self.layout_down.addWidget(self.layout_4, 2, 2)

        self.shape2circle.setStyleSheet("background-color:rgb(255,255,255);"
                                        "border:2px groove gray;"
                                        "border-radius:12px;"
                                        )
        self.shape2circle.setMinimumWidth(24)
        self.shape2circle.setMaximumWidth(24)
        self.shape2circle.setMinimumHeight(24)
        self.shape2circle.setMaximumHeight(24)

        self.layout_down.addWidget(self.shape2circle, 1, 1)
        self.layout_down.setSpacing(2)

        # 总布局
        self.layout_total.addLayout(self.layout_up)
        self.layout_total.addLayout(self.layout_down)
        # 初次加载今日数据
        self.load_the_day(QDate.currentDate())
        # 布局完成
        widget = QWidget()
        widget.setLayout(self.layout_total)
        self.setCentralWidget(widget)

    # 右键弹出的菜单
    def create_menu(self):
        self.menu_box.setStyleSheet("background-color:rgb(245,245,245);"
                                    "border:1px groove gray;"
                                    "border-radius:1px;"
                                    "padding:2px 4px;")

        self.action_exit.setShortcut("Ctrl+Z")
        self.action_exit.triggered.connect(QCoreApplication.quit)

        self.action_top.setShortcut("Ctrl+U")
        self.action_top.triggered.connect(self.top_it)

        self.action_down.setShortcut("Ctrl+B")
        self.action_down.triggered.connect(self.down_it)

        self.action_free.setShortcut("Ctrl+F")
        self.action_free.triggered.connect(self.free_it)

        self.action_frame.setShortcut("Ctrl+S")
        self.action_frame.triggered.connect(self.show_frame)

        self.action_no_frame.triggered.connect(self.hide_frame)

        self.trans_100.triggered.connect(lambda: self.change_transparent(1))
        self.trans_90.triggered.connect(lambda: self.change_transparent(0.9))
        self.trans_80.triggered.connect(lambda: self.change_transparent(0.8))
        self.trans_70.triggered.connect(lambda: self.change_transparent(0.7))
        self.trans_60.triggered.connect(lambda: self.change_transparent(0.6))
        self.trans_50.triggered.connect(lambda: self.change_transparent(0.5))

        self.menu_box.addAction(self.action_exit)
        self.menu_box.addAction(self.action_top)
        self.menu_box.addAction(self.action_down)
        self.menu_box.addAction(self.action_free)
        self.menu_box.addAction(self.action_frame)
        self.menu_box.addAction(self.action_no_frame)

        self.menu_transparent.addAction(self.trans_100)
        self.menu_transparent.addAction(self.trans_90)
        self.menu_transparent.addAction(self.trans_80)
        self.menu_transparent.addAction(self.trans_70)
        self.menu_transparent.addAction(self.trans_60)
        self.menu_transparent.addAction(self.trans_50)
        self.menu_box.addMenu(self.menu_transparent)

        # 鼠标位置弹出
        self.menu_box.popup(QCursor.pos())

    # 处理透明度改变
    def change_transparent(self, percent):
        self.setWindowOpacity(percent)
        self.show()

    # 重写resize事件
    def resizeEvent(self, e):
        self.fixSize = self.size()
        p1_x = self.layout_down.itemAtPosition(0, 0).geometry().x() + \
               self.layout_down.itemAtPosition(0, 0).geometry().width()
        p1_y = self.layout_down.itemAtPosition(0, 0).geometry().y() + \
               self.layout_down.itemAtPosition(0, 0).geometry().height()

        p2_x = self.layout_down.itemAtPosition(2, 2).geometry().x()
        p2_y = self.layout_down.itemAtPosition(2, 2).geometry().y()

        print("width", p2_x - p1_x)
        print("height", p2_y - p1_y)

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
        elif e.button() == Qt.RightButton:
            self.create_menu()

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

    # 实现置顶
    def top_it(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        if self.fixSize is not None:
            self.resize(self.fixSize)
        self.show()

    # 实现置底
    def down_it(self):
        self.setWindowFlags(Qt.WindowStaysOnBottomHint | Qt.FramelessWindowHint)
        if self.fixSize is not None:
            self.resize(self.fixSize)
        self.show()

    # 实现自由
    def free_it(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        if self.fixSize is not None:
            self.resize(self.fixSize)
        self.show()

    # 显示边框并调整大小
    def show_frame(self):
        self.setWindowFlags(Qt.Window)
        self.show()

    # 隐藏边框
    def hide_frame(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()

    """
        加载指定日数据（粗暴）
    """

    def load_the_day(self, date):

        self.now = date
        layouts = [self.layout_1, self.layout_2, self.layout_3, self.layout_4]

        # 删除所有原来的控件,避免内存问题
        for i in range(0, 4):
            for j in reversed(range(layouts[i].layout().count())):
                widgetToRemove = layouts[i].layout().itemAt(j).widget()
                # remove it from the layout list
                layouts[i].layout().removeWidget(widgetToRemove)
                # remove it from the gui
                widgetToRemove.setParent(None)

        if self.day_item is None:
            print("load day")
            self.day_item = DayItem(date)
        else:
            self.day_item.get_items(date)

        # 直接修改数据库不会在这更新,对于数据库单向同步（数据库向本代码靠拢）
        cnt = 0
        finish = 0
        for item in self.day_item.items:
            cnt += 1
            # 统计完成情况
            if item.state:
                finish += 1
            item_widget = ItemWidget(item.item_id, item.item_type, item.state, item.item_name, item.link)
            item_widget.item_del.clicked.connect(self.delete_handle)
            layouts[item.item_type].addWidget(item_widget)

        if finish != 0:
            self.today_finish = "" + str(finish / cnt * 100)[0:4] + "%"
            print("finish:", finish)
            print("cnt:", cnt)
            print(self.today_finish)
        else:
            self.today_finish = "0%"
            print("finish:", finish)
            print("cnt:", cnt)
            print(self.today_finish)

        for i in range(0, 4):
            btn = QPushButton("+")
            btn.setObjectName(f"{i}")

            if i == 0:
                btn.setStyleSheet("background-color: rgb(0,191,255);"
                                  "border-style: outset;border-width: 2px;"
                                  "border-radius: 10px;"
                                  "border-color: gray;"
                                  "font: bold 14px;"
                                  "min-width: 10em;"
                                  "padding: 6px;")
            elif i == 1:
                btn.setStyleSheet("background-color: rgb(135,206,250);"
                                  "border-style: outset;border-width: 2px;"
                                  "border-radius: 10px;"
                                  "border-color: gray;"
                                  "font: bold 14px;"
                                  "min-width: 10em;"
                                  "padding: 6px;")
            elif i == 2:
                btn.setStyleSheet("background-color: rgb(255,165,0);"
                                  "border-style: outset;border-width: 2px;"
                                  "border-radius: 10px;"
                                  "border-color: gray;"
                                  "font: bold 14px;"
                                  "min-width: 10em;"
                                  "padding: 6px;")
            elif i == 3:
                btn.setStyleSheet("background-color: rgb(255,248,220);"
                                  "border-style: outset;border-width: 2px;"
                                  "border-radius: 10px;"
                                  "border-color: gray;"
                                  "font: bold 14px;"
                                  "min-width: 10em;"
                                  "padding: 6px;")

            btn.clicked.connect(self.add_item)
            layouts[i].addWidget(btn)

    """
        删除item触发
    """

    def delete_handle(self):
        item_id = self.sender().objectName()
        print(f"delete-{item_id}")
        self.day_item.delete_item(item_id)
        # 重新加载
        self.load_the_day(self.now)

    """
        添加新的item触发dialog
    """

    def add_item(self):
        button = self.sender()
        print(button.objectName())
        dlg = AddDialog(self)
        res = dlg.exec()
        print("res:", res)
        if res:
            print("Success!")
            new_item = Item(create_id(), self.day_item.date, dlg.name_s,
                            int(button.objectName()), 0, dlg.link_s)
            self.day_item.add_item(new_item)
            # 重新加载
            self.load_the_day(self.now)
        else:
            print("Cancel!")

    """
        导出数据
    """

    def export(self):
        dlg = RecordDialog(self)
        res = dlg.exec()
        if res:
            chosen_date, chosen_types = dlg.date, dlg.chosen
            print(f"chosen_date:{chosen_date}")
            print(f"chosen_types:{chosen_types}")
            # Recorder干活
            rd = Recorder(chosen_date, chosen_types)
            rd.export_records()
            print("Success!")

        else:
            print("Cancel!")

    """ 
        同步数据库（每次修改状态或者事项名之后）
        待优化TODO
    """

    def sync(self):

        new_items = []
        layouts = [self.layout_1, self.layout_2, self.layout_3, self.layout_4]
        cnt = 0
        finish = 0
        for layout_ in layouts:
            for i in range(layout_.layout().count()):
                item_widget = layout_.layout().itemAt(i).widget()
                # 计数
                if isinstance(item_widget, ItemWidget):
                    cnt += 1
                    print(f"item_widget.state{item_widget.state}")
                    if item_widget.state:
                        finish += 1

                # 仅仅考虑修改过的
                if isinstance(item_widget, ItemWidget) and item_widget.isChanged:
                    new_item = Item(item_widget.item_id, self.now.toPyDate(), item_widget.item_name,
                                    item_widget.item_type, item_widget.state, item_widget.link)
                    new_items.append(new_item)
                    print("1", str(new_item))
        res = self.day_item.edit_item(new_items)

        if finish != 0:
            self.today_finish = "" + str(finish / cnt * 100)[0:4] + "%"
            print("finish:", finish)
            print("cnt:", cnt)
            print(self.today_finish)
        else:
            print("finish:", finish)
            print("cnt:", cnt)
            self.today_finish = "0%"
            print(self.today_finish)

        if res:
            print("finish sync")
        else:
            print("error")
