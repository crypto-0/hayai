from typing import List, Optional, Type
from PyQt5.QtCore import QModelIndex, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import  QFrame, QHBoxLayout,  QLabel, QListView, QPushButton, QScrollArea,  QSizePolicy, QVBoxLayout
from PyQt5.QtWidgets import QWidget
from provider_parsers import ProviderParser

from hayai.widgets.film import QFilmListModel
from hayai.widgets import QResizableIconListView
from hayai.widgets.film import QFilmDelegate

class QHome(QFrame):

    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)
    def __init__(self, providerParser: Type[ProviderParser] , parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self.providerParser: Type[ProviderParser] = providerParser

        self.categoryModels: List[QFilmListModel] = []

        self.categoryView: List[QListView] = []


        scrollAreaFrame: QFrame = QFrame()

        scrollArea = QScrollArea()
        scrollArea.setObjectName("scroll-area")
        scrollArea.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        
        scrollArea.setWidget(scrollAreaFrame)
        scrollArea.horizontalScrollBar().setEnabled(False)
        scrollArea.verticalScrollBar().setEnabled(True)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setWidgetResizable(True)
        scrollArea.setContentsMargins(0,0,0,0)


        scrollAreaFrameLayout: QVBoxLayout = QVBoxLayout()
        for category in providerParser.home_categories:
            categoryFrame: QFrame = QFrame()
            categoryFrame.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)

            categoryTitle: QLabel = QLabel(category.capitalize())

            navFrame: QFrame = QFrame()
            navFrame.setFrameStyle(QFrame.NoFrame)

            leftNavButton: QPushButton = QPushButton()
            leftNavButton.setIcon(QIcon("hayai/screens/home/assets/icons/go-back.png"))
            leftNavButton.setIconSize(QSize(24,24))
            leftNavButton.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)


            righNavButton: QPushButton = QPushButton()
            righNavButton.setIcon(QIcon("hayai/screens/home/assets/icons/go-forward.png"))
            righNavButton.setIconSize(QSize(24,24))
            righNavButton.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)

            categoryModel: QFilmListModel = QFilmListModel(self.providerParser.parse_category(category=category,fetch_image=False),maxFilms=30)
            #categoryModel: QFilmListModel = QFilmListModel()

            categoryView: QResizableIconListView = QResizableIconListView()
            categoryView.setItemDelegate(QFilmDelegate())
            categoryView.setModel(categoryModel)
            categoryView.setWrapping(False)
            categoryView.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
            categoryView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #pyright: ignore
            categoryView.horizontalScrollBar().setEnabled(False)
            
            righNavButton.clicked.connect(categoryView.scrollRight)
            leftNavButton.clicked.connect(categoryView.scrollLeft)
            categoryView.clicked.connect(self.filmClicked)

            navFrameLayout: QHBoxLayout = QHBoxLayout()
            navFrameLayout.addWidget(categoryTitle)
            navFrameLayout.addWidget(leftNavButton,Qt.AlignmentFlag.AlignRight)
            navFrameLayout.addWidget(righNavButton,Qt.AlignmentFlag.AlignRight)
            navFrameLayout.setContentsMargins(0,0,10,0)
            navFrameLayout.setSpacing(10)
            navFrame.setLayout(navFrameLayout)
            categoryFrameLayout: QVBoxLayout = QVBoxLayout()
            categoryFrameLayout.setContentsMargins(5,10,0,0)
            categoryFrameLayout.setSpacing(0)
            categoryFrameLayout.addWidget(navFrame)
            categoryFrameLayout.addWidget(categoryView)
            categoryFrame.setLayout(categoryFrameLayout)

            scrollAreaFrameLayout.addWidget(categoryFrame)

        scrollAreaFrameLayout.setContentsMargins(0,0,0,0)
        scrollAreaFrameLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scrollAreaFrameLayout.setSpacing(5)
        scrollAreaFrame.setLayout(scrollAreaFrameLayout)

        homeLayout: QHBoxLayout = QHBoxLayout()
        homeLayout.addWidget(scrollArea)
        homeLayout.setContentsMargins(0,0,0,0)
        homeLayout.setSpacing(0)
        self.setLayout(homeLayout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
        self.setObjectName("QHome")

