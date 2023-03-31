from typing import Optional

from PyQt6.QtWidgets import (
    QAbstractButton,
    QFrame,
    QStackedLayout,
    QWidget,
    QMainWindow,
    QDockWidget,
)
from PyQt6.QtCore import QModelIndex, Qt
from provider_parsers import Sol

from hayai.features.widgets.sidebar import QSidebar

from ..category import QCategory
from ..home  import QHome
from ..search import QSearch
from ..filmdetail import QFilmDetail

class QWindow(QMainWindow):

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__()

        self.sidebar: QSidebar = QSidebar(Sol,parent=self)

        self.filmDetail: QFilmDetail = QFilmDetail(Sol,parent=self)

        self.category: QCategory = QCategory(Sol,parent=self)

        self.home: QHome = QHome(Sol,parent=self)

        self.search: QSearch = QSearch(Sol,parent=self)

        mainFrame: QFrame = QFrame()
        mainFrame.setObjectName("QMainFrame")
        #self.player: QPlayer = QPlayer(mainFrame.winId())

        sidebarDock: QDockWidget = QDockWidget()
        sidebarDock.setWidget(self.sidebar)
        sidebarDock.setTitleBarWidget(QWidget())


        self.sidebar.categoryButtonToggled.connect(self.loadCategory)
        self.sidebar.menuButtonToggled.connect(self.loadCategory)
        self.sidebar.homeButtonToggle.connect(self.loadHome)
        self.sidebar.searchButtonToggle.connect(self.loadSearch)
        self.home.filmClicked.connect(self.loadFilmDetail)
        self.category.filmClicked.connect(self.loadFilmDetail)
        self.search.filmClicked.connect(self.loadFilmDetail)

        

        self.mainFrameLayout: QStackedLayout = QStackedLayout()
        self.mainFrameLayout.addWidget(self.home)
        self.mainFrameLayout.addWidget(self.category)
        self.mainFrameLayout.addWidget(self.search)
        self.mainFrameLayout.addWidget(self.filmDetail)
        self.mainFrameLayout.setContentsMargins(0,0,0,0)
        self.mainFrameLayout.setCurrentIndex(0)
        mainFrame.setLayout(self.mainFrameLayout)

        self.setCentralWidget(mainFrame)
        #self.setCentralWidget(self.player)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,sidebarDock)
        #self.setCorner(Qt.Corner.TopLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setContentsMargins(0,0,0,0)
        self.setObjectName("window")
        self.setWindowTitle("Hayai")
        self.loadStylesheet()

    def loadHome(self):
        self.mainFrameLayout.setCurrentIndex(0)

    def loadCategory(self,button: QAbstractButton):
        self.category.load(button)
        self.mainFrameLayout.setCurrentIndex(1)

    def loadSearch(self):
        self.mainFrameLayout.setCurrentIndex(2)

    def loadFilmDetail(self,index: QModelIndex):
        self.mainFrameLayout.setCurrentIndex(3)
        self.filmDetail.updateFilmDetail(index=index)
        #self.player.stop()

    def loadStylesheet(self):
        with open("hayai/screens/window/window.qss","r") as f:
            self.setStyleSheet(f.read())
        
