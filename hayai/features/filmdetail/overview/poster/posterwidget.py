from typing import Optional
from PyQt5.QtCore import QEvent, QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSizePolicy, QWidget

class QPoster(QLabel):

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        #self.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Ignored)
        self.setFixedSize(150,int(150 * 1.5))

    def setPixmap(self, pixmap: QPixmap) -> None:
        pixmap = pixmap.scaledToWidth(self.width())
        return super().setPixmap(pixmap)

