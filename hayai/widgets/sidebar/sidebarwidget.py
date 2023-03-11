from typing import Dict
from PyQt5.QtCore import pyqtSignal
from .nav import QNav
from .providerlist import QProviderList
from .logo import QLogo
from .searchbar import QSearchbar
from PyQt5.QtWidgets import (
    QAbstractButton,
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QVBoxLayout
)

class QSidebar(QFrame):
    menuButtonToggled: pyqtSignal = pyqtSignal(QAbstractButton)
    categoryButtonToggled: pyqtSignal = pyqtSignal(QAbstractButton)
    libraryButtonToggled: pyqtSignal = pyqtSignal(QAbstractButton)
    generalButtonToggled: pyqtSignal = pyqtSignal(QAbstractButton)
    navButtonToggled: pyqtSignal = pyqtSignal(QAbstractButton)
    homeButtonToggle: pyqtSignal = pyqtSignal(QAbstractButton)

    def __init__(self):
        super().__init__()

        leftFrame: QFrame = QFrame()
        leftFrame.setObjectName("left")

        rightFrame: QFrame = QFrame()
        rightFrame.setObjectName("right")

        topFrame: QFrame = QFrame()
        topFrame.setObjectName("top")

        logo: QLogo = QLogo()
        searchbar: QSearchbar = QSearchbar()

        
        providerNav: QProviderList = QProviderList(["sol","zoro","asian"])
        menuNav: QNav = QNav("menu",["home","movies","tv shows"])
        librayNav: QNav = QNav("library",["downloads"])
        categoryNav: QNav = QNav("category",["latest","trending","coming soon"])
        generalNav: QNav = QNav("general",["setting"])

        self.buttonGroup: QButtonGroup = QButtonGroup()

        id: int = 0
        self.buttonSignalMapping: Dict = {}
        for idx,button in enumerate(menuNav.getNavButtons()):
            if idx == 0:
                self.buttonSignalMapping[id] = self.homeButtonToggle
            else:
                self.buttonSignalMapping[id] = self.menuButtonToggled
            self.buttonGroup.addButton(button,id)
            id +=1
        for button in librayNav.getNavButtons():
            self.buttonGroup.addButton(button,id)
            self.buttonSignalMapping[id] = self.libraryButtonToggled
            id +=1
        for button in categoryNav.getNavButtons():
            self.buttonGroup.addButton(button,id)
            self.buttonSignalMapping[id] = self.categoryButtonToggled
            id +=1
        for button in generalNav.getNavButtons():
            self.buttonGroup.addButton(button,id)
            self.buttonSignalMapping[id] = self.generalButtonToggled
            id +=1

        self.buttonGroup.buttonToggled.connect(self.buttonToggled)

        topFrameLayout: QVBoxLayout = QVBoxLayout()
        topFrameLayout.addWidget(logo)
        topFrameLayout.addWidget(searchbar)
        topFrameLayout.setContentsMargins(0,20,10,20)
        topFrameLayout.setSpacing(20)
        topFrame.setLayout(topFrameLayout)

        leftFrameLayout: QVBoxLayout = QVBoxLayout()
        leftFrameLayout.addWidget(providerNav)
        leftFrameLayout.setContentsMargins(0,20,0,20)
        leftFrameLayout.setSpacing(0)
        leftFrame.setLayout(leftFrameLayout)

        rightFrameLayout: QVBoxLayout = QVBoxLayout()
        rightFrameLayout.addWidget(topFrame,1)
        rightFrameLayout.addWidget(menuNav,2)
        rightFrameLayout.addWidget(librayNav,2)
        rightFrameLayout.addWidget(categoryNav,2)
        rightFrameLayout.addWidget(generalNav,2)
        rightFrameLayout.setContentsMargins(10,2,10,20)
        rightFrameLayout.setSpacing(5)
        #rightFrameLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        rightFrame.setLayout(rightFrameLayout)



        sidebarLayout: QHBoxLayout = QHBoxLayout()
        sidebarLayout.addWidget(leftFrame,1)
        sidebarLayout.addWidget(rightFrame,3)
        sidebarLayout.setContentsMargins(0,0,0,0)
        sidebarLayout.setSpacing(0)
        self.setLayout(sidebarLayout)

        self.setFixedWidth(250)
        self.setObjectName("QSidebar")
    def buttonToggled(self,button: QAbstractButton):
        self.buttonSignalMapping[self.buttonGroup.id(button)].emit(button)
        
