from typing import Optional
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import  QFrame, QWidget

class BackgroundFrame(QFrame):
    def __init__(self, pixmap: QPixmap, parent: Optional[QWidget]=None):
        super().__init__(parent)
        self._pixmap: QPixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self._pixmap)
        super().paintEvent(event)

