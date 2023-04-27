from typing import List, Optional
from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget
from ...provider import Episode

class QEpisodeListModel(QAbstractListModel):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self._episodes: List[Episode] = []
        self._defaultThumbnail: QIcon = QIcon("hayai/features/provider/models/episodelist/assets/icons/no-image.svg")

    def rowCount(self, parent = QModelIndex()):
        return len(self._episodes)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 4

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

    def data(self, index: QModelIndex, role = Qt.ItemDataRole.DisplayRole): 
        if not index.isValid():
            return None
        row: int = index.row()
        col: int = index.column()

        if row >= self.rowCount() or row < 0 or col < 0 or col > self.columnCount():
            return None


        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return self._episodes[row].episodeNumber + "." + self._episodes[row].title

            if col == 1:
                return self._episodes[row].title
            if col == 2:
                return self._episodes[row].episodeNumber
            if col == 3:
                return self._episodes[row].episodeId

        elif role == Qt.ItemDataRole.DecorationRole: 
            if col == 0:
                return self._defaultThumbnail

        return None

    def appendRow(self,*episode: Episode):
        if episode:
            first: int = self.rowCount()
            last: int = first + len(episode) -1
            self.beginInsertRows(QModelIndex(),first,last)
            self._episodes.extend(episode)
            self.endInsertRows()

    def clear(self):
        self.beginResetModel()
        self._episodes.clear()
        self.endResetModel()

