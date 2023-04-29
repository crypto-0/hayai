from typing import Optional
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel,  QWidget
from PyQt6.QtCore import pyqtProperty #pyright: ignore

class QFilmPoster(QLabel):

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        self.setFixedSize(150,int(150 * 1.5))

    @pyqtProperty(QPixmap)
    def posterPixmap(self) -> QPixmap: #pyright: ignore
        return super().pixmap()

    @posterPixmap.setter
    def posterPixmap(self, pixmap: QPixmap) -> None:
        pixmap = pixmap.scaledToWidth(self.width())
        return super().setPixmap(pixmap)

