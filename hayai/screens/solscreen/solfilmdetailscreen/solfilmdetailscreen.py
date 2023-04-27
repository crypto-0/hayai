
from typing import List, Optional

from PyQt6.QtCore import  QModelIndex, QPoint, Qt, pyqtSignal
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QDataWidgetMapper,
    QFrame,
    QHBoxLayout,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
)
from PyQt6.QtWidgets import QWidget
from hayai.features.provider.provider import VideoServer
from hayai.features.provider.extractors.videoextractor import VideoContainer
from hayai.features.provider.widgets.film import QFilmDetail
from hayai.features.provider.widgets.film import QFilmDescription
from hayai.features.provider.widgets.film import QFilmPoster
from hayai.features.provider.widgets.serversmenu import QServersMenu
from hayai.features.provider.delegates.filmdelegate import QFilmDelegate
from hayai.features.sol.viewmodels import QSolFilmDetailViewModel
from hayai.features.widgets.autofitview  import QAutoFitView
from hayai.features.widgets.rowview import QRowView

from ...screen import QScreen

class QSolFilmDetailScreen(QScreen):

    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)
    playMedia: pyqtSignal = pyqtSignal(str)
    def __init__(self,filmUrl: str= "", parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)
        self._filmDetailViewModel: QSolFilmDetailViewModel = QSolFilmDetailViewModel(filmUrl)

        scrollAreaFrame: QFrame = QFrame()

        scrollArea = QScrollArea()
        self.horizontalScrollBar = scrollArea.horizontalScrollBar()
        scrollArea.setObjectName("scroll-area")
        scrollArea.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        
        scrollArea.setWidget(scrollAreaFrame)
        scrollArea.horizontalScrollBar().setEnabled(False)
        scrollArea.verticalScrollBar().setEnabled(True)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setWidgetResizable(True)
        scrollArea.setContentsMargins(0,0,0,0)

        leftFrame: QFrame = QFrame()
        leftFrame.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.MinimumExpanding)
        rightFrame: QFrame = QFrame()
        overviewFrame: QFrame = QFrame()

        self.poster: QFilmPoster = QFilmPoster()
        filmDescription: QFilmDescription = QFilmDescription()
        filmDetail: QFilmDetail = QFilmDetail()

        self.widgetMapper: QDataWidgetMapper = QDataWidgetMapper()
        self.widgetMapper.setModel(self._filmDetailViewModel.filmInfo)
        self.widgetMapper.addMapping(filmDescription.titleLabel,0,b"text") #pyright: ignore
        self.widgetMapper.addMapping(filmDescription.descriptionLabel,2,b"text") #pyright: ignore
        self.widgetMapper.addMapping(self.poster,6,b"pixmap") #pyright: ignore
        self.widgetMapper.toFirst()

        self._seasonComboBox: QComboBox = QComboBox()
        self._seasonComboBox.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed)
        self._seasonComboBox.setModel(self._filmDetailViewModel.seasons)
        self._seasonComboBox.hide()

        self._episodeView: QAutoFitView = QAutoFitView(showAll=True)
        self._episodeView.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self._episodeView.setSpacing(0)
        self._episodeView.setWrapping(True)
        self._episodeView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) #pyright: ignore
        self._episodeView.horizontalScrollBar().setEnabled(False)
        self._episodeView.setModel(self._filmDetailViewModel.episodes)
        self._episodeView.hide()


        self._recommendationRow: QRowView = QRowView("You may also like",self._filmDetailViewModel.filmRecomendation,QFilmDelegate())


        self.started.connect(self._filmDetailViewModel.loadFilmInfo)
        self._seasonComboBox.currentIndexChanged.connect(self.onSeasonComboboxIndexChange)
        self._filmDetailViewModel.seasonsLoadingFinished.connect(self.seasonsLoadingFinished)
        self._filmDetailViewModel.episodesLoadingFinished.connect(self.episodesLoadingFinished)
        self._filmDetailViewModel.serversLoaded.connect(self.serversLoaded)
        self._episodeView.clicked.connect(self.onEpisodeClicked)
        self._recommendationRow.itemClicked.connect(self.filmClicked)
        self._filmDetailViewModel.videoLoaded.connect(self.videoLoaded)

        leftFrameLayout: QVBoxLayout = QVBoxLayout()
        leftFrameLayout.addWidget(self.poster)
        leftFrameLayout.addStretch()
        leftFrameLayout.setContentsMargins(0,0,0,0)
        leftFrameLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        leftFrame.setLayout(leftFrameLayout)

        rightFrameLayout: QVBoxLayout = QVBoxLayout()
        rightFrameLayout.addWidget(filmDescription)
        rightFrameLayout.addWidget(filmDetail)
        rightFrameLayout.setContentsMargins(30,20,5,0)
        rightFrameLayout.setSpacing(10)
        rightFrame.setLayout(rightFrameLayout)

        overviewLayout: QHBoxLayout = QHBoxLayout()
        overviewLayout.addWidget(leftFrame)
        overviewLayout.addWidget(rightFrame)
        overviewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        overviewLayout.setContentsMargins(0,0,0,0)
        overviewLayout.setSpacing(5)
        overviewFrame.setLayout(overviewLayout)

        scrollAreaFrameLayout: QVBoxLayout = QVBoxLayout()
        scrollAreaFrameLayout.addWidget(overviewFrame)
        scrollAreaFrameLayout.addWidget(self._seasonComboBox)
        scrollAreaFrameLayout.addWidget(self._episodeView)
        scrollAreaFrameLayout.addWidget(self._recommendationRow)
        scrollAreaFrameLayout.setContentsMargins(0,0,0,0)
        scrollAreaFrameLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scrollAreaFrameLayout.setSpacing(0)
        scrollAreaFrame.setLayout(scrollAreaFrameLayout)

        filmDetailLayout: QHBoxLayout = QHBoxLayout()
        filmDetailLayout.addWidget(scrollArea)
        filmDetailLayout.setContentsMargins(20,20,0,0)
        filmDetailLayout.setSpacing(0)
        self.setLayout(filmDetailLayout)

        self.title = "FilmDetail"

    def seasonsLoadingFinished(self):
        self._seasonComboBox.show()
        self._seasonComboBox.setCurrentIndex(0)

    def episodesLoadingFinished(self):
        self._episodeView.show()
        self._episodeView.resize(self.size())

    def serversLoaded(self,servers: List[VideoServer]):
        if servers:
            menu = QServersMenu(servers)
            menu.setFixedWidth(self.width())
            menu.setFixedHeight(self.height()//3)
            menu.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
            bottomPos: QPoint = self.rect().bottomLeft()
            bottomPos.setY(bottomPos.y() - menu.height() + 20)
            action = menu.exec(self.mapToGlobal(bottomPos)) 
            if action and isinstance(action.data(),VideoServer):
                self._filmDetailViewModel.loadVideo(action.data())

    def videoLoaded(self,videoContainer: VideoContainer):
        if len(videoContainer.videos) > 0:
            self.playMedia.emit(videoContainer.videos[0].url)

    def onSeasonComboboxIndexChange(self,index: int):
        self._filmDetailViewModel.loadEpisodes(index)

    def onEpisodeClicked(self,index: QModelIndex):
        self._filmDetailViewModel.loadServers(index.row())

