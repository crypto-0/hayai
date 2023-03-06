from typing import Optional

from PyQt5.QtWidgets import (
    QAbstractButton,
    QFrame,
    QGridLayout,
    QScrollArea,
    QSizePolicy,
    QStackedLayout,
    QWidget,
)
from provider_parsers import Sol

from hayai.widgets import QSidebar

from ..browse.browse import QBrowse
from ..home.home import QHome

class QWindow(QWidget):

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__()

        sidebar: QSidebar = QSidebar()

        browse: QBrowse = QBrowse(Sol)

        home: QHome = QHome(Sol)

        mainFrame: QFrame = QFrame()


        scrollArea = QScrollArea()
        scrollArea.setObjectName("scroll-area")
        scrollArea.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        
        scrollArea.setWidget(home)
        scrollArea.horizontalScrollBar().setEnabled(True)
        scrollArea.verticalScrollBar().setEnabled(True)
        scrollArea.setWidgetResizable(True)

        sidebar.categoryButtonToggled.connect(browse.browseCategory)
        sidebar.categoryButtonToggled.connect(self.changeScreen)
        sidebar.menuButtonToggled.connect(self.changeScreen)
        sidebar.menuButtonToggled.connect(browse.browseCategory)

        self.mainFrameLayout: QStackedLayout = QStackedLayout()
        self.mainFrameLayout.addWidget(scrollArea)
        self.mainFrameLayout.addWidget(browse)
        self.mainFrameLayout.setCurrentIndex(0)
        mainFrame.setLayout(self.mainFrameLayout)

        windowLayout: QGridLayout = QGridLayout()
        windowLayout.addWidget(sidebar,0,0,1,1)
        windowLayout.addWidget(mainFrame,0,1,1,1)
        windowLayout.setSpacing(0)
        windowLayout.setContentsMargins(0,0,0,0)
        self.setLayout(windowLayout)

        #self.setMaximumSize(1920,1080)
        self.setFixedSize(800,700)
        self.setObjectName("window")
        self.setWindowTitle("Hayai")
        self.loadStylesheet()

    def changeScreen(self,button: QAbstractButton):
        if button.text().lower() == "home":
            self.mainFrameLayout.setCurrentIndex(0)
        else:
            self.mainFrameLayout.setCurrentIndex(1)


    def loadStylesheet(self):
        with open("hayai/screens/window/window.qss","r") as f:
            self.setStyleSheet(f.read())
        
