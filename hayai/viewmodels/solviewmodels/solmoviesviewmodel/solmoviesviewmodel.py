
from typing import Optional
from PyQt6.QtCore import QObject
from hayai.providers import QSol
from hayai.models.filmlist import QFilmListModel
from hayai.providers.provider import Page, PageInfo

class QSolMoviesViewModel(QObject):
    
    def __init__(self,parent: Optional[QObject] = None):
        super().__init__(parent=parent)
        self._sol: QSol = QSol(self)
        self._movies: QFilmListModel = QFilmListModel(self)

        self._loadingMovies: bool = False

        self._moviesPageInfo: PageInfo = PageInfo(0,1,True)

        self._sol.moviesLoaded.connect(self.moviesLoaded)
        self._movies.fetchMoreRequest.connect(self.loadMovies)

    @property
    def movies(self):
        return self._movies

    def loadMovies(self):
        if self._loadingMovies or not self._moviesPageInfo.hasNextPage:
            return
        self._loadingMovies = True
        self._sol.loadMovies(self._moviesPageInfo.currentPage + 1)

    def moviesLoaded(self,page: Page):
        self._loadingMovies = False
        self._moviesPageInfo = page.pageInfo
        if len(page.films) > 0:
            self._movies.appendRow(*page.films)

