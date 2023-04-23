from typing import Optional
from PyQt6.QtCore import QObject
from hayai.providers import QSol
from hayai.models.filmlist import QFilmListModel
from hayai.providers.provider import Page, PageInfo

class QSolImdbViewModel(QObject):
    
    def __init__(self,parent: Optional[QObject] = None):
        super().__init__(parent=parent)
        self._sol: QSol = QSol(self)
        self._imdb: QFilmListModel = QFilmListModel(self)

        self._loadingImdb: bool = False

        self._imdbPageInfo: PageInfo = PageInfo(0,1,True)

        self._sol.imdbLoaded.connect(self.imdbLoaded)
        self._imdb.fetchMoreRequest.connect(self.loadImdb)

    @property
    def imdb(self):
        return self._imdb

    def loadImdb(self):
        if self._loadingImdb or not self._imdbPageInfo.hasNextPage:
            return
        self._loadingImdb = True
        self._sol.loadImdb(self._imdbPageInfo.currentPage + 1)

    def imdbLoaded(self,page: Page):
        self._loadingImdb = False
        self._imdbPageInfo = page.pageInfo
        if len(page.films) > 0:
            self._imdb.appendRow(*page.films)

