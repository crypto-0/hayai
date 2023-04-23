
from typing import Optional

from PyQt6.QtCore import QModelIndex, Qt, pyqtSignal
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDataWidgetMapper,
    QFrame,
    QHBoxLayout,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
)
from PyQt6.QtWidgets import QWidget

from hayai.features.provider.widgets.film import QFilmDetail
from hayai.features.provider.widgets.film import QFilmDescription
from hayai.features.provider.widgets.film import QFilmPoster
from hayai.features.sol.viewmodels import QSolFilmDetailViewModel

from ...screen import QScreen


class QSolFilmDetailScreen(QScreen):

    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)
    def __init__(self, parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)
        self._filmDetailViewModel: QSolFilmDetailViewModel = QSolFilmDetailViewModel()

        scrollAreaFrame: QFrame = QFrame()

        scrollArea = QScrollArea()
        scrollArea.setObjectName("scroll-area")
        scrollArea.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        
        scrollArea.setWidget(scrollAreaFrame)
        scrollArea.horizontalScrollBar().setEnabled(False)
        scrollArea.verticalScrollBar().setEnabled(True)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setWidgetResizable(True)
        scrollArea.setContentsMargins(0,0,0,0)

        leftFrame: QFrame = QFrame()
        leftFrame.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.MinimumExpanding)
        rightFrame: QFrame = QFrame()
        overviewFrame: QFrame = QFrame()

        self.poster: QFilmPoster = QFilmPoster()
        filmDescription: QFilmDescription = QFilmDescription()
        filmDetail: QFilmDetail = QFilmDetail()

        self.widgetMapper: QDataWidgetMapper = QDataWidgetMapper()
        self.widgetMapper.setModel(self._filmDetailViewModel.filmInfo)
        self.widgetMapper.addMapping(filmDescription.titleLabel,0,b"text") #pyright: ignore
        self.widgetMapper.addMapping(filmDescription.descriptionLabel,2,b"text") #pyright: ignore
        self.widgetMapper.addMapping(self.poster,6,b"pixmap") #pyright: ignore
        self.widgetMapper.toFirst()



        self.started.connect(self._filmDetailViewModel.loadFilmInfo)

        leftFrameLayout: QVBoxLayout = QVBoxLayout()
        leftFrameLayout.addWidget(self.poster)
        leftFrameLayout.addStretch()
        leftFrameLayout.setContentsMargins(0,0,0,0)
        leftFrameLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        leftFrame.setLayout(leftFrameLayout)

        rightFrameLayout: QVBoxLayout = QVBoxLayout()
        rightFrameLayout.addWidget(filmDescription)
        rightFrameLayout.addWidget(filmDetail)
        rightFrameLayout.setContentsMargins(30,20,5,0)
        rightFrameLayout.setSpacing(10)
        rightFrame.setLayout(rightFrameLayout)

        overviewLayout: QHBoxLayout = QHBoxLayout()
        overviewLayout.addWidget(leftFrame)
        overviewLayout.addWidget(rightFrame)
        overviewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        overviewLayout.setContentsMargins(0,0,0,0)
        overviewLayout.setSpacing(5)
        overviewFrame.setLayout(overviewLayout)

        scrollAreaFrameLayout: QVBoxLayout = QVBoxLayout()
        scrollAreaFrameLayout.addWidget(overviewFrame)
        scrollAreaFrameLayout.setContentsMargins(0,0,0,0)
        scrollAreaFrameLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scrollAreaFrameLayout.setSpacing(0)
        scrollAreaFrame.setLayout(scrollAreaFrameLayout)

        filmDetailLayout: QHBoxLayout = QHBoxLayout()
        filmDetailLayout.addWidget(scrollArea)
        filmDetailLayout.setContentsMargins(0,0,0,0)
        filmDetailLayout.setSpacing(0)
        self.setLayout(filmDetailLayout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
        self.title = "FilmDetail"

