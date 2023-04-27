from typing import Optional
from PyQt6.QtCore import QModelIndex

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QStackedWidget, QWidget
from ..screen import QScreen
from ..playerscreen import QPlayer
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
        home.filmClicked.connect(self.onFilmclicked)
        self.main.addWidget(home)
        """
        url: str = "https://solarmovie.pe/tv/watch-dead-ringers-free-95773"
        filmDetail: QSolFilmDetailScreen = QSolFilmDetailScreen(url)
        self.window().setWindowTitle(filmDetail.title)
        filmDetail.onStart()
        self.main.addWidget(filmDetail)
        """
        #player: QPlayer = QPlayer()
        #self.main.addWidget(player)
        return super().onStart()

    def onSearchButtonClicked(self):
        pass
    def onFilmclicked(self,index: QModelIndex):
        filmUrl: Optional[str] = index.siblingAtColumn(1).data()
        if filmUrl is not None:
            currentScreen: QWidget = self.main.currentWidget()
            if isinstance(currentScreen, QScreen):
                currentScreen.onStop()
            if isinstance(currentScreen,QPlayer):
                self.main.removeWidget(currentScreen)
                currentScreen.onDestroy()
                currentScreen.deleteLater()
            filmDetail: QSolFilmDetailScreen = QSolFilmDetailScreen(filmUrl)
            filmDetail.filmClicked.connect(self.onFilmclicked)
            filmDetail.playMedia.connect(self.onPlayMedia)
            self.window().setWindowTitle(filmDetail.title)
            filmDetail.onStart()
            filmDetailIndex: int = self.main.addWidget(filmDetail)
            self.main.setCurrentIndex(filmDetailIndex)

    def onHomeButtonClicked(self):
        if not isinstance(self.main.currentWidget(),QSolHomeScreen):
            currentScreen: QWidget = self.main.currentWidget()
            if isinstance(currentScreen, QScreen):
                currentScreen.onStop()
            if isinstance(currentScreen,QPlayer):
                self.main.removeWidget(currentScreen)
                currentScreen.onDestroy()
                currentScreen.deleteLater()
            screen: QScreen = QSolHomeScreen()
            screen.filmClicked.connect(self.onFilmclicked)
            self.window().setWindowTitle(screen.title)
            index: int = self.main.addWidget(screen)
            screen.onStart()
            self.main.setCurrentIndex(index)

    def onMoviesButtonClicked(self):
        if not isinstance(self.main.currentWidget(),QSolMoviesScreen):
            currentScreen: QWidget = self.main.currentWidget()
            if isinstance(currentScreen, QScreen):
                currentScreen.onStop()
            if isinstance(currentScreen,QPlayer):
                self.main.removeWidget(currentScreen)
                currentScreen.onDestroy()
                currentScreen.deleteLater()
            screen: QScreen = QSolMoviesScreen()
            screen.filmClicked.connect(self.onFilmclicked)
            self.window().setWindowTitle(screen.title)
            index: int = self.main.addWidget(screen)
            screen.onStart()
            self.main.setCurrentIndex(index)
    def onShowsButtonClicked(self):
        if not isinstance(self.main.currentWidget(),QSolShowsScreen):
            currentScreen: QWidget = self.main.currentWidget()
            if isinstance(currentScreen, QScreen):
                currentScreen.onStop()
            if isinstance(currentScreen,QPlayer):
                self.main.removeWidget(currentScreen)
                currentScreen.onDestroy()
                currentScreen.deleteLater()
            screen: QScreen = QSolShowsScreen()
            screen.filmClicked.connect(self.onFilmclicked)
            self.window().setWindowTitle(screen.title)
            index: int = self.main.addWidget(screen)
            screen.onStart()
            self.main.setCurrentIndex(index)

    def onImdbButtonClicked(self):
        if not isinstance(self.main.currentWidget(),QSolImdbScreen):
            currentScreen: QWidget = self.main.currentWidget()
            if isinstance(currentScreen, QScreen):
                currentScreen.onStop()
            if isinstance(currentScreen,QPlayer):
                self.main.removeWidget(currentScreen)
                currentScreen.onDestroy()
                currentScreen.deleteLater()
            screen: QScreen = QSolImdbScreen()
            screen.filmClicked.connect(self.onFilmclicked)
            self.window().setWindowTitle(screen.title)
            index: int = self.main.addWidget(screen)
            screen.onStart()
            self.main.setCurrentIndex(index)
    def onBackButtonClicked(self):
        if self.main.count() > 1:
            screen: QWidget = self.main.currentWidget()
            self.main.removeWidget(screen)
            if isinstance(screen, QScreen):
                screen.onStop()
                screen.onDestroy()
            screen.deleteLater()
            currentWidget: QWidget = self.main.currentWidget()
            if isinstance(currentWidget, QScreen):
                self.window().setWindowTitle(currentWidget.title)

    def onPlayMedia(self,mediaUrl: str):
        currentScreen: QWidget = self.main.currentWidget()
        if isinstance(currentScreen, QScreen):
            currentScreen.onStop()
        if isinstance(currentScreen,QPlayer):
            self.main.removeWidget(currentScreen)
            currentScreen.onDestroy()
            currentScreen.deleteLater()

        player: QPlayer = QPlayer(mediaUrl,self)
        index: int = self.main.addWidget(player)
        self.main.setCurrentIndex(index)
        self.window().setWindowTitle(player.title)
