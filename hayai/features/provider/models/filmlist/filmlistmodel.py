from typing import Dict, List, Optional
from PyQt6.QtCore import  QObject, QUrl, Qt, pyqtSignal
from PyQt6.QtCore import QAbstractListModel
from PyQt6.QtCore import QModelIndex
from PyQt6.QtGui import QColor, QIcon, QPixmap
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest 
from ...provider import Film

class QFilmListModel(QAbstractListModel):
    _abort: pyqtSignal = pyqtSignal()
    fetchMoreRequest: pyqtSignal = pyqtSignal()

    def __init__(self, parent: Optional[QObject]=None,):
        super().__init__(parent)

        pixmap: QPixmap = QPixmap(600,int(600 * 1.5))
        pixmap.fill(QColor("#7c859E"))
        self._placeHolderIcon: QIcon = QIcon(pixmap)
        self._films: List[Film] = []
        self._filmIcons: Dict[int,QIcon] = {}
        self._networkAccessManager: QNetworkAccessManager = QNetworkAccessManager(self)
        self._networkAccessManager.finished.connect(self._onPosterLoaded)

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._films)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 5

    def itemFromIndex(self,index: QModelIndex):
        if not index.isValid(): return None
        row: int = index.row()
        if row < 0 or row >= self.rowCount(): return None
        return self._films[row]



    def hasIndex(self, row: int, column: int, parent: QModelIndex = ...) -> bool:
        if parent.isValid() or row < 0 or row >= self.rowCount() or column < 0 or column >= self.columnCount():
            return False
        
        return True

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if self.hasIndex(row,column=column,parent=parent):
            return self.createIndex(row, column)
        return QModelIndex()

    def setData(self, index, value, role=Qt.ItemDataRole.DecorationRole) -> bool: 
        if value is None:
            return False
        if not index.isValid():
            return False
        
        row: int = index.row()
        col: int = index.column()

        if row >= self.rowCount() or row < 0:
            return False

        if role == Qt.ItemDataRole.DecorationRole: 
            if col == 0:
                key: int = hash(self._films[row])
                self._filmIcons[key] = value
                self.dataChanged.emit(index,index, [role])
            return True

        return False

    def data(self, index, role=Qt.ItemDataRole.DisplayRole) -> object: 
        if not index.isValid():
            return None
        row: int = index.row()
        col: int = index.column()

        if row >= self.rowCount() or row < 0 or col < 0 or col > self.columnCount():
            return None



        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return self._films[row].title
            if col == 1:
                return self._films[row].link
            if col == 2:
                return self._films[row].isTv
            if col == 3:
                return self._films[row].extra
            if col == 4:
                return self._films[row].posterUrl

        if role == Qt.ItemDataRole.DecorationRole: 
            if col == 0:
                key: int = hash(self._films[row])
                return self._filmIcons[key]

        return None
    

    def canFetchMore(self, parent: QModelIndex) -> bool:
        return True

    def fetchMore(self, parent: QModelIndex) -> None:
        self.fetchMoreRequest.emit()

    def appendRow(self,*film: Film):
        if film:
            first: int = self.rowCount()
            last: int = first + len(film) -1
            self.beginInsertRows(QModelIndex(),first,last)
            for idx, f in enumerate(film):
                key: int = hash(f)
                self._films.append(f)
                self._filmIcons[key] = self._placeHolderIcon
                row: int = first + idx
                request: QNetworkRequest = QNetworkRequest(QUrl(f.posterUrl))
                reply: QNetworkReply = self._networkAccessManager.get(request)
                reply.setProperty("row",row)
                self._abort.connect(reply.abort)
        self.endInsertRows()

    def clear(self):
        self.beginResetModel()
        self._films.clear()
        self._filmIcons.clear()
        self._abort.emit()
        self.endResetModel()

    def _onPosterLoaded(self,reply: QNetworkReply):
            if reply.error()  == QNetworkReply.NetworkError.NoError: 
                row: int = reply.property("row")
                data = reply.readAll().data()
                pixmap: QPixmap = QPixmap()
                pixmap.loadFromData(data) #pyright:ignore
                index: QModelIndex = self.index(row,0)
                self.setData(index,QIcon(pixmap))
            reply.deleteLater()
