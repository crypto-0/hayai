from typing import Optional
from PyQt6.QtCore import QAbstractItemModel, QModelIndex, Qt
from PyQt6.QtGui import QColor, QIcon, QPixmap
from PyQt6.QtWidgets import QWidget
from ...provider import FilmInfo

class QFilmInfoItemModel(QAbstractItemModel):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.filmInfo: Optional[FilmInfo] = FilmInfo(title="testing title",description="testing description")
        pixmap: QPixmap = QPixmap(600,int(600 * 1.5))
        pixmap.fill(QColor("#7c859E"))
        self._placeHolderPixmap: QPixmap = pixmap

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


    def data(self, index: QModelIndex, role = Qt.ItemDataRole.DisplayRole): 
        if not index.isValid():
            return None
        if self.filmInfo is None:
            return
        row: int = index.row()
        col: int = index.column()

        if row >= self.rowCount() or row < 0 or col < 0 or col > self.columnCount():
            return None

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            if col == 0:
                return self.filmInfo.title
            if col == 1:
                return self.filmInfo.release
            if col == 2:
                return self.filmInfo.description
            if col == 3:
                return self.filmInfo.genre
            if col == 4:
                return self.filmInfo.country
            if col == 5:
                return self.filmInfo.duration
            if col == 6:
                print("here")
                return self._placeHolderPixmap
        if role == Qt.ItemDataRole.DecorationRole:
            return self._placeHolderPixmap

        return None

    def setItem(self,filmInfo: FilmInfo):
        self.beginResetModel()
        self.filmInfo = filmInfo
        self.endResetModel()

    def clear(self):
        self.beginResetModel()
        self.filmInfo = None
        self.endResetModel()

