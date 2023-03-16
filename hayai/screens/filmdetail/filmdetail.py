from typing import Optional
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap, QResizeEvent
import math

from PyQt5.QtWidgets import QComboBox, QDialog, QFrame, QHBoxLayout, QScrollArea, QSizePolicy, QVBoxLayout, QWidget
from hayai.features.filmdetail import QOverview
from hayai.features.filmdetail import SeasonListModel
from hayai.features.filmdetail import EpisodeListModel
from hayai.widgets.resizableiconlistview import QResizableIconListView
from provider_parsers import Season, Episode

class QFilmDetail(QFrame):

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        scrollAreaFrame: QFrame = QFrame()
        scrollAreaFrame.setObjectName("QScrollAreaFrame")
        scrollAreaFrame.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Minimum)

        scrollArea = QScrollArea()
        #scrollArea.setFixedWidth(320)
        scrollArea.setObjectName("scroll-area")
        scrollArea.setWidget(scrollAreaFrame)
        scrollArea.horizontalScrollBar().setEnabled(False)
        #scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scrollArea.setWidgetResizable(True)
        scrollArea.setContentsMargins(0,0,0,0)

        self.overview: QOverview = QOverview()
        title: str = "Fullmetal Alchemist: Brotherhood One piece"
        description: str = "Gold Roger was known as the  the strongest and most infamous being to have sailed the Grand Line. The capture and execution of Roger by the World Government brought a change throughout the world. His last words before his death revealed the existence of the greatest treasure in the world, One Piece. It was this revelation that brought about the Grand Age of Pirates, men who dreamed of finding One Piece—which promises an unlimited amount of riches and fame—and quite possibly the pinnacle of glory and the title of the Pirate King. Enter Monkey Luffy, a 17-year-old boy who defies your standard definition of a pirate. Rather than the popular persona of a wicked, hardened, toothless pirate ransacking villages for fun, Luffy's reason for being a pirate is one of pure wonder: the thought of an exciting adventure that leads him to intriguing people and ultimately, the promised treasure. Following in the footsteps of his childhood hero, Luffy and his crew travel across the Grand Line, experiencing crazy adventures, unveiling dark mysteries and battling strong enemies, all in order to reach the most coveted of all fortunes—One Piece. [Written by MAL Rewrite] - Less"
        #description: str = "Test"
        #icon: QIcon = QIcon("hayai/assets/imgs/creed3.jpg")
        icon: QIcon = QIcon("hayai/assets/imgs/creed3.jpg")
        self.overview.updateOverview(icon,title,description)

        self.seasonListModel: SeasonListModel = SeasonListModel()
        self.seasonListModel.loadSeasons([Season("Season 1","id"),Season("Season 2","id"),Season("Season 1","id"),Season("Season 2","id")])

        self.episodeModel : EpisodeListModel = EpisodeListModel()
        episodes = []
        for i in range(20):
            episode: Episode = Episode(f"{i}","id",f"Episode: {i}")
            episodes.append(episode)
        self.episodeModel.loadEpisodes(episodes)

        self.seasonComboBox: QComboBox = QComboBox()
        self.seasonComboBox.setModel(self.seasonListModel)

        self.episodeView: QResizableIconListView = QResizableIconListView()
        self.episodeView.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.episodeView.setIconRatio(.7)
        self.episodeView.setMinimumIconSize(200,int(200 * .7))
        self.episodeView.setSpacing(0)
        self.episodeView.setWrapping(True)
        self.episodeView.setShowAll(True)
        self.episodeView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #pyright: ignore
        self.episodeView.horizontalScrollBar().setEnabled(False)
        self.episodeView.setModel(self.episodeModel)
        #self.episodeView.setMinimumHeight(total_height)

        scrollArea.verticalScrollBar().valueChanged.connect(self.episodeView.verticalScrollBar().setValue)

        scrollAreaFrameLayout: QVBoxLayout = QVBoxLayout()
        scrollAreaFrameLayout.addWidget(self.overview)
        scrollAreaFrameLayout.addWidget(self.seasonComboBox)
        scrollAreaFrameLayout.addWidget(self.episodeView)
        scrollAreaFrameLayout.setContentsMargins(0,0,0,0)
        scrollAreaFrameLayout.setSpacing(10)
        scrollAreaFrame.setLayout(scrollAreaFrameLayout)

        filmdDetailLayout: QHBoxLayout = QHBoxLayout()
        filmdDetailLayout.addWidget(scrollArea)
        self.setLayout(filmdDetailLayout)

        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        self.setObjectName("QFilmDetail")

    """
    def resizeEvent(self, event: QResizeEvent) -> None:
        rowHeight = self.episodeView.sizeHintForRow(0)
        colWidth = self.episodeView.sizeHintForColumn(0)
        numCols: int = self.episodeView.width() // colWidth
        numCols = max(1,numCols)
        rows: int = math.ceil(self.episodeModel.rowCount()/ numCols)
        total_height = rowHeight * rows
        self.episodeView.setMinimumHeight(total_height)
        super().resizeEvent(event)
        """

