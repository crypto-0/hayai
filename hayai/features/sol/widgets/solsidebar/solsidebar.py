from typing import Optional
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QPushButton, QGroupBox, QVBoxLayout, QWidget
from ....widgets.navbutton import QNavButton

class QSolSidebar(QFrame):
    searchButtonClicked: pyqtSignal = pyqtSignal()
    homeButtonClicked: pyqtSignal = pyqtSignal()
    moviesButtonClicked: pyqtSignal = pyqtSignal()
    showsButtonClicked: pyqtSignal = pyqtSignal()
    imdbButtonClicked: pyqtSignal = pyqtSignal()
    settingButtonClicked: pyqtSignal = pyqtSignal()

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        menuGroupBox: QGroupBox = QGroupBox("Menu")
        categoryGroupBox: QGroupBox = QGroupBox("Category")
        generalGroupBox: QGroupBox = QGroupBox("General")

        iconLocation = "hayai/features/sol/widgets/solsidebar/assets"

        searchButton: QPushButton = QNavButton("search",f"{iconLocation}/search.png")
        homeButton: QPushButton = QNavButton("home",f"{iconLocation}/home.png")
        moviesButton: QPushButton = QNavButton("movies",f"{iconLocation}/movie.png")
        showsButton: QPushButton = QNavButton("shows",f"{iconLocation}/tv show.png")
        imdbButton: QPushButton = QNavButton("imdb",f"{iconLocation}/top imdb.png")
        settingButton: QPushButton = QNavButton("setting",f"{iconLocation}/setting.png")

        menuGroupBoxLayout: QVBoxLayout = QVBoxLayout()
        menuGroupBoxLayout.addWidget(searchButton)
        menuGroupBoxLayout.addWidget(homeButton)
        menuGroupBoxLayout.addWidget(moviesButton)
        menuGroupBoxLayout.addWidget(showsButton)
        menuGroupBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) 
        menuGroupBox.setLayout(menuGroupBoxLayout)

        categoryGroupBoxLayout: QVBoxLayout = QVBoxLayout()
        categoryGroupBoxLayout.addWidget(imdbButton)
        categoryGroupBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) 
        categoryGroupBox.setLayout(categoryGroupBoxLayout)

        generalGroupBoxLayout: QVBoxLayout = QVBoxLayout()
        generalGroupBoxLayout.addWidget(settingButton)
        generalGroupBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) 
        generalGroupBox.setLayout(generalGroupBoxLayout)

        searchButton.clicked.connect(self.searchButtonClicked)
        homeButton.clicked.connect(self.homeButtonClicked)
        moviesButton.clicked.connect(self.moviesButtonClicked)
        showsButton.clicked.connect(self.showsButtonClicked)
        imdbButton.clicked.connect(self.imdbButtonClicked)
        settingButton.clicked.connect(self.settingButtonClicked)

        sidebarLayout: QVBoxLayout = QVBoxLayout()
        sidebarLayout.addWidget(menuGroupBox)
        sidebarLayout.addWidget(categoryGroupBox)
        sidebarLayout.addWidget(generalGroupBox)
        sidebarLayout.setContentsMargins(5,20,0,0)
        sidebarLayout.setSpacing(0)
        self.setLayout(sidebarLayout)
        self.setFixedWidth(150)

