from typing import List, Optional, Type
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import  QFrame,  QLabel, QListView,  QSizePolicy, QVBoxLayout
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
        for category in providerParser.categories:
            categoryFrame: QFrame = QFrame()

            categoryTitle: QLabel = QLabel(category.capitalize())

            #categoryModel: QFilmListModel = QFilmListModel(self.providerParser.parse_category(category=category),maxFilms=30)
            categoryModel: QFilmListModel = QFilmListModel()

            categoryView: QFilmListView = QFilmListView()
            categoryView.setModel(categoryModel)
            categoryView.setWrapping(False)
            categoryView.update()
            categoryView.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
            categoryView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #pyright: ignore
            categoryView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #pyright: ignore

            categoryFrameLayout: QVBoxLayout = QVBoxLayout()
            categoryFrameLayout.setContentsMargins(5,10,0,0)
            categoryFrameLayout.setSpacing(0)
            categoryFrameLayout.addWidget(categoryTitle)
            categoryFrameLayout.addWidget(categoryView)
            categoryFrame.setLayout(categoryFrameLayout)

            homeLayout.addWidget(categoryFrame)

        homeLayout.setContentsMargins(0,0,0,0)
        homeLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        homeLayout.setSpacing(5)
        self.setLayout(homeLayout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
        self.setObjectName("QHome")

