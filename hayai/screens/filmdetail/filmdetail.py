from typing import List, Optional, Type
from PyQt6.QtCore import QModelIndex,  Qt
from PyQt6.QtGui import QIcon

from PyQt6.QtWidgets import QComboBox,  QFrame, QHBoxLayout,  QScrollArea, QSizePolicy, QVBoxLayout, QWidget
from hayai.features.filmdetail.widgets import QOverview
from hayai.features.filmdetail.models import SeasonListModel
from hayai.features.filmdetail.models import EpisodeListModel
from hayai.features.widgets.autofitview import QAutoFitView
from hayai.features.models import QFilmListModel
from hayai.features.widgets.film import QFilmRow
from hayai.features.widgets.film import QFilmDelegate
from provider_parsers import Season, Episode, ProviderParser,FilmInfo


class QFilmDetail(QFrame):

    def __init__(self,providerParser: Type[ProviderParser],parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        self.providerParser: Type[ProviderParser] = providerParser

        scrollAreaFrame: QFrame = QFrame()
        scrollAreaFrame.setObjectName("QScrollAreaFrame")
        scrollAreaFrame.setSizePolicy(QSizePolicy.Policy.Ignored,QSizePolicy.Policy.Minimum)

        scrollArea = QScrollArea()
        scrollArea.setObjectName("scroll-area")
        scrollArea.setWidget(scrollAreaFrame)
        scrollArea.horizontalScrollBar().setEnabled(False)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scrollArea.setWidgetResizable(True)
        scrollArea.setContentsMargins(0,0,0,0)

        self.overview: QOverview = QOverview()

        self.seasonListModel: SeasonListModel = SeasonListModel()

        self.episodeModel : EpisodeListModel = EpisodeListModel()

        self.seasonComboBox: QComboBox = QComboBox()
        self.seasonComboBox.setModel(self.seasonListModel)

        self.episodeView: QAutoFitView = QAutoFitView(showAll=True)
        self.episodeView.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.episodeView.setSpacing(0)
        self.episodeView.setWrapping(True)
        self.episodeView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) #pyright: ignore
        self.episodeView.horizontalScrollBar().setEnabled(False)
        self.episodeView.setModel(self.episodeModel)


        self.recommendModel: QFilmListModel = QFilmListModel()
        self.recommendView: QAutoFitView = QAutoFitView()
        self.recommendView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.recommendView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.recommendView.setItemDelegate(QFilmDelegate())
        self.recommendView.setModel(self.recommendModel)
        self.recommendRow: QFilmRow = QFilmRow("You may also like",self.recommendView)

        self.seasonComboBox.currentIndexChanged.connect(self.__updateEpisodes)
        self.recommendView.clicked.connect(self.updateFilmDetail)

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

    def __fetchFilmDetails(self,link: str,progress_callback = None):
        filmInfo: FilmInfo = self.providerParser.parse_info(link)
        id: str = link.rsplit("-",1)[-1]
        seasons: List[Season] = self.providerParser.parse_seasons(id)


    def updateFilmDetail(self,index: QModelIndex):
        link: str = index.data(QFilmListModel.linkRole)
        isTv: bool = index.data(QFilmListModel.isTvRole)
        posterIcon: QIcon = index.data(Qt.ItemDataRole.DecorationRole) 
        filmInfo: FilmInfo = self.providerParser.parse_info(link)
        if isTv:
            extra: str = "TV"
        else:
            extra: str = "Movie"
        extra = f"{extra} ({filmInfo.release}) "
        if isTv:
            id: str = link.rsplit("-",1)[-1]
            seasons: List[Season] = self.providerParser.parse_seasons(id)
            extra += f"{len(seasons)} Seasons"
            if len(seasons) > 0:
                self.seasonListModel.loadSeasons(seasons=seasons)
            self.seasonComboBox.setVisible(True)
            self.episodeView.setVisible(True)
        else:
            self.seasonComboBox.setVisible(False)
            self.episodeView.setVisible(False)
        self.overview.updateOverview(posterIcon=posterIcon,title=filmInfo.title,description=filmInfo.description,genre=filmInfo.genre,country=filmInfo.country,duration=filmInfo.duration + "min",extra=extra)
        self.recommendModel.reset(iter(filmInfo.recommendation))

    def __updateEpisodes(self,index: int):
        id: str = self.seasonComboBox.currentData(SeasonListModel.idRole)
        episodes: List[Episode] = self.providerParser.parse_episodes(id)
        self.episodeModel.loadEpisodes(episodes=episodes)
        self.episodeView.resize(self.size())

