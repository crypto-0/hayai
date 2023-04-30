from typing import Optional
from PyQt6.QtCore import QObject

from ....provider.models.filmlist import QFilmListModel
from ...sol import Page, PageInfo, QSol

class QSolMoviesViewModel(QObject):
    
    def __init__(self,parent: Optional[QObject] = None):
        super().__init__(parent=parent)
        self._sol: QSol = QSol(self)
        self._movies: QFilmListModel = QFilmListModel(self)

        self._loadingMovies: bool = False

        self._moviesPageInfo: PageInfo = PageInfo(0,1,True)

        self._sol.moviesLoaded.connect(self.moviesLoaded)
        self._movies.fetchMoreRequest.connect(self.loadNext)

    @property
    def movies(self):
        return self._movies

    def loadMovies(self):
        self._moviesPageInfo = PageInfo(0,1,True)
        self._movies.clear()
        self._loadingMovies = False
        self.loadNext()

    def loadNext(self):
        if self._loadingMovies or not self._moviesPageInfo.hasNextPage:
            return
        self._loadingMovies = True
        self._sol.loadMovies(self._moviesPageInfo.currentPage + 1)

    def moviesLoaded(self,page: Page):
        self._loadingMovies = False
        self._moviesPageInfo = page.pageInfo
        if len(page.films) > 0:
            self._movies.appendRow(*page.films)

