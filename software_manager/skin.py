# -*- coding: utf-8 -*-
"""
module author: Long Hao <hoolongvfx@gmail.com>
"""
import glob
import os
import sys

import openmetadata as om
from Qt import QtCore, QtGui, QtWidgets
from hz.awesome_ui.widgets import RenderAwesomeUI
from hz.resources import HZResources

SKIN_INDEX = 2
SKIN_WIDTH = 340 / SKIN_INDEX
SKIN_HEIGHT = 640 / SKIN_INDEX


class CustomListWidget(QtWidgets.QListWidget):
    def __init__(self, parent):
        super(CustomListWidget, self).__init__()
        RenderAwesomeUI(parent_widget=self)
        self.parent = parent
        self.software_gui = self.parent.parent

        self.setDragEnabled(False)
        icon_size_x = SKIN_WIDTH
        icon_size_y = SKIN_HEIGHT
        grid_size_x = icon_size_x + 5
        grid_size_y = icon_size_y + 5
        self.setBatchSize(grid_size_x)
        self.setIconSize(QtCore.QSize(icon_size_x, icon_size_y))
        self.setGridSize(QtCore.QSize(grid_size_x, grid_size_y))
        self.setAutoScroll(True)
        self.setAutoScrollMargin(5)

        self.setFrameShape(QtWidgets.QFrame().NoFrame)
        self.setResizeMode(QtWidgets.QListView().Adjust)
        self.setViewMode(QtWidgets.QListView().ViewMode.IconMode)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.clicked.connect(self.change_skin)

        for skin in self.get_skins():
            layer_item = ThumbWidgetItem(skin)
            layer_item.path = skin.decode("gbk")
            self.addItem(layer_item)
        self.setStyleSheet("QListWidget {border-radius: 15px}")

    def change_skin(self):
        item = self.currentItem()
        if item:
            skin_path = item.path.replace("\\", '/')
            om.write(self.software_gui.local_profile_folder,
                     'skin', skin_path)
            self.software_gui.set_background_image_css(skin_path)

    def get_skins(self):
        all_files = []
        all_files.extend(
            glob.glob("%s/skin/*.png" % HZResources.resources_root))
        all_files.extend(
            glob.glob(
                "%s/skin/*.png" % self.software_gui.local_profile_folder))
        return all_files


class ThumbWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, skin_path):
        RenderAwesomeUI(parent_widget=self)
        self.skin_path = skin_path.replace("\\", '/').decode("gbk")
        self.name = os.path.basename(self.skin_path).split(".")[0]
        super(ThumbWidgetItem, self).__init__()
        self.draw_icon()
        self.setToolTip(self.name)

    def draw_icon(self):
        image = QtGui.QImage(self.skin_path)
        image = QtGui.QPixmap().fromImage(image)
        y = image.size().height()
        bottom = y - 10
        painter = QtGui.QPainter(image)
        painter.setPen(QtGui.QColor(0, 0, 0, 255))
        font = QtGui.QFont("OpenSans-Bold")
        font.setPointSize(20)
        painter.setFont(font)
        name = self.name
        center_name = 60 - ((len(name) * font.pixelSize()) / 2)
        painter.setPen(QtGui.QColor(255, 255, 255, 255))
        painter.drawText(center_name - 2, bottom - 18, name)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
        painter.end()
        self.setIcon(image)


class SoftwareManagerSkinUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SoftwareManagerSkinUI, self).__init__()
        self.parent = parent
        RenderAwesomeUI(parent_widget=self)
        hbox_layout = QtWidgets.QHBoxLayout()
        skin_list_widget = CustomListWidget(self)
        self.setMinimumSize(SKIN_WIDTH * 5 - 100, SKIN_HEIGHT * 2 + 20)
        hbox_layout.addWidget(skin_list_widget)
        self.setLayout(hbox_layout)
        self.setWindowTitle("Skin Store")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    c = SoftwareManagerSkinUI()
    c.show()
    app.exec_()
