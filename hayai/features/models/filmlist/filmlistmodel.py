from typing import Dict, Optional
from PyQt6.QtCore import  QObject, Qt, pyqtSlot
from PyQt6.QtCore import QAbstractListModel
from PyQt6.QtCore import QModelIndex
from PyQt6.QtGui import QColor, QIcon, QImage, QPixmap 
from providers import Film
from .filmimageloader import QFilmImageLoader

class QFilmListModel(QAbstractListModel):

    def __init__(self, parent: Optional[QObject]=None,):
        super().__init__(parent)

        pixmap: QPixmap = QPixmap(600,int(600 * 1.5))
        pixmap.fill(QColor("#7c859E"))
        self._placeHolderIcon: QIcon = QIcon(pixmap)
        self._filmImageLoader: QFilmImageLoader = QFilmImageLoader()
        self._filmImageLoader.image.connect(self._imageLoaded)

        self._films: Dict[int,Film] = {}
        self._filmIcons: Dict[int,QIcon] = {}
        self._indexToKey: Dict[int,int] = {}
        self._keyToIndex: Dict[int,int] = {}

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._films)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 5

    def setData(self, index, value, role=Qt.ItemDataRole.DecorationRole) -> bool: 
        if value is None:
            return False
        if not index.isValid():
            return False
        
        row: int = index.row()
        col: int = index.column()

        if row >= self.rowCount() or row < 0:
            return False

        key: int = self._indexToKey[row]
        if role == Qt.ItemDataRole.DecorationRole: 
            if col == 0:
                self._filmIcons[key] = value
                self.dataChanged.emit(index,index, [role])
            return True

        return False

    def itemFromIndex(self,index: QModelIndex):
        if not index.isValid(): return None
        row: int = index.row()
        if row < 0 or row >= self.rowCount(): return None
        key: int = self._indexToKey[row]
        return self._films[key]

    def indexFromItem(self,film: Film):
        key: int = hash(film)
        if key not in self._keyToIndex:
            return QModelIndex()
        return self.createIndex(self._keyToIndex[key],0)


    def hasIndex(self, row: int, column: int, parent: QModelIndex = ...) -> bool:
        if parent.isValid() or row < 0 or row >= self.rowCount():
            return False
        return True

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if self.hasIndex(row,column=column,parent=parent):
            return self.createIndex(row, column)
        return QModelIndex()

    def data(self, index, role=Qt.ItemDataRole.DisplayRole) -> object: 
        if not index.isValid():
            return None
        row: int = index.row()
        col: int = index.column()

        if row >= self.rowCount() or row < 0 or col < 0 or col > self.columnCount():
            return None


        key: int = self._indexToKey[row]

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return self._films[key].title
            if col == 1:
                return self._films[key].link
            if col == 2:
                return self._films[key].is_tv
            if col == 3:
                return self._films[key].extra
            if col == 4:
                return self._films[key].poster_url

        if role == Qt.ItemDataRole.DecorationRole: 
            if col == 0:
                return self._filmIcons[key]

        return None
    

    def appendRow(self,*film: Film):
        if film:
            first: int = self.rowCount()
            last: int = first + len(film) -1
            self.beginInsertRows(QModelIndex(),first,last)
            for f in film:
                key: int = hash(f)
                if key in self._films:
                    continue

                self._films[key] = f
                self._keyToIndex[key] = len(self._films) -1
                self._indexToKey[len(self._films) -1] = key
                self._filmIcons[key] = self._placeHolderIcon
                self._filmImageLoader.loadImage(url=f.poster_url,filmHash=key)
                
            self.endInsertRows()

    def clear(self):
        self.beginResetModel()
        self._films.clear()
        self._filmIcons.clear()
        self._indexToKey.clear()
        self._keyToIndex.clear()
        self._filmImageLoader.cancel()
        self.endResetModel()

    def _imageLoaded(self,image: QImage,filmHash: int):
        if filmHash in self._films:
            index: QModelIndex = self.index(self._keyToIndex[filmHash],0)
            pixmap: QPixmap = QPixmap.fromImage(image)
            icon: QIcon = QIcon(pixmap)
            self.setData(index,icon)
