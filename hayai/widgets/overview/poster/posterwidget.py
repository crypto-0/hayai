from typing import Optional
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel,  QWidget

class QPoster(QLabel):

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        self.setFixedSize(150,int(150 * 1.5))

    def setPixmap(self, pixmap: QPixmap) -> None:
        pixmap = pixmap.scaledToWidth(self.width())
        return super().setPixmap(pixmap)

