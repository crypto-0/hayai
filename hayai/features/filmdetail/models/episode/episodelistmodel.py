from typing import List, Optional
from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget
from providers import  Episode

class EpisodeListModel(QAbstractListModel):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self._episodes: List[Episode] = []
        self._defaultThumbnail: QIcon = QIcon("hayai/features/filmdetail/models/episode/assets/icons/no-image.svg")

    def rowCount(self, parent = QModelIndex()):
        return len(self._episodes)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 4

    def data(self, index: QModelIndex, role = Qt.ItemDataRole.DisplayRole): 
        if not index.isValid():
            return None
        row: int = index.row()
        col: int = index.column()

        if row >= self.rowCount() or row < 0 or col < 0 or col > self.columnCount():
            return None


        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return self._episodes[row].episode_number + "." + self._episodes[row].title

            if col == 1:
                return self._episodes[row].title
            if col == 2:
                return self._episodes[row].episode_number
            if col == 3:
                return self._episodes[row].id

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

