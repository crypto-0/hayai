from typing import Optional
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor, QIcon, QPainter, QPixmap
from PyQt5.QtWidgets import QPushButton, QWidget

class QNavButton(QPushButton):
    def __init__(self, icon_path,title: str = "",parent: Optional[QWidget] = None):
        super().__init__(title,parent=parent)
        defaultPixmap: QPixmap = QPixmap(icon_path)
        selectedPixmap: QPixmap = self.createColoredPixmap(defaultPixmap)
        icon: QIcon = QIcon()
        icon.addPixmap(defaultPixmap,QIcon.Mode.Normal)
        icon.addPixmap(selectedPixmap,QIcon.Mode.Active)

        self.setIcon(icon)
        self.setCheckable(True)
        self.setFlat(True)
        self.setObjectName("QNavButton")
        
    def createColoredPixmap(self,pixmap: QPixmap):
        pixmap = pixmap.copy()
        color = QColor("red")
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()

        return pixmap

