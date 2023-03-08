from collections.abc import Iterator
from typing import List, Optional

from PyQt5.QtCore import  QSize, QThreadPool, Qt
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QIcon, QPixmap
from provider_parsers import Film
from hayai.concurrency import Worker, worker

class QFilmListModel(QAbstractListModel):
    numberPopulated = pyqtSignal(int)

    def __init__(self,filmGenerator:Optional[Iterator[Film]] = None,batch: int = 3,maxFilms: int = -1, parent=None,):
        super().__init__(parent)

        self.filmGenerator: Optional[Iterator[Film]] = filmGenerator
        self.batch: int = max(1,batch)
        self.batch = min(self.batch,10)
        self.maxFilms: int = maxFilms
        self.iconSize:QSize = QSize(150,int(150 * 1.5))
        #self.films: List[Film] = [Film("This is for testing only","link",True,"link")]
        #self.films += [Film("This is for testing only","link",True,"link")]
        self.films: List[Film] = []
        self.noMoreData: bool = False
        self.threadPool: QThreadPool = QThreadPool()
        self.threadPool.setMaxThreadCount(1)

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
            #pixmap = pixmap.scaledToWidth(100)
            #pixmap = pixmap.scaled(self.iconSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            return QIcon(pixmap)
            #return pixmap


        return None

    def canFetchMore(self, index) -> bool:
        if self.filmGenerator == None:
            return False
        if self.maxFilms >= 0  and self.maxFilms  == len(self.films):
            return False

        if self.noMoreData:
            return False
        return True

    def fetchMore(self, index):
        if self.filmGenerator == None:
            return
        itemsToFetch: int = self.batch 
        if self.maxFilms >=0:
            itemsToFetch = min(itemsToFetch,self.maxFilms - len(self.films))
        worker: Worker = Worker(self.__fetchFilms,itemsToFetch)
        self.destroyed.connect(worker.exit)
        self.threadPool.start(worker)

    def __fetchFilms(self,maxFilms: int,progress_callback = None):
        if self.noMoreData or self.filmGenerator is None:
            return
        buffer: List[Film] = []
        for a in range(maxFilms):
            try:
                buffer.append(next(self.filmGenerator))
            except StopIteration:
                self.noMoreData = True
                break
        if buffer:
            startRow: int = len(self.films)
            endRow: int = startRow + len(buffer) -1
            self.beginInsertRows(QModelIndex(), startRow,endRow)
            self.films += buffer
            self.endInsertRows()

    def setFilmGenerator(self, filmGenerator: Optional[Iterator[Film]]) -> None:
        self.filmGenerator = filmGenerator
        self.beginResetModel()
        self.films.clear()
        self.noMoreData = False
        self.endResetModel()
    def deleteLator(self):
        self.threadPool.clear()

