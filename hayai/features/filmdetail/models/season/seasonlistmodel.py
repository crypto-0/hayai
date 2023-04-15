from typing import List, Optional
from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt6.QtWidgets import QWidget
from providers import Season

class SeasonListModel(QAbstractListModel):
    idRole: int = Qt.ItemDataRole.UserRole

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self._seasons: List[Season] = []

    def rowCount(self, parent = QModelIndex()):
        return len(self._seasons)

    def data(self, index: QModelIndex, role = Qt.ItemDataRole.DisplayRole): 
        if not index.isValid():
            return None
        row: int = index.row()
        col: int = index.column()

        if row >= self.rowCount() or row < 0 or col < 0 or col > self.columnCount():
            return None


        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return "Season " + self._seasons[row].season_number

            if col == 1:
                return self._seasons[row].season_number
            if col == 2:
                return self._seasons[row].id

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

