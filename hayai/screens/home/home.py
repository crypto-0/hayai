from typing import List, Optional, Type
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import  QFrame, QHBoxLayout,  QLabel, QListView, QPushButton,  QSizePolicy, QVBoxLayout
from PyQt5.QtWidgets import QWidget
from provider_parsers import ProviderParser

from hayai.widgets.film import QFilmListModel
from hayai.widgets.film import QFilmListView

class QHome(QFrame):

    def __init__(self, providerParser: Type[ProviderParser] , parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self.providerParser: Type[ProviderParser] = providerParser

        self.categoryModels: List[QFilmListModel] = []

        self.categoryView: List[QListView] = []

        homeLayout: QVBoxLayout = QVBoxLayout()
        for category in providerParser.home_categories:
            categoryFrame: QFrame = QFrame()

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

            categoryView: QFilmListView = QFilmListView()
            categoryView.setModel(categoryModel)
            categoryView.setWrapping(False)
            categoryView.update()
            categoryView.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
            categoryView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #pyright: ignore
            categoryView.horizontalScrollBar().setEnabled(False)
            
            righNavButton.clicked.connect(categoryView.scrollRight)
            leftNavButton.clicked.connect(categoryView.scrollLeft)

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

            homeLayout.addWidget(categoryFrame)

        homeLayout.setContentsMargins(0,0,0,0)
        homeLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        homeLayout.setSpacing(5)
        self.setLayout(homeLayout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
        self.setObjectName("QHome")

