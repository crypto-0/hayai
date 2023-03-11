from typing import Optional
from PyQt5.QtCore import pyqtProperty #pyright: ignore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtWidgets import QWidget
from provider_parsers import FilmInfo
from hayai.widgets import QBanner


class QFilmDeatail(QFrame):

    def __init__(self , filmInfo: FilmInfo, parent: Optional[QWidget] = None)  -> None:
        super().__init__(parent)

        self._filmInfo = filmInfo

        banner: QBanner = QBanner(filmInfo.title,"test",filmInfo.description,QPixmap())

        filmDetailLayout: QVBoxLayout = QVBoxLayout()
        filmDetailLayout.addWidget(banner)
        self.setLayout(filmDetailLayout)

    @pyqtProperty(FilmInfo)
    def filmInfo(self): #pyright: ignore
        return self._filmInfo

    @filmInfo.setter
    def filmInfo(self, filmInfo: FilmInfo):
        self._filmInfo = filmInfo

