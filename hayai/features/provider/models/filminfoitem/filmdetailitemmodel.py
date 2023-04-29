from typing import Optional
from PyQt6.QtCore import QAbstractItemModel, QModelIndex, QUrl, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt6.QtWidgets import QWidget
from ...provider import FilmInfo

class QFilmInfoItemModel(QAbstractItemModel):
    _abort: pyqtSignal = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self._filmInfo: FilmInfo = FilmInfo()
        pixmap: QPixmap = QPixmap(600,int(600 * 1.5))
        pixmap.fill(QColor("#7c859E"))
        self._placeHolderPixmap: QPixmap = pixmap
        self._posterPixmap: Optional[QPixmap] = None
        self._networkAccessManager: QNetworkAccessManager = QNetworkAccessManager(self)
        self._networkAccessManager.finished.connect(self._onPosterLoaded)

    def rowCount(self, parent = QModelIndex()):
        return 1

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 7

    def hasIndex(self, row: int, column: int, parent: QModelIndex = ...) -> bool:
        if parent.isValid() or row < 0 or row >= self.rowCount() or column < 0 or column >= self.columnCount():
            return False
        
        return True

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if self.hasIndex(row,column=column,parent=parent):
            return self.createIndex(row, column)
        return QModelIndex()

    def sibling(self, row: int, column: int, idx: QModelIndex) -> QModelIndex:
        if idx.row() == row:
            return self.index(row,column)
        return QModelIndex()

    def parent(self,index: QModelIndex):
        return QModelIndex()

    def data(self, index: QModelIndex, role = Qt.ItemDataRole.DisplayRole): 
        if not index.isValid():
            return None
        if self._filmInfo is None:
            return
        row: int = index.row()
        col: int = index.column()

        if row >= self.rowCount() or row < 0 or col < 0 or col > self.columnCount():
            return None

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            if col == 0:
                return self._filmInfo.title.capitalize()
            if col == 1:
                return self._filmInfo.release
            if col == 2:
                return self._filmInfo.description
            if col == 3:
                return self._filmInfo.genre
            if col == 4:
                return self._filmInfo.country
            if col == 5:
                return self._filmInfo.duration
            if col == 6:
                if self._posterPixmap is not None:
                    return self._posterPixmap
                return self._placeHolderPixmap
        if role == Qt.ItemDataRole.DecorationRole:
            return self._placeHolderPixmap

        return None

    def setItem(self,filmInfo: FilmInfo):
        self._abort.emit()
        self._filmInfo = filmInfo
        request: QNetworkRequest = QNetworkRequest(QUrl(filmInfo.posterUrl))
        reply: QNetworkReply = self._networkAccessManager.get(request)
        self._abort.connect(reply.abort)
        self.dataChanged.emit(self.index(0,0),self.index(0,self.columnCount()-2),[])

    def _onPosterLoaded(self,reply: QNetworkReply):
        if reply.error()  == QNetworkReply.NetworkError.NoError: 
            data = reply.readAll().data()
            pixmap: QPixmap = QPixmap()
            pixmap.loadFromData(data) #pyright:ignore
            self._posterPixmap = pixmap
            index: QModelIndex = self.index(0,6)
            self.dataChanged.emit(index,index, [Qt.ItemDataRole.DecorationRole])
        reply.deleteLater()

