
from typing import Optional
from PyQt6.QtCore import QObject
from ....provider.models.filmlist import QFilmListModel
from ....provider.models.filminfoitem import QFilmInfoItemModel
from ...sol import Page, PageInfo, QSol, FilmInfo

class QSolFilmDetailViewModel(QObject):
    
    def __init__(self,filmUrl: str = "",parent: Optional[QObject] = None):
        super().__init__(parent=parent)
        self._sol: QSol = QSol(self)
        self._filmInfo: QFilmInfoItemModel = QFilmInfoItemModel()
        self._filmRecomendation: QFilmListModel = QFilmListModel()
        self._loadingFilmInfo: bool = False
        self._filmUrl = filmUrl;
        self._sol.filmInfoLoaded.connect(self.filmInfoLoaded)

    @property
    def filmInfo(self):
        return self._filmInfo

    @property
    def filmRecomendation(self):
        return self._filmRecomendation

    def loadFilmInfo(self):
        if self._loadingFilmInfo or not self._filmUrl:
            return
        self._loadingFilmInfo = True
        self._sol.loadFilmInfo(self._filmUrl)

    def filmInfoLoaded(self,filmInfo: FilmInfo):
        self._loadingFilmInfo = False
        self._filmInfo.setItem(filmInfo)
        if len(filmInfo.recommendation) > 0:
            self._filmRecomendation.clear()
            self._filmRecomendation.appendRow(*filmInfo.recommendation)

