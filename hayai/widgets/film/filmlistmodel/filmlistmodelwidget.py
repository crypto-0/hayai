from collections.abc import Iterator
from typing import List, Optional 
from PyQt5.QtCore import  QCoreApplication, QThread, Qt, pyqtSignal
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QColor, QIcon, QImage, QPixmap 
from provider_parsers import Film
from .workers import QFilmGeneratorWorker
from .workers import QFilmImageWorker

class QFilmListModel(QAbstractListModel):
    extraRole: int = Qt.UserRole  #pyright: ignore
    isTvRole: int = Qt.UserRole + 1 #pyright: ignore
    linkRole: int = Qt.UserRole + 2 #pyright: ignore
    generatorChange: pyqtSignal = pyqtSignal(object)
    fetchFilms: pyqtSignal = pyqtSignal()
    fetchImage: pyqtSignal = pyqtSignal(str, QModelIndex)

    def __init__(self,filmGenerator:Optional[Iterator[Film]] = None,batch: int = 30,maxFilms: int = -1, parent=None,):
        super().__init__(parent)
        self.placeHolderPixmap: QPixmap = QPixmap(600,int(600 * 1.5))
        self.placeHolderPixmap.fill(QColor("#7c859E"))

        self.maxFilms: int = maxFilms
        self.films: List[Film] = []

        self.filmGeneratorWorker: QFilmGeneratorWorker = QFilmGeneratorWorker(filmGenerator,batch)
        self.filmGeneratorThread: QThread = QThread(parent=self)
        self.filmGeneratorWorker.moveToThread(self.filmGeneratorThread)
        self.filmGeneratorThread.finished.connect(self.filmGeneratorWorker.deleteLater)
        self.fetchFilms.connect(self.filmGeneratorWorker.fetchFilms) #pyright: ignore
        self.generatorChange.connect(self.filmGeneratorWorker.setGenerator) #pyright: ignore
        self.filmGeneratorWorker.result.connect(self.__appendFilms)

        self.filmImageWorker: QFilmImageWorker = QFilmImageWorker()
        self.filmImageThread: QThread = QThread(parent=self)
        self.filmImageWorker.moveToThread(self.filmImageThread)
        self.filmImageThread.finished.connect(self.filmImageWorker.deleteLater)
        self.fetchImage.connect(self.filmImageWorker.fetchImage) #pyright: ignore
        self.filmImageWorker.result.connect(self.__setFilmIconFromImage)

        self.filmGeneratorThread.start()
        self.filmImageThread.start()

        QCoreApplication.instance().aboutToQuit.connect(self.cleanup)


    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.films)

    def setData(self, index, value, role=Qt.EditRole) -> bool: #pyright: ignore
        if value is None:
            return False
        if not index.isValid():
            return False
        
        row: int = index.row()

        if row >= len(self.films) or row < 0:
            return False

        if role == Qt.DecorationRole: #pyright: ignore
            setattr(self.films[index.row()], 'poster_icon', value)
            self.films[index.row()].poster_data = None
            self.dataChanged.emit(index,index, [role])
            return True

        return False

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if parent.isValid() or row < 0 or row >= len(self.films):
            return QModelIndex()
        return self.createIndex(row, column)

    def data(self, index, role=Qt.DisplayRole) -> object: #pyright: ignore
        if not index.isValid():
            return None
        row: int = index.row()

        if row >= len(self.films) or row < 0:
            return None

        if role == QFilmListModel.isTvRole : #pyright: ignore
            return self.films[row].is_tv

        if role == QFilmListModel.linkRole : #pyright: ignore
            return self.films[row].link

        if role == QFilmListModel.extraRole : #pyright: ignore
            return self.films[row].extra

        if role == Qt.DisplayRole: #pyright: ignore
            return self.films[row].title

        if role == Qt.DecorationRole: #pyright: ignore
            #pixmap: QPixmap = QPixmap("hayai/assets/imgs/jujutsu.jpg")
            if hasattr(self.films[row],"poster_icon"):
                return self.films[row].poster_icon #pyright: ignore
            else:
                self.fetchImage.emit(self.films[row].poster_url,index)

            return QIcon(self.placeHolderPixmap)

            return None


        return None

    def canFetchMore(self, index: QModelIndex) -> bool:
        if self.maxFilms >= 0  and self.maxFilms  == len(self.films):
            return False
        return self.filmGeneratorWorker.hasMoreFilms()


    def fetchMore(self, index: QModelIndex) -> None:
        self.fetchFilms.emit()

    def __appendFilms(self,films):
        if len(films) > 0:
            startRow: int = len(self.films)
            endRow: int = startRow + len(films) -1
            self.beginInsertRows(QModelIndex(), startRow,endRow)
            self.films.extend(films)
            self.endInsertRows()

    def __setFilmIconFromImage(self,image: QImage,index: QModelIndex):
        pixmap: QPixmap = QPixmap.fromImage(image)
        icon: QIcon = QIcon(pixmap)
        self.setData(index,icon,Qt.DecorationRole) #pyright: ignore

    def setFilmGenerator(self, filmGenerator: Optional[Iterator[Film]]) -> None:
        self.beginResetModel()
        self.filmGeneratorWorker.cancel()
        self.filmImageWorker.cancel()
        self.generatorChange.emit(filmGenerator)
        self.films.clear()
        self.endResetModel()

    def clear(self):
        self.beginResetModel()
        self.filmGeneratorWorker.result.disconnect()
        self.films.clear()
        self.filmGeneratorWorker.result.connect(self.__appendFilms)
        self.endResetModel()

    def cleanup(self):
        self.filmGeneratorWorker.cancel()
        self.filmImageWorker.cancel()
        self.filmGeneratorThread.quit()
        self.filmGeneratorThread.wait()
        self.filmImageThread.quit()
        self.filmImageThread.wait()
