
from collections.abc import Iterator
from typing import List, Optional
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from provider_parsers import Film


class QFilmGeneratorWorker(QObject):
    result: pyqtSignal = pyqtSignal(list)

    def __init__(self,generator: Optional[Iterator[Film]] = None, batch: int = 32,parent:Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.canceled: bool = False
        self.batch: int = batch
        self.moreFilms = True if generator is not None else False
        self.generator: Optional[Iterator[Film]] = generator

    @pyqtSlot()
    def fetchFilms(self):
        if self.generator is None or not self.moreFilms:
            return

        films: List[Film] = []
        try:
            for a in range(self.batch):
                film: Film = next(self.generator)
                films.append(film)
                if self.canceled:
                    self.canceled = False
                    return
        except StopIteration:
            self.moreFilms = False

        self.result.emit(films)

    @pyqtSlot(object)
    def setGenerator(self,generator: Iterator):
        self.generator = generator
        self.moreFilms = True if generator is not None else False
        self.canceled = False

    def cancel(self):
        self.canceled = True

    def hasMoreFilms(self):
        return self.moreFilms






