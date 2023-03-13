from typing import Optional

from PyQt5.QtWidgets import (
    QAbstractButton,
    QFrame,
    QScrollArea,
    QSizePolicy,
    QStackedLayout,
    QWidget,
    QMainWindow,
    QDockWidget,
)
from PyQt5.QtCore import Qt
from provider_parsers import Sol

from hayai.widgets import QSidebar
from hayai.widgets import QHeader

from ..category import QCategory
from ..home  import QHome
from ..search import QSearch

class QWindow(QMainWindow):

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__()

        self.header: QHeader = QHeader()

        self.sidebar: QSidebar = QSidebar(Sol)

        self.category: QCategory = QCategory(Sol)

        self.home: QHome = QHome(Sol)

        self.search: QSearch = QSearch(Sol)

        mainFrame: QFrame = QFrame()
        mainFrame.setObjectName("QMainFrame")


        scrollArea = QScrollArea()
        scrollArea.setObjectName("scroll-area")
        scrollArea.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        
        scrollArea.setWidget(self.home)
        scrollArea.horizontalScrollBar().setEnabled(False)
        scrollArea.verticalScrollBar().setEnabled(True)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setWidgetResizable(True)
        scrollArea.setContentsMargins(0,0,0,0)


        sidebarDock: QDockWidget = QDockWidget()
        sidebarDock.setWidget(self.sidebar)
        sidebarDock.setTitleBarWidget(QWidget())

        headerDock: QDockWidget = QDockWidget()
        headerDock.setWidget(self.header)
        headerDock.setTitleBarWidget(QWidget())

        self.sidebar.categoryButtonToggled.connect(self.loadCategory)
        self.sidebar.menuButtonToggled.connect(self.loadCategory)
        self.sidebar.homeButtonToggle.connect(self.loadHome)
        self.sidebar.lineEditFocusGained.connect(self.loadSearch)
        self.sidebar.lineEditTextChanged.connect(self.search.search)

        

        self.mainFrameLayout: QStackedLayout = QStackedLayout()
        self.mainFrameLayout.addWidget(scrollArea)
        self.mainFrameLayout.addWidget(self.category)
        self.mainFrameLayout.addWidget(self.search)
        self.mainFrameLayout.setContentsMargins(5,0,0,0)
        self.mainFrameLayout.setSpacing(0)
        self.mainFrameLayout.setCurrentIndex(0)
        mainFrame.setLayout(self.mainFrameLayout)

        self.setCentralWidget(mainFrame)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,sidebarDock)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea,headerDock)
        self.setCorner(Qt.Corner.TopLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setContentsMargins(0,0,0,0)
        self.setObjectName("window")
        self.setWindowTitle("Hayai")
        self.loadStylesheet()

    def loadHome(self):
        self.mainFrameLayout.setCurrentIndex(0)
        self.header.setCurrentScreenTitle("Home")

    def loadCategory(self,button: QAbstractButton):
        self.category.load(button)
        self.header.setCurrentScreenTitle(button.text())
        self.mainFrameLayout.setCurrentIndex(1)

    def loadSearch(self):
        self.header.setCurrentScreenTitle("Search")
        self.mainFrameLayout.setCurrentIndex(2)

    def loadStylesheet(self):
        with open("hayai/screens/window/window.qss","r") as f:
            self.setStyleSheet(f.read())
        
