from typing import Optional
from PyQt6.QtGui import QImage
from providers import Page, Provider
from providers.provider import FilmInfo
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class QProvider(QObject):
    page: pyqtSignal = pyqtSignal(Page)
    seasons: pyqtSignal = pyqtSignal(list)
    episodes: pyqtSignal = pyqtSignal(list)
    episodeServers: pyqtSignal = pyqtSignal(list)
    movieServers: pyqtSignal = pyqtSignal(list)
    filmInfo: pyqtSignal = pyqtSignal(FilmInfo)
    posterImage: pyqtSignal = pyqtSignal(QImage)

    def __init__(self,provider: Provider,parent: Optional[QObject] = None):
        super().__init__(parent=parent)
        self._provider = provider

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self,provider: Provider):
        self._provider = provider

    @property
    def availableHomeCategories(self):
        return self._provider.available_home_categories

    @property
    def availableGeneralCategories(self):
        return self._provider.available_general_categories


    @pyqtSlot(str,int)
    def search(self,query: str, pageNumber: int):
        self.page.emit(self._provider.search(query,pageNumber))

    @pyqtSlot(str,int)
    def getCategory(self,category: str,pageNumber: int = 1):
        self.page.emit(self._provider.get_category(category,pageNumber))

    @pyqtSlot(str)
    def getSeasons(self,id: str):
        self.seasons.emit(self._provider.get_seasons(id))

    @pyqtSlot(str)
    def getEpisodes(self,id: str):
        self.episodes.emit(self._provider.get_episodes(id))

    @pyqtSlot(str)
    def getEpisodeServers(self,id: str):
        self.episodeServers.emit(self._provider.get_episode_servers(id))

    @pyqtSlot(str)
    def getMovieServers(self,id: str):
        self.movieServers.emit(self._provider.get_movie_servers(id))

    @pyqtSlot(str)
    def getFilmInfo(self,url: str):
        self.filmInfo.emit(self._provider.get_film_info(url))

    @pyqtSlot(str)
    def getPosterImage(self,url: str):
        image: QImage = QImage()
        image.loadFromData(self._provider.get_poster_image(url)) #pyright: ignore
        self.posterImage.emit(image)

