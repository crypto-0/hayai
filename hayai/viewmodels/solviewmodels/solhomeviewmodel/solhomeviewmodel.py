from typing import Optional
from PyQt6.QtCore import QObject
from hayai.providers import QSol
from hayai.models.filmlist import QFilmListModel
from hayai.providers.provider import Page

class QSolHomeViewModel(QObject):
    
    def __init__(self,parent: Optional[QObject] = None):
        super().__init__(parent=parent)
        self._sol: QSol = QSol(self)
        self._trendingMovies: QFilmListModel = QFilmListModel(self)
        self._trendingShows: QFilmListModel = QFilmListModel(self)
        self._latestMovies: QFilmListModel = QFilmListModel(self)
        self._latestShows: QFilmListModel = QFilmListModel(self)
        self._comingSoon: QFilmListModel = QFilmListModel(self)

        self._loadingHome: bool = False

        self._sol.trendingMoviesLoaded.connect(self.trendingMoviesLoaded)
        self._sol.trendingShowsLoaded.connect(self.trendingShowsLoaded)
        self._sol.latestMoviesLoaded.connect(self.latestMoviesLoaded)
        self._sol.latestShowsLoaded.connect(self.latestShowsLoaded)
        self._sol.comingSoonLoaded.connect(self.comingSoonLoaded)



    @property
    def trendingMovies(self):
        return self._trendingMovies
    @property
    def trendingShows(self):
        return self._trendingShows
    @property
    def latestMovies(self):
        return self._latestMovies
    @property
    def latestShows(self):
        return self._latestShows
    @property
    def comingSoon(self):
        return self._comingSoon

    def loadHome(self):
        if self._loadingHome:
            return
        self._loadingHome = True
        self._sol.loadHome()

    def trendingMoviesLoaded(self,page: Page):
        self._loadingHome = False
        if len(page.films) > 0:
            self._trendingMovies.appendRow(*page.films)
    def trendingShowsLoaded(self,page: Page):
        self._loadingHome = False
        if len(page.films) > 0:
            self._trendingShows.appendRow(*page.films)

    def latestMoviesLoaded(self,page: Page):
        self._loadingHome = False
        if len(page.films) > 0:
            self._latestMovies.appendRow(*page.films)

    def latestShowsLoaded(self,page: Page):
        self._loadingHome = False
        if len(page.films) > 0:
            self._latestShows.appendRow(*page.films)

    def comingSoonLoaded(self,page: Page):
        self._loadingHome = False
        if len(page.films) > 0:
            self._comingSoon.appendRow(*page.films)
