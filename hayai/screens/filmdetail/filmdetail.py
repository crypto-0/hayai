from typing import  Optional
from PyQt6.QtCore import Q_ARG, QAbstractItemModel, QMetaObject, QModelIndex, QThread,  Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QIcon, QPixmap

from PyQt6.QtWidgets import QComboBox,  QFrame, QHBoxLayout,  QScrollArea, QSizePolicy, QVBoxLayout, QWidget
from hayai.features.filmdetail.widgets import QOverview
from hayai.features.filmdetail.models import SeasonListModel
from hayai.features.filmdetail.models import EpisodeListModel
from hayai.features.qprovider import QProvider
from hayai.features.widgets.autofitview import QAutoFitView
from hayai.features.models.filmlist import QFilmListModel
from hayai.features.widgets.filmrow import QFilmRow
from providers import Season, Episode, Provider,FilmInfo
from ..screen import QScreen


class QFilmDetail(QScreen):
    changeGenerator: pyqtSignal = pyqtSignal(object)

    def __init__(self,provider: Provider,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        self._qprovider = QProvider(provider)
        self._qproviderThread: QThread = QThread()
        self._qprovider.moveToThread(self._qproviderThread)
        self._qproviderThread.finished.connect(self._qprovider.deleteLater)

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
        self.recommendRow: QFilmRow = QFilmRow("You may also like",self.recommendModel,self._qprovider)

        self.seasonComboBox.currentIndexChanged.connect(self.__updateEpisodes)
        #self.recommendRow.filmClicked.connect(self.updateFilmDetail)
        self._qprovider.filmInfo.connect(self._filmInfo)

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
        self._qproviderThread.start()

    def loadFilmDetails(self,index: QModelIndex):
        model: QAbstractItemModel = index.model()
        linkIndex: QModelIndex = model.index(index.row(),1)
        isTVIndex: QModelIndex = model.index(index.row(),2)
        link: str = model.data(linkIndex,Qt.ItemDataRole.DisplayRole)
        isTv: bool = model.data(isTVIndex,Qt.ItemDataRole.DisplayRole)
        QMetaObject.invokeMethod(self._qprovider,"getFilmInfo",Q_ARG(str,link))
        #QMetaObject.invokeMethod(self._qprovider,"getFilmInfo",Q_ARG(str,link))
        


    @pyqtSlot(FilmInfo)
    def _filmInfo(self,filmInfo: FilmInfo):
        pixmap: QPixmap = QPixmap()
        pixmap.loadFromData(filmInfo.poster_image) #pyright: ignore
        posterIcon: QIcon = QIcon(pixmap)
        extra = f"release ({filmInfo.release}) "
        self.overview.updateOverview(posterIcon=posterIcon,title=filmInfo.title,description=filmInfo.description,genre=filmInfo.genre,country=filmInfo.country,duration=filmInfo.duration + "min",extra=extra)

    """
    @pyqtSlot(QModelIndex)
    def updateFilmDetail(self,index: QModelIndex):
        model: QAbstractItemModel = index.model()
        linkIndex: QModelIndex = model.index(index.row(),1)
        isTVIndex: QModelIndex = model.index(index.row(),2)
        link: str = model.data(linkIndex,Qt.ItemDataRole.DisplayRole)
        isTv: bool = model.data(isTVIndex,Qt.ItemDataRole.DisplayRole)
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
                self.seasonListModel.appendRow(season=seasons)
            self.seasonComboBox.setVisible(True)
            self.episodeView.setVisible(True)
        else:
            self.seasonComboBox.setVisible(False)
            self.episodeView.setVisible(False)
        self.overview.updateOverview(posterIcon=posterIcon,title=filmInfo.title,description=filmInfo.description,genre=filmInfo.genre,country=filmInfo.country,duration=filmInfo.duration + "min",extra=extra)
        generator: Iterator = iter(filmInfo.recommendation)
        self.changeGenerator.emit(generator)
        pass

    """
    def __updateEpisodes(self,index: int):
        pass
        """
        id: str = self.seasonComboBox.currentData(SeasonListModel.idRole)
        episodes: List[Episode] = self.providerParser.parse_episodes(id)
        self.episodeModel.appendRow(episode=episodes)
        self.episodeView.resize(self.size())
        """
    def onDestroy(self):
        self._qproviderThread.quit()
        self._qproviderThread.wait()
        return super().onDestroy()
        
