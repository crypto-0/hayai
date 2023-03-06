from collections.abc import Iterator
from itertools import islice
from typing import List, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QIcon, QPixmap
from provider_parsers import Film

class QFilmListModel(QAbstractListModel):
    numberPopulated = pyqtSignal(int)

    def __init__(self,filmGenerator:Optional[Iterator[Film]] = None,batch: int = 5,maxFilms: int = -1, parent=None,):
        super().__init__(parent)

        self.filmGenerator: Optional[Iterator[Film]] = filmGenerator
        self.batch: int = max(1,batch)
        self.batch = min(self.batch,10)
        self.maxFilms: int = maxFilms
        self.films: List[Film] = []
        self.buffer: List[Film] = []

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.films)

    def data(self, index, role=Qt.DisplayRole) -> object: #pyright: ignore
        if not index.isValid():
            return None

        if index.row() >= len(self.films) or index.row() < 0:
            return None

        if role == Qt.DisplayRole: #pyright: ignore
            return self.films[index.row()].title

        if role == Qt.DecorationRole: #pyright: ignore
            #pixmap: QPixmap = QPixmap("hayai/assets/imgs/jujutsu.jpg")
            pixmap: QPixmap = QPixmap("hayai/assets/imgs/creed3.jpg")
            #pixmap: QPixmap = QPixmap("hayai/assets/imgs/road-back-home.png")
            #pixmap: QPixmap = QPixmap()
            pixmap = pixmap.scaledToWidth(150)
            return pixmap


        return None

    def canFetchMore(self, index) -> bool:
        if self.filmGenerator == None:
            return False
        if self.maxFilms >= 0  and self.maxFilms  == len(self.films):
            return False

        if self.buffer:
            return True
        try:

            self.buffer = [next(self.filmGenerator)]
            return True
        except StopIteration:
            return False


    def fetchMore(self, index):
        if self.filmGenerator == None:
            return
        itemsToFetch: int = self.batch -1
        if self.maxFilms >=0:
            itemsToFetch = min(itemsToFetch,self.maxFilms - len(self.films))
        self.buffer += islice(self.filmGenerator,itemsToFetch)
        startRow: int = len(self.films)
        endRow: int = startRow + len(self.buffer) -1
        self.beginInsertRows(QModelIndex(), startRow,endRow)
        self.films += self.buffer
        self.buffer.clear()
        self.endInsertRows()

    def setFilmGenerator(self, filmGenerator: Optional[Iterator[Film]]) -> None:
        self.filmGenerator = filmGenerator
        self.beginResetModel()
        self.films.clear()
        self.buffer.clear()
        self.endResetModel()

