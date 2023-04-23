from typing import Optional
from PyQt6.QtGui import QColor, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import QPushButton, QWidget

class QNavButton(QPushButton):
    def __init__(self, title: str = "",iconPath: str = "",parent: Optional[QWidget] = None):
        super().__init__(title.capitalize(),parent=parent)
        pixmap: QPixmap = QPixmap(iconPath)
        self.defaultIcon: QIcon = QIcon(pixmap)
        self.hoverIcon: QIcon = QIcon(self.createColoredPixmap(pixmap))
        icon: QIcon = QIcon(self.defaultIcon)

        self.setIcon(icon)
        self.setCheckable(True)
        self.setFlat(True)
        self.setObjectName("QNavButton")

    def enterEvent(self, e):
        self.setIcon(self.hoverIcon)
        super().enterEvent(e)

    def leaveEvent(self, e) -> None:
        self.setIcon(self.defaultIcon)
        super().leaveEvent(e)

    def onToggled(self):
        if self.isChecked():
            self.setIcon(self.hoverIcon)
        else:
            self.setIcon(self.defaultIcon)
            
    def createColoredPixmap(self,pixmap: QPixmap):
        pixmap = pixmap.copy()
        color = QColor("white")
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()

        return pixmap

