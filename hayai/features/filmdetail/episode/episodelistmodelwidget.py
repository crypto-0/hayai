from typing import List, Optional
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from provider_parsers.provider_parser import  Episode

class EpisodeListModel(QAbstractListModel):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.episodes: List[Episode] = []
        self.defaultThumbnail: QIcon = QIcon("hayai/features/filmdetail/episode/assets/icons/video.png")

    def rowCount(self, parent = QModelIndex()):
        return len(self.episodes)

    def data(self, index: QModelIndex, role = Qt.DisplayRole): #pyright: ignore
        if not index.isValid():
            return None
        if index.row() < 0 or index.row() >= len(self.episodes):
            return None

        if role == Qt.TextAlignmentRole: #pyright: ignore
            return Qt.AlignLeft | Qt.AlignVCenter #pyright: ignore

        if role == Qt.DisplayRole: #pyright: ignore
            return self.episodes[index.row()].episode_number + "." + self.episodes[index.row()].title
            #return self.episodes[index.row()].title

        if role == Qt.DecorationRole: #pyright: ignore
            return self.defaultThumbnail

        if role == Qt.UserRole: #pyright: ignore
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


