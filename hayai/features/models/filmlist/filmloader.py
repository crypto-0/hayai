from collections.abc import Iterator
from typing import List, Optional
from PyQt6.QtCore import  QObject, pyqtSignal, pyqtSlot
from provider_parsers import Film
from datetime import datetime

class QFilmLoader(QObject):
    filmsLoaded: pyqtSignal = pyqtSignal(list,datetime)
    generatorChanged: pyqtSignal = pyqtSignal()
    noMoreFilms: pyqtSignal = pyqtSignal()

    def __init__(self,generator: Optional[Iterator[Film]] = None, batch: int = 32,parent:Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.batch: int = batch
        self.generator: Optional[Iterator[Film]] = generator
        self.canceled: bool = False

    @pyqtSlot(datetime)
    def loadNext(self,timeStamp: datetime ):
        if self.generator is None:
            self.noMoreFilms.emit()
            return

        films: List[Film] = []
        try:
            for _ in range(self.batch):
                film: Film = next(self.generator)
                films.append(film)
                if self.canceled:
                    self.canceled = False
                    return
        except StopIteration:
            self.noMoreFilms.emit()

        self.filmsLoaded.emit(films,timeStamp)

    @pyqtSlot(object)
    def setGenerator(self,generator: Iterator):
        self.generator = generator
        self.canceled = False
        self.generatorChanged.emit()

    def cancel(self):
        self.canceled = True
