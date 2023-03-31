from typing import List, Optional
from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget
from provider_parsers.provider_parser import  Episode

class EpisodeListModel(QAbstractListModel):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.episodes: List[Episode] = []
        self.defaultThumbnail: QIcon = QIcon("hayai/features/filmdetail/models/episode/assets/icons/no-image.svg")

    def rowCount(self, parent = QModelIndex()):
        return len(self.episodes)

    def data(self, index: QModelIndex, role = Qt.ItemDataRole.DisplayRole): 
        if not index.isValid():
            return None
        if index.row() < 0 or index.row() >= len(self.episodes):
            return None

        if role == Qt.ItemDataRole.TextAlignmentRole: 
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter 

        if role == Qt.ItemDataRole.DisplayRole: 
            return self.episodes[index.row()].episode_number + "." + self.episodes[index.row()].title

        if role == Qt.ItemDataRole.DecorationRole: 
            return self.defaultThumbnail

        if role == Qt.ItemDataRole.UserRole: 
            return self.episodes[index.row()].id
        return None

    def loadEpisodes(self,episodes: List[Episode]):
        if episodes is not None:
            self.beginResetModel()
            self.episodes.clear()
            self.episodes.extend(episodes)
            self.endResetModel()

    def clear(self):
        self.beginResetModel()
        self.episodes.clear()
        self.endResetModel()


