from typing import List, Optional
from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt6.QtWidgets import QWidget
from ...provider import Season

class QSeasonListModel(QAbstractListModel):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self._seasons: List[Season] = []

    def rowCount(self, parent = QModelIndex()):
        return len(self._seasons)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 3

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
                return "Season " + self._seasons[row].seasonNumber

            if col == 1:
                return self._seasons[row].seasonNumber
            if col == 2:
                return self._seasons[row].seasonId

        return None

    def appendRow(self,*season: Season):
        if season:
            first: int = self.rowCount()
            last: int = first + len(season) -1
            self.beginInsertRows(QModelIndex(),first,last)
            self._seasons.extend(season)

    def clear(self):
        self.beginResetModel()
        self._seasons.clear()
        self.endResetModel()

