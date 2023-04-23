from typing import Optional
from PyQt6.QtCore import QObject
from ....provider.models.filmlist import QFilmListModel
from ...sol import Page, PageInfo, QSol

class QSolShowsViewModel(QObject):
    
    def __init__(self,parent: Optional[QObject] = None):
        super().__init__(parent=parent)
        self._sol: QSol = QSol(self)
        self._shows: QFilmListModel = QFilmListModel(self)

        self._loadingShows: bool = False

        self._showsPageInfo: PageInfo = PageInfo(0,1,True)

        self._sol.showsLoaded.connect(self.showsLoaded)
        self._shows.fetchMoreRequest.connect(self.loadShows)

    @property
    def shows(self):
        return self._shows

    def loadShows(self):
        if self._loadingShows or not self._showsPageInfo.hasNextPage:
            return
        self._loadingShows = True
        self._sol.loadShows(self._showsPageInfo.currentPage + 1)

    def showsLoaded(self,page: Page):
        self._loadingShows = False
        self._showsPageInfo = page.pageInfo
        if len(page.films) > 0:
            self._shows.appendRow(*page.films)
