
from typing import Any, Dict, List, Optional
from PyQt6.QtCore import QModelIndex, QObject, pyqtSignal
from ....provider.models.filmlist import QFilmListModel
from ....provider.models.seasonlist import QSeasonListModel
from ....provider.models.episodelist import QEpisodeListModel
from ....provider.models.filminfoitem import QFilmInfoItemModel
from ....provider.extractors.videoextractor import VideoContainer
from ...sol import  QSol, FilmInfo,Episode, Season,VideoServer

class QSolFilmDetailViewModel(QObject):
    episodesLoadingFinished: pyqtSignal = pyqtSignal()
    seasonsLoadingFinished: pyqtSignal = pyqtSignal()
    serversLoaded: pyqtSignal = pyqtSignal(list)
    videoLoaded: pyqtSignal = pyqtSignal(VideoContainer)

    def __init__(self,filmUrl: str = "",parent: Optional[QObject] = None):
        super().__init__(parent=parent)
        self._sol: QSol = QSol(self)
        self._filmInfo: QFilmInfoItemModel = QFilmInfoItemModel()
        self._filmRecomendation: QFilmListModel = QFilmListModel()
        self._seasons: QSeasonListModel = QSeasonListModel()
        self._episodes: QEpisodeListModel = QEpisodeListModel()
        self._loadingFilmInfo: bool = False
        self._loadingSeasons: bool = False
        self._loadingEpisodes: bool = False
        self._loadingServers: bool = False
        self._filmUrl = filmUrl;
        self._sol.filmInfoLoaded.connect(self.filmInfoLoaded)
        self._sol.episodesLoaded.connect(self.episodesLoaded)
        self._sol.seasonsLoaded.connect(self.seasonsLoaded)
        self._sol.episodeServersLoaded.connect(self.serversLoaded)
        self._sol.movieServersLoaded.connect(self.serversLoaded)
        self._sol.videoLoaded.connect(self.videoLoaded)
        self._servers: Dict[str,VideoServer] = {}

    @property
    def filmInfo(self):
        return self._filmInfo

    @property
    def filmRecomendation(self):
        return self._filmRecomendation

    @property
    def seasons(self):
        return self._seasons

    @property
    def episodes(self):
        return self._episodes
    @property
    def servers(self):
        return list(self._servers.keys())

    def loadFilmInfo(self):
        if self._loadingFilmInfo or not self._filmUrl or self._loadingSeasons:
            return
        self._loadingFilmInfo = True
        self._sol.loadFilmInfo(self._filmUrl)

    def filmInfoLoaded(self,filmInfo: FilmInfo):
        self._loadingFilmInfo = False
        self._filmInfo.setItem(filmInfo)
        if len(filmInfo.recommendation) > 0:
            self._filmRecomendation.clear()
            self._filmRecomendation.appendRow(*filmInfo.recommendation)
        filmUrlSplit = self._filmUrl.rsplit("/",2)
        if len(filmUrlSplit) > 1 and filmUrlSplit[-2] == "tv":
            seasonId: str = filmUrlSplit[-1].rsplit("-",1)[-1]
            self._loadingSeasons = True
            self._sol.loadSeasons(seasonId)

    def seasonsLoaded(self,seasons: List[Season]):
        self._loadingSeasons = False
        if seasons:
            self._seasons.clear()
            self._seasons.appendRow(*seasons)
        self.seasonsLoadingFinished.emit()

    def loadEpisodes(self,seasonRow: int):
        if self._loadingEpisodes: return
        index: QModelIndex = self._seasons.index(seasonRow,2)
        seasonId: Optional[str] = self._seasons.data(index)
        if seasonId:
            self._loadingEpisodes = True
            self._sol.loadEpisodes(seasonId)

    def episodesLoaded(self,episodes: List[Episode]):
        self._loadingEpisodes = False
        if episodes:
            self._episodes.clear()
            self._episodes.appendRow(*episodes)
        self.episodesLoadingFinished.emit()

    def loadServers(self,row: int = 0):
        if self._loadingServers: return
        filmUrlSplit = self._filmUrl.rsplit("/",2)
        if len(filmUrlSplit) < 1:
            return
        if  filmUrlSplit[-2] == "tv":
            index: QModelIndex = self._episodes.index(row,3)
            episodeId: Any = self._episodes.data(index)
            if isinstance(episodeId,str):
                self._sol.loadEpisodeServers(episodeId)
        else:
            movieId: str = filmUrlSplit[-1].rsplit("-",1)[-1]
            self._sol.loadMovieServers(movieId)

    def loadVideo(self,server: VideoServer):
        self._sol.loadVideo(server)


