from collections.abc import Iterator
from typing import List, Optional 
from PyQt6.QtCore import  QCoreApplication, QThread, Qt, pyqtSignal
from PyQt6.QtCore import QAbstractListModel
from PyQt6.QtCore import QModelIndex
from PyQt6.QtGui import QColor, QIcon, QImage, QPixmap 
from provider_parsers import Film
from .workers import QFilmGeneratorWorker
from .workers import QFilmImageWorker

class QFilmListModel(QAbstractListModel):
    extraRole: int = Qt.ItemDataRole.UserRole  
    isTvRole: int = Qt.ItemDataRole.UserRole + 1 
    linkRole: int = Qt.ItemDataRole.UserRole + 2 
    generatorChange: pyqtSignal = pyqtSignal(object)
    fetchFilms: pyqtSignal = pyqtSignal()
    fetchImage: pyqtSignal = pyqtSignal(str, QModelIndex)

    def __init__(self,filmGenerator:Optional[Iterator[Film]] = None,batch: int = 30, parent=None,):
        super().__init__(parent)
        self.placeHolderPixmap: QPixmap = QPixmap(600,int(600 * 1.5))
        self.placeHolderPixmap.fill(QColor("#7c859E"))

        self.films: List[Film] = []

        self.filmGeneratorWorker: QFilmGeneratorWorker = QFilmGeneratorWorker(filmGenerator,batch)
        self.filmGeneratorThread: QThread = QThread(parent=self)
        self.filmGeneratorWorker.moveToThread(self.filmGeneratorThread)
        self.filmGeneratorThread.finished.connect(self.filmGeneratorWorker.deleteLater)
        self.fetchFilms.connect(self.filmGeneratorWorker.fetchFilms)
        self.generatorChange.connect(self.filmGeneratorWorker.setGenerator) 
        self.filmGeneratorWorker.result.connect(self.__insertFilms)

        self.filmImageWorker: QFilmImageWorker = QFilmImageWorker()
        self.filmImageThread: QThread = QThread(parent=self)
        self.filmImageWorker.moveToThread(self.filmImageThread)
        self.filmImageThread.finished.connect(self.filmImageWorker.deleteLater)
        self.fetchImage.connect(self.filmImageWorker.fetchImage) 
        self.filmImageWorker.result.connect(self.__insertImage)

        self.filmGeneratorThread.start()
        self.filmImageThread.start()

        QCoreApplication.instance().aboutToQuit.connect(self.cleanup)


    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.films)

    def setData(self, index, value, role=Qt.ItemDataRole.DecorationRole) -> bool: 
        if value is None:
            return False
        if not index.isValid():
            return False
        
        row: int = index.row()

        if row >= len(self.films) or row < 0:
            return False

        if role == Qt.ItemDataRole.DecorationRole: 
            setattr(self.films[index.row()], 'poster_icon', value)
            self.films[index.row()].poster_data = None
            self.dataChanged.emit(index,index, [role])
            return True

        return False

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if parent.isValid() or row < 0 or row >= len(self.films):
            return QModelIndex()
        return self.createIndex(row, column)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole) -> object: #pyright: ignore
        if not index.isValid():
            return None
        row: int = index.row()

        if row >= len(self.films) or row < 0:
            return None

        if role == QFilmListModel.isTvRole : 
            return self.films[row].is_tv

        if role == QFilmListModel.linkRole : 
            return self.films[row].link

        if role == QFilmListModel.extraRole : 
            return self.films[row].extra

        if role == Qt.ItemDataRole.DisplayRole: 
            return self.films[row].title

        if role == Qt.ItemDataRole.DecorationRole: 
            if hasattr(self.films[row],"poster_icon"):
                return self.films[row].poster_icon #pyright: ignore
            else:
                self.fetchImage.emit(self.films[row].poster_url,index)

            return QIcon(self.placeHolderPixmap)

            return None

        return None

    def canFetchMore(self, index: QModelIndex) -> bool:
        return self.filmGeneratorWorker.hasMoreFilms()

    def fetchMore(self, index: QModelIndex) -> None:
        self.fetchFilms.emit()

    def __insertFilms(self,films):
        if len(films) > 0:
            startRow: int = len(self.films)
            endRow: int = startRow + len(films) -1
            self.beginInsertRows(QModelIndex(), startRow,endRow)
            self.films.extend(films)
            self.endInsertRows()

    def __insertImage(self,index: QModelIndex,image: QImage,):
        pixmap: QPixmap = QPixmap.fromImage(image)
        icon: QIcon = QIcon(pixmap)
        self.setData(index,icon,Qt.ItemDataRole.DecorationRole) 

    def reset(self, filmGenerator: Optional[Iterator[Film]] = None) -> None:
        self.beginResetModel()
        self.filmGeneratorWorker.cancel()
        self.filmImageWorker.cancel()
        self.generatorChange.emit(filmGenerator)
        self.films.clear()
        self.endResetModel()

    def cleanup(self):
        self.filmGeneratorWorker.cancel()
        self.filmImageWorker.cancel()
        self.filmGeneratorThread.quit()
        self.filmGeneratorThread.wait()
        self.filmImageThread.quit()
        self.filmImageThread.wait()
