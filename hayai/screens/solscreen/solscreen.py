from typing import Optional

from PyQt6.QtWidgets import QAbstractButton, QHBoxLayout, QStackedWidget, QWidget

from hayai.features.sol.widgets.solsidebar import QSolSidebar

from ..screen import QScreen
from ..screen import IScreenNavigation
from .solhomescreen import QSolHomeScreen
from .solimdbscreen import QSolImdbScreen
from .solmoviesscreen import QSolMoviesScreen
from .solshowsscreen import QSolShowsScreen
from .solsearchscreen import QSolSearchScreen

class QSolScreen(QScreen,IScreenNavigation):

    def __init__(self,parent: Optional[QWidget] = None):
        super(QScreen,self).__init__(parent=parent)

        self.sidebar: QSolSidebar = QSolSidebar()
        self.main: QStackedWidget = QStackedWidget()
        
        self.sidebar.navButtonClicked.connect(self.onNavButtonClicked)

        solScreenLayout: QHBoxLayout = QHBoxLayout()
        solScreenLayout.addWidget(self.sidebar)
        solScreenLayout.addWidget(self.main)
        solScreenLayout.setContentsMargins(0,0,0,0)
        solScreenLayout.setSpacing(0)
        self.setLayout(solScreenLayout)

    def onStart(self):
        home: QSolHomeScreen = QSolHomeScreen()
        self.push(home)
        return super().onStart()


    def push(self, screen: QScreen):
        currentScreen = self.main.currentWidget()
        if isinstance(currentScreen,QScreen):
            currentScreen.onStop()
        screen.navigation = self
        screenIdx = self.main.addWidget(screen)
        self.main.setCurrentIndex(screenIdx)
        self.window().setWindowTitle(screen.title)
        screen.onStart()

    def pop(self):
        currentScreen = self.main.currentWidget()
        if isinstance(currentScreen,QScreen):
            currentScreen.onDestroy()
            currentScreen.deleteLater()
        self.main.removeWidget(currentScreen)
        currentScreen = self.main.currentWidget()
        if isinstance(currentScreen,QScreen):
            self.window().setWindowTitle(currentScreen.title)

    def popToRoot(self):
        while self.main.count() > 1:
            self.pop()

    def onBackButtonClicked(self):
        if self.main.count() > 1:
            self.pop()

    def onNavButtonClicked(self,button: QAbstractButton):
        currentScreen = self.main.currentWidget()
        if button.text().lower() == "home" and not isinstance(currentScreen,QSolHomeScreen):
            screen: QScreen = QSolHomeScreen()
            self.push(screen)
        if button.text().lower() == "movies" and not isinstance(currentScreen,QSolMoviesScreen):
            screen: QScreen = QSolMoviesScreen()
            self.push(screen)
        if button.text().lower() == "shows" and not isinstance(currentScreen,QSolShowsScreen):
            screen: QScreen = QSolShowsScreen()
            self.push(screen)
        if button.text().lower() == "imdb" and not isinstance(currentScreen,QSolImdbScreen):
            screen: QScreen = QSolImdbScreen()
            self.push(screen)

        if button.text().lower() == "search" and not isinstance(currentScreen,QSolSearchScreen):
            screen: QScreen = QSolSearchScreen()
            self.push(screen)

