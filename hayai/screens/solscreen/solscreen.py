from typing import Optional

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QStackedWidget, QWidget
from ..screen import QScreen
from .solhomescreen import QSolHomeScreen
from .solmoviesscreen import QSolMoviesScreen
from .solimdbscreen import QSolImdbScreen
from .solshowsscreen import QSolShowsScreen
from .solfilmdetailscreen import QSolFilmDetailScreen
from hayai.features.sol.widgets.solsidebar import QSolSidebar


class QSolScreen(QScreen):

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        self.sidebar: QSolSidebar = QSolSidebar()
        self.main: QStackedWidget = QStackedWidget()
        
        self.sidebar.homeButtonClicked.connect(self.onHomeButtonClicked)
        self.sidebar.moviesButtonClicked.connect(self.onMoviesButtonClicked)
        self.sidebar.showsButtonClicked.connect(self.onShowsButtonClicked)
        self.sidebar.imdbButtonClicked.connect(self.onImdbButtonClicked)

        solScreenLayout: QHBoxLayout = QHBoxLayout()
        solScreenLayout.addWidget(self.sidebar)
        solScreenLayout.addWidget(self.main)
        solScreenLayout.setContentsMargins(0,0,0,0)
        solScreenLayout.setSpacing(0)
        self.setLayout(solScreenLayout)

    def onStart(self):
        home: QSolHomeScreen = QSolHomeScreen()
        self.window().setWindowTitle(home.title)
        home.onStart()
        self.main.addWidget(home)
        """
        filmDetail: QSolFilmDetailScreen = QSolFilmDetailScreen()
        self.window().setWindowTitle(filmDetail.title)
        filmDetail.onStart()
        self.main.addWidget(filmDetail)
        """
        return super().onStart()

    def onSearchButtonClicked(self):
        pass
    def onHomeButtonClicked(self):
        if not isinstance(self.main.currentWidget(),QSolHomeScreen):
            screen: QScreen = QSolHomeScreen()
            self.window().setWindowTitle(screen.title)
            index: int = self.main.addWidget(screen)
            screen.onStart()
            self.main.setCurrentIndex(index)

    def onMoviesButtonClicked(self):
        if not isinstance(self.main.currentWidget(),QSolMoviesScreen):
            screen: QScreen = QSolMoviesScreen()
            self.window().setWindowTitle(screen.title)
            index: int = self.main.addWidget(screen)
            screen.onStart()
            self.main.setCurrentIndex(index)
    def onShowsButtonClicked(self):
        if not isinstance(self.main.currentWidget(),QSolShowsScreen):
            screen: QScreen = QSolShowsScreen()
            self.window().setWindowTitle(screen.title)
            index: int = self.main.addWidget(screen)
            screen.onStart()
            self.main.setCurrentIndex(index)

    def onImdbButtonClicked(self):
        if not isinstance(self.main.currentWidget(),QSolImdbScreen):
            screen: QScreen = QSolImdbScreen()
            self.window().setWindowTitle(screen.title)
            index: int = self.main.addWidget(screen)
            screen.onStart()
            self.main.setCurrentIndex(index)
    def onBackButtonClicked(self):
        if self.main.count() > 1:
            screen: QWidget = self.main.currentWidget()
            self.main.removeWidget(screen)
            if isinstance(screen, QScreen):
                screen.onDestroy()
            screen.deleteLater()
            currentWidget: QWidget = self.main.currentWidget()
            if isinstance(currentWidget, QScreen):
                self.window().setWindowTitle(currentWidget.title)
