
from typing import Optional

from PyQt6.QtCore import QModelIndex, Qt, pyqtSignal
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QSizePolicy, QVBoxLayout
from PyQt6.QtWidgets import QWidget

from ...screen import QScreen
from hayai.viewmodels.solviewmodels import QSolHomeViewModel
from hayai.widgets.filmrow import QFilmRow


class QSolHomeScreen(QScreen):

    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)
    def __init__(self, parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)
        self._homeViewModel: QSolHomeViewModel = QSolHomeViewModel(self)

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

        trendingMoviesRow: QFilmRow = QFilmRow("trending movies",self._homeViewModel.trendingMovies)
        trendingShowsRow: QFilmRow = QFilmRow("trending shows",self._homeViewModel.trendingShows)
        latestMoviesRow: QFilmRow = QFilmRow("latest movies",self._homeViewModel.latestMovies)
        latestShowsRow: QFilmRow = QFilmRow("latest shows",self._homeViewModel.latestShows)
        comingSoonRow: QFilmRow = QFilmRow("coming soon",self._homeViewModel.comingSoon)

        self.started.connect(self._homeViewModel.loadHome)

        scrollAreaFrameLayout: QVBoxLayout = QVBoxLayout()
        scrollAreaFrameLayout.addWidget(trendingMoviesRow)
        scrollAreaFrameLayout.addWidget(trendingShowsRow)
        scrollAreaFrameLayout.addWidget(latestMoviesRow)
        scrollAreaFrameLayout.addWidget(latestShowsRow)
        scrollAreaFrameLayout.addWidget(comingSoonRow)
        scrollAreaFrameLayout.setContentsMargins(0,0,0,0)
        scrollAreaFrameLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scrollAreaFrameLayout.setSpacing(0)
        scrollAreaFrame.setLayout(scrollAreaFrameLayout)

        homeLayout: QHBoxLayout = QHBoxLayout()
        homeLayout.addWidget(scrollArea)
        homeLayout.setContentsMargins(0,0,0,0)
        homeLayout.setSpacing(0)
        self.setLayout(homeLayout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
        self.title = "Home"

