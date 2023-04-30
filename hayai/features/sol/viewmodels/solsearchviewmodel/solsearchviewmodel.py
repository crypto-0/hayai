from typing import Optional
from PyQt6.QtCore import QObject

from ....provider.models.filmlist import QFilmListModel
from ...sol import Page, PageInfo, QSol

class QSolSearchViewModel(QObject):
    
    def __init__(self,parent: Optional[QObject] = None):
        super().__init__(parent=parent)
        self._sol: QSol = QSol(self)
        self._queriedFilms: QFilmListModel = QFilmListModel(self)

        self._searching: bool = False
        self._searchQuery: str = ""

        self._searchPageInfo: PageInfo = PageInfo(0,1,True)

        self._sol.searchLoaded.connect(self.searchLoaded)
        self._queriedFilms.fetchMoreRequest.connect(self.loadNext)

    @property
    def queriedFilms(self):
        return self._queriedFilms

    def loadSearch(self,query: str):
        self._searchQuery = query
        self._searchPageInfo: PageInfo = PageInfo(0,1,True)
        self._queriedFilms.clear()
        self._searching = False
        self._sol.abort()
        self.loadNext()

    def loadNext(self):
        if self._searching or not self._searchPageInfo.hasNextPage:
            return
        self._searching = True
        self._sol.loadSearch(self._searchQuery,self._searchPageInfo.currentPage + 1)

    def searchLoaded(self,page: Page):
        self._searching = False
        self._searchPageInfo = page.pageInfo
        if len(page.films) > 0:
            self._queriedFilms.appendRow(*page.films)

