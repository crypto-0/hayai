from cachetools import TTLCache
from collections.abc import Iterator
from typing import List, Optional
from concurrent.futures import Future, ThreadPoolExecutor
from PyQt5.QtCore import  QSize, QThreadPool, Qt
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QIcon, QPixmap 
from provider_parsers import Film
from hayai.concurrency import Worker
import requests

class QFilmListModel(QAbstractListModel):
    session = requests.session()
    cache = TTLCache(maxsize=100,ttl=180)

    def __init__(self,filmGenerator:Optional[Iterator[Film]] = None,batch: int = 10,maxFilms: int = -1, parent=None,):
        super().__init__(parent)

        self.filmGenerator: Optional[Iterator[Film]] = filmGenerator
        self.batch: int = max(1,batch)
        self.maxFilms: int = maxFilms
        self.iconSize:QSize = QSize(150,int(150 * 1.5))
        self.films: List[Film] = [Film("This is for testing only","link",True,"link",extra="2018 . 101min. movie") for x in range(20)]
        [setattr(film, 'poster_icon',QIcon("hayai/assets/imgs/creed3.jpg")
 ) for film in self.films]
        #self.films += [Film("This is for testing only","link",True,"link")]
        #self.films: List[Film] = []
        self.noMoreData: bool = False
        self.threadPool: QThreadPool = QThreadPool()
        self.threadPool.setMaxThreadCount(1)

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.films)

    def setData(self, index, value, role=Qt.EditRole) -> bool: #pyright: ignore
        if value is None:
            return False
        if role == Qt.DecorationRole: #pyright: ignore
            setattr(self.films[index.row()], 'poster_icon', value)
            self.films[index.row()].poster_data = None
            self.dataChanged.emit(index, index, [role])
            return True

        return False

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if parent.isValid() or row < 0 or row >= len(self.films):
            return QModelIndex()
        return self.createIndex(row, column)

    def data(self, index, role=Qt.DisplayRole) -> object: #pyright: ignore
        if not index.isValid():
            return None

        if index.row() >= len(self.films) or index.row() < 0:
            return None

        if role == Qt.UserRole: #pyright: ignore
            return self.films[index.row()].extra

        if role == Qt.DisplayRole: #pyright: ignore
            return self.films[index.row()].title

        if role == Qt.DecorationRole: #pyright: ignore
            #pixmap: QPixmap = QPixmap("hayai/assets/imgs/jujutsu.jpg")
            if hasattr(self.films[index.row()],"poster_icon"):
                return self.films[index.row()].poster_icon #pyright: ignore
            #pixmap: QPixmap = QPixmap("hayai/assets/imgs/creed3.jpg")
            #pixmap: QPixmap = QPixmap("hayai/assets/imgs/road-back-home.png")
            #pixmap = pixmap.scaledToWidth(100)
            #pixmap = pixmap.scaled(self.iconSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            return None
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

    def fetchMore(self, index) -> None:
        if self.filmGenerator == None:
            return
        itemsToFetch: int = self.batch 
        if self.maxFilms >=0:
            itemsToFetch = min(itemsToFetch,self.maxFilms - len(self.films))
        worker: Worker = Worker(self.__fetchFilms,itemsToFetch)
        worker.signals.result.connect(self.appendRows)
        self.destroyed.connect(worker.exit)
        self.threadPool.start(worker)

    def __fetchFilms(self,maxFilms: int,progress_callback = None) -> List[Film]:
        if self.noMoreData or self.filmGenerator is None:
            return []
        buffer: List[Film] = []
        futures: List[Future] = []
        with ThreadPoolExecutor(3) as executor:
            for a in range(maxFilms):
                try:
                    film: Film = next(self.filmGenerator)
                    cachedIcon: Optional[QIcon] = QFilmListModel.cache.get(film.poster_url)
                    if cachedIcon is not None:
                        setattr(film, 'poster_icon',QIcon(cachedIcon) )
                    else:
                        future = executor.submit(self.loadIcon,film)
                        futures.append(future)
                    buffer.append(film)
                except StopIteration:
                    self.noMoreData = True
                    break
        return buffer

    def setFilmGenerator(self, filmGenerator: Optional[Iterator[Film]]) -> None:
        self.filmGenerator = filmGenerator
        self.beginResetModel()
        self.films.clear()
        self.noMoreData = False
        self.endResetModel()


    def appendRows(self,films: List[Film]) -> None:
        if films is not None and len(films) > 0:
            startRow: int = len(self.films)
            endRow: int = startRow + len(films) -1
            self.beginInsertRows(QModelIndex(), startRow,endRow)
            self.films.extend(films)
            self.endInsertRows()

    def clear(self):
        self.filmGenerator = None
        self.beginResetModel()
        self.films.clear()
        self.noMoreData = False
        self.endResetModel()

    def loadIcon(self,film: Film):
        headers =  {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
                }
        pixmap = QPixmap()
        r = requests.Request = QFilmListModel.session.get(film.poster_url,headers=headers) 
        pixmap.loadFromData(r.content)
        icon: QIcon = QIcon(pixmap)
        setattr(film, 'poster_icon',icon)
        QFilmListModel.cache[film.poster_url] = icon

    def deleteLator(self):
        self.threadPool.clear()
