from typing import Optional

from PyQt5.QtWidgets import (
    QAbstractButton,
    QFrame,
    QGridLayout,
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

from ..category.category import QCategory
from ..home.home import QHome

class QWindow(QMainWindow):

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__()

        self.header: QHeader = QHeader()

        self.sidebar: QSidebar = QSidebar()

        self.category: QCategory = QCategory(Sol)

        self.home: QHome = QHome(Sol)

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

        self.sidebar.categoryButtonToggled.connect(self.loadCategory)
        self.sidebar.menuButtonToggled.connect(self.loadCategory)
        self.sidebar.homeButtonToggle.connect(self.loadHome)

        sidebarDock: QDockWidget = QDockWidget()
        sidebarDock.setWidget(self.sidebar)
        sidebarDock.setTitleBarWidget(QWidget())

        headerDock: QDockWidget = QDockWidget()
        headerDock.setWidget(self.header)
        headerDock.setTitleBarWidget(QWidget())

        self.mainFrameLayout: QStackedLayout = QStackedLayout()
        self.mainFrameLayout.addWidget(scrollArea)
        self.mainFrameLayout.addWidget(self.category)
        self.mainFrameLayout.setContentsMargins(5,0,0,0)
        self.mainFrameLayout.setSpacing(0)
        self.mainFrameLayout.setCurrentIndex(0)
        mainFrame.setLayout(self.mainFrameLayout)

        """
        windowLayout: QGridLayout = QGridLayout()
        windowLayout.addWidget(self.sidebar,0,0,1,1)
        windowLayout.addWidget(mainFrame,0,1,1,1)
        windowLayout.setSpacing(0)
        windowLayout.setContentsMargins(0,0,0,0)
        self.setLayout(windowLayout)
        """

        #self.setFixedSize(800,700)
        self.setCentralWidget(mainFrame)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,sidebarDock)
       # self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea,headerDock)
        self.setCorner(Qt.Corner.TopLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setContentsMargins(0,0,0,0)
        self.setObjectName("window")
        self.setWindowTitle("Hayai")
        self.loadStylesheet()

    def loadHome(self):
        self.mainFrameLayout.setCurrentIndex(0)
    def loadCategory(self,button: QAbstractButton):
        self.category.load(button)
        self.mainFrameLayout.setCurrentIndex(1)

    def loadStylesheet(self):
        with open("hayai/screens/window/window.qss","r") as f:
            self.setStyleSheet(f.read())
        
