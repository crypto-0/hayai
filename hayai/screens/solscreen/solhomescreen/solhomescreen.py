from typing import Optional

from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QSizePolicy, QVBoxLayout
from PyQt6.QtWidgets import QWidget

from ...screen import QScreen
from ..solfilmdetailscreen import QSolFilmDetailScreen
from hayai.features.sol.viewmodels import QSolHomeViewModel
from hayai.features.provider.delegates.filmdelegate import QFilmDelegate
from hayai.features.widgets.rowview import  QRowView


class QSolHomeScreen(QScreen):

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

        trendingMoviesRow: QRowView = QRowView("trending movies",self._homeViewModel.trendingMovies,QFilmDelegate())
        trendingShowsRow: QRowView = QRowView("trending shows",self._homeViewModel.trendingShows,QFilmDelegate())
        latestMoviesRow: QRowView = QRowView("latest movies",self._homeViewModel.latestMovies,QFilmDelegate())
        latestShowsRow: QRowView = QRowView("latest shows",self._homeViewModel.latestShows,QFilmDelegate())
        comingSoonRow: QRowView = QRowView("coming soon",self._homeViewModel.comingSoon,QFilmDelegate())

        self.started.connect(self._homeViewModel.loadHome)
        trendingMoviesRow.itemClicked.connect(self.onFilmClicked)
        trendingShowsRow.itemClicked.connect(self.onFilmClicked)
        latestMoviesRow.itemClicked.connect(self.onFilmClicked)
        latestShowsRow.itemClicked.connect(self.onFilmClicked)
        comingSoonRow.itemClicked.connect(self.onFilmClicked)

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

    def onFilmClicked(self,index: QModelIndex):
        filmUrl: Optional[str] = index.siblingAtColumn(1).data()
        if filmUrl is not None and self.navigation is not None:
            screen: QScreen = QSolFilmDetailScreen(filmUrl)
            self.navigation.push(screen)

