from typing import List, Optional, Type
from PyQt5.QtCore import QModelIndex, QSize, Qt
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QComboBox,  QFrame, QHBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy, QVBoxLayout, QWidget
from hayai.features.filmdetail import QOverview
from hayai.features.filmdetail import SeasonListModel
from hayai.features.filmdetail import EpisodeListModel
from hayai.widgets.film.filmdelegate.filmdelegatewidget import QFilmDelegate
from hayai.widgets.resizableiconlistview import QResizableIconListView
from hayai.widgets.film import QFilmListModel
from hayai.widgets.film import QFilmRow
from provider_parsers import Season, Episode, ProviderParser,FilmInfo


class QFilmDetail(QFrame):

    def __init__(self,providerParser: Type[ProviderParser],parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        self.providerParser: Type[ProviderParser] = providerParser

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

        self.seasonListModel: SeasonListModel = SeasonListModel()

        self.episodeModel : EpisodeListModel = EpisodeListModel()

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

        self.recommendRow: QFilmRow = QFilmRow("You may also like")

        self.seasonComboBox.currentIndexChanged.connect(self.__updateEpisodes)
        self.recommendRow.filmClicked.connect(self.updateFilmDetail)


        scrollAreaFrameLayout: QVBoxLayout = QVBoxLayout()
        scrollAreaFrameLayout.addWidget(self.overview)
        scrollAreaFrameLayout.addWidget(self.seasonComboBox)
        scrollAreaFrameLayout.addWidget(self.episodeView)
        scrollAreaFrameLayout.addWidget(self.recommendRow)
        scrollAreaFrameLayout.addStretch()
        scrollAreaFrameLayout.setContentsMargins(0,0,0,0)
        scrollAreaFrameLayout.setSpacing(10)
        scrollAreaFrame.setLayout(scrollAreaFrameLayout)

        filmdDetailLayout: QHBoxLayout = QHBoxLayout()
        filmdDetailLayout.addWidget(scrollArea)
        self.setLayout(filmdDetailLayout)

        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        self.setObjectName("QFilmDetail")

    def updateFilmDetail(self,index: QModelIndex):
        link: str = index.data(QFilmListModel.linkRole)
        isTv: bool = index.data(QFilmListModel.isTvRole)
        posterIcon: QIcon = index.data(Qt.DecorationRole) #pyright: ignore
        filmInfo: FilmInfo = self.providerParser.parse_info(link)
        self.overview.updateOverview(posterIcon=posterIcon,title=filmInfo.title,description=filmInfo.description,genre=filmInfo.genre,country=filmInfo.country,duration=filmInfo.duration + "min")
        if isTv:
            id: str = link.rsplit("-",1)[-1]
            seasons: List[Season] = self.providerParser.parse_seasons(id)
            if len(seasons) > 0:
                self.seasonListModel.loadSeasons(seasons=seasons)
                seasonIndex: QModelIndex = self.seasonListModel.index(0,0,QModelIndex())
                self.__updateEpisodes(seasonIndex)
            self.seasonComboBox.setVisible(True)
            self.episodeView.setVisible(True)
        else:
            self.seasonComboBox.setVisible(False)
            self.episodeView.setVisible(False)
        self.recommendRow.setFilmGenerator(iter(filmInfo.recommendation))

    def __updateEpisodes(self,index: int):
        id: str = self.seasonComboBox.currentData(SeasonListModel.idRole)
        episodes: List[Episode] = self.providerParser.parse_episodes(id)
        self.episodeModel.loadEpisodes(episodes=episodes)


