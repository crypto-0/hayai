from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtCore import pyqtSignal
from .widgets import QNav
from .widgets import QProviderList
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout
)
class QSidebar(QFrame):
    menuButtonClicked: pyqtSignal = pyqtSignal(str)
    categoryButtonClicked: pyqtSignal = pyqtSignal(str)
    libraryButtonClicked: pyqtSignal = pyqtSignal(str)
    generalButtonClicked: pyqtSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        leftFrame: QFrame = QFrame()
        leftFrame.setObjectName("left")

        rightFrame: QFrame = QFrame()
        rightFrame.setObjectName("right")

        
        providerNav: QProviderList = QProviderList(["sol","zoro","asian"])
        menuNav: QNav = QNav("menu",["home","movies","tv shows"])
        librayNav: QNav = QNav("library",["downloads"])
        categoryNav: QNav = QNav("category",["latest","trending","coming soon"])
        generalNav: QNav = QNav("general",["setting"])


        leftFrameLayout: QVBoxLayout = QVBoxLayout()
        leftFrameLayout.addWidget(providerNav)
        leftFrameLayout.setContentsMargins(0,20,0,20)
        leftFrameLayout.setSpacing(0)
        leftFrame.setLayout(leftFrameLayout)

        rightFrameLayout: QVBoxLayout = QVBoxLayout()
        rightFrameLayout.addWidget(menuNav)
        rightFrameLayout.addWidget(librayNav)
        rightFrameLayout.addWidget(categoryNav)
        rightFrameLayout.addWidget(generalNav)
        rightFrameLayout.setContentsMargins(0,20,0,20)
        rightFrameLayout.setSpacing(5)
        rightFrame.setLayout(rightFrameLayout)

        sidebarLayout: QHBoxLayout = QHBoxLayout()
        sidebarLayout.addWidget(leftFrame,1)
        sidebarLayout.addWidget(rightFrame,3)
        sidebarLayout.setContentsMargins(0,0,0,0)
        sidebarLayout.setSpacing(0)
        self.setLayout(sidebarLayout)

        self.setFixedWidth(250)
        self.setObjectName("QSidebar")
        


