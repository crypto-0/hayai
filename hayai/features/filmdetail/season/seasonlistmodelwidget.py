from typing import List, Optional
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt5.QtWidgets import QWidget
from provider_parsers.provider_parser import Season

class SeasonListModel(QAbstractListModel):
    idRole: int = Qt.UserRole #pyright: ignore

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.seasons: List[Season] = []

    def rowCount(self, parent = QModelIndex()):
        return len(self.seasons)

    def data(self, index: QModelIndex, role = Qt.DisplayRole): #pyright: ignore
        if not index.isValid():
            return None
        if index.row() < 0 or index.row() >= len(self.seasons):
            return None
        if role == Qt.DisplayRole: #pyright: ignore
            return "Season " + self.seasons[index.row()].season_number
        if role == SeasonListModel.idRole: #pyright: ignore
            return self.seasons[index.row()].id
        return None

    def loadSeasons(self,seasons: List[Season]):
        self.beginResetModel()
        self.seasons.clear()
        self.seasons.extend(seasons)
        self.endResetModel()
    def clear(self):
        self.beginResetModel()
        self.seasons.clear()
        self.endResetModel()


