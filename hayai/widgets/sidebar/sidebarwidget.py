from typing import Dict, Optional
from PyQt5.QtCore import Qt, pyqtSignal
from .nav import QNav
from .providerlist import QProviderList
from .searchbar import QSearchbar
from provider_parsers import ProviderParser
from PyQt5.QtWidgets import (
    QAbstractButton,
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QSizePolicy,
    QVBoxLayout,
    QWidget
)

class QSidebar(QFrame):
    menuButtonToggled: pyqtSignal = pyqtSignal(QAbstractButton)
    categoryButtonToggled: pyqtSignal = pyqtSignal(QAbstractButton)
    libraryButtonToggled: pyqtSignal = pyqtSignal(QAbstractButton)
    generalButtonToggled: pyqtSignal = pyqtSignal(QAbstractButton)
    navButtonToggled: pyqtSignal = pyqtSignal(QAbstractButton)
    homeButtonToggle: pyqtSignal = pyqtSignal(QAbstractButton)
    lineEditTextChanged: pyqtSignal = pyqtSignal(str)
    lineEditFocusGained: pyqtSignal = pyqtSignal()

    def __init__(self,provider: type[ProviderParser],parent: Optional[QWidget] = None):
        super().__init__()

        self.previousButton: Optional[QAbstractButton] = None
        leftFrame: QFrame = QFrame()
        leftFrame.setObjectName("left")

        rightFrame: QFrame = QFrame()
        rightFrame.setObjectName("right")

        topFrame: QFrame = QFrame()
        topFrame.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)
        topFrame.setObjectName("top")

        #logo: QLogo = QLogo()
        searchbar: QSearchbar = QSearchbar()
        
        providerNav: QProviderList = QProviderList(["sol","zoro","asian"])
        menuNav: QNav = QNav("menu",["home","movies","tv shows"])
        librayNav: QNav = QNav("library",["downloads"])
        categoryNav: QNav = QNav("category",provider.categories)
        generalNav: QNav = QNav("general",["setting"])

        self.buttonGroup: QButtonGroup = QButtonGroup()
        self.buttonGroup.setExclusive(False)

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
        searchbar.lineEditFocusGained.connect(self.lineEditFocusGained)
        searchbar.lineEditFocusGained.connect(self.resetPreviousButton)
        searchbar.lineEditTextChanged.connect(self.lineEditTextChanged)

        topFrameLayout: QVBoxLayout = QVBoxLayout()
        #topFrameLayout.addWidget(logo)
        topFrameLayout.addWidget(searchbar)
        topFrameLayout.setContentsMargins(0,0,10,20)
        topFrameLayout.setSpacing(20)
        topFrameLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        topFrame.setLayout(topFrameLayout)

        leftFrameLayout: QVBoxLayout = QVBoxLayout()
        leftFrameLayout.addWidget(providerNav)
        leftFrameLayout.setContentsMargins(0,0,0,20)
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
        #if button is not self.previousButton:
        self.buttonSignalMapping[self.buttonGroup.id(button)].emit(button)
        #    self.previousButton = button
    def resetPreviousButton(self):
        self.previousButton = None;

