from typing import Dict, Optional

from PyQt6.QtWidgets import (
    QStackedWidget,
    QWidget,
    QMainWindow,
    QDockWidget,
)
from PyQt6.QtCore import QModelIndex, QTimer, Qt, pyqtSignal
from providers import Sol

from hayai.features.widgets.sidebar import QSidebar
from hayai.screens.screen import QScreen

from ..category import QCategory
from ..home  import QHome
from ..search import QSearch
from ..filmdetail import QFilmDetail
from ..downloads import QDownloads

class QWindow(QMainWindow):
    stopped: pyqtSignal = pyqtSignal()
    started: pyqtSignal = pyqtSignal()
    destroyed: pyqtSignal = pyqtSignal()

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__()

        self.currentProvider: Sol = Sol()
        self.screensWidget: QStackedWidget = QStackedWidget(self)
        self.screenToIndex: Dict = {}

        self.sidebar: QSidebar = QSidebar(self.currentProvider,parent=self)
        self.filmDetail: QFilmDetail = QFilmDetail(self.currentProvider,self)
        self.destroyed.connect(self.filmDetail.destroyed)
        self.screensWidget.addWidget(self.filmDetail)

        sidebarDock: QDockWidget = QDockWidget()
        sidebarDock.setWidget(self.sidebar)
        sidebarDock.setTitleBarWidget(QWidget())


        self.sidebar.categoryButtonToggled.connect(self.loadCategoryScreen)
        self.sidebar.homeButtonToggle.connect(self.loadHomeScreen)
        self.sidebar.searchButtonToggle.connect(self.loadSearchScreen)
        #self.home.filmClicked.connect(self.loadFilmDetail)
        #self.category.filmClicked.connect(self.loadFilmDetail)
        #self.search.filmClicked.connect(self.loadFilmDetail)
        self.started.connect(lambda: self.loadHomeScreen("home"))

        self.setCentralWidget(self.screensWidget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,sidebarDock)
        self.setContentsMargins(0,0,0,0)
        self.setObjectName("window")
        self.setWindowTitle("Hayai")
        self.loadStylesheet()

        #self.downloads.download()
        #self.loadHomeScreen("home")
        self.loadCategoryScreen("movie")

    def loadCategoryScreen(self,screen: str):
        currentWidget: QWidget = self.screensWidget.currentWidget()
        if isinstance(currentWidget,QScreen):
            currentWidget.onStop()
        if screen in self.screenToIndex:
            self.screensWidget.setCurrentIndex(self.screenToIndex[screen])
            nextWidget: QWidget = self.screensWidget.currentWidget()
            if isinstance(nextWidget,QScreen):
                nextWidget.onStart()
        else:
            categoryScreen: QCategory = QCategory(screen,self.currentProvider,self)
            self.destroyed.connect(categoryScreen.onDestroy)
            categoryScreen.filmClicked.connect(self.loadFilmDetail)
            idx: int = self.screensWidget.addWidget(categoryScreen)
            self.screenToIndex[screen] = idx
            self.screensWidget.setCurrentIndex(idx)
            categoryScreen.onStart()

    def loadHomeScreen(self,screen: str):
        currentWidget: QWidget = self.screensWidget.currentWidget()
        if isinstance(currentWidget,QScreen):
            currentWidget.onStop()

        if screen in self.screenToIndex:
            self.screensWidget.setCurrentIndex(self.screenToIndex[screen])
            nextWidget: QWidget = self.screensWidget.currentWidget()
            if isinstance(nextWidget,QScreen):
                nextWidget.onStart()
        else:
            homeScreen: QHome = QHome(self.currentProvider,self)
            homeScreen.filmClicked.connect(self.filmDetail.loadFilmDetails)
            self.destroyed.connect(homeScreen.onDestroy)
            idx: int = self.screensWidget.addWidget(homeScreen)
            self.screenToIndex[screen] = idx
            self.screensWidget.setCurrentIndex(idx)
            homeScreen.onStart()

    def loadSearchScreen(self,screen: str):
        currentWidget: QWidget = self.screensWidget.currentWidget()
        if isinstance(currentWidget,QScreen):
            currentWidget.onStop()

        if screen in self.screenToIndex:
            self.screensWidget.setCurrentIndex(self.screenToIndex[screen])
            nextWidget: QWidget = self.screensWidget.currentWidget()
            if isinstance(nextWidget,QScreen):
                nextWidget.onStart()
        else:
            searchScreen: QSearch = QSearch(self.currentProvider,self)
            searchScreen.filmClicked.connect(self.loadFilmDetail)
            self.destroyed.connect(searchScreen.onDestroy)
            idx: int = self.screensWidget.addWidget(searchScreen)
            self.screenToIndex[screen] = idx
            self.screensWidget.setCurrentIndex(idx)
            searchScreen.onStart()

    def loadFilmDetail(self,index: QModelIndex):

        self.screensWidget.setCurrentWidget(self.filmDetail)
        self.filmDetail.loadFilmDetails(index)
        self.filmDetail.onStart()



    def loadStylesheet(self):
        with open("hayai/screens/window/window.qss","r") as f:
            self.setStyleSheet(f.read())
        
    def onStart(self):
        self.started.emit()

    def onStop(self):
        self.stopped.emit()

    def onDestroy(self):
        self.destroyed.emit()

