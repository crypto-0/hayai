from typing import List, Optional, Type
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QAbstractButton, QFrame, QGridLayout, QLabel, QListView, QScrollArea, QSizePolicy, QVBoxLayout
from PyQt5.QtWidgets import QWidget
from provider_parsers import ProviderParser

from hayai.features.film import QFilmListModel
from hayai.features.film.filmlistview.filmlistview import QFilmListView

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

            categoryModel: QFilmListModel = QFilmListModel(self.providerParser.parse_category(category=category),maxFilms=30)

            categoryView: QFilmListView = QFilmListView()
            categoryView.setModel(categoryModel)
            categoryView.setWrapping(False)
            categoryView.update()
            categoryView.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
            categoryView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #pyright: ignore
            categoryView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #pyright: ignore

            categoryFrameLayout: QVBoxLayout = QVBoxLayout()
            categoryFrameLayout.setContentsMargins(0,0,0,0)
            categoryFrameLayout.setSpacing(0)
            categoryFrameLayout.addWidget(categoryTitle)
            categoryFrameLayout.addWidget(categoryView)
            categoryFrame.setLayout(categoryFrameLayout)

            homeLayout.addWidget(categoryFrame)

        homeLayout.setContentsMargins(0,0,0,0)
        #homeLayout.addStretch(1)  # add a stretch with alignment to the top
        homeLayout.setAlignment(Qt.AlignmentFlag.AlignTop)  # set the alignment to the top
        homeLayout.setSpacing(0)
        self.setLayout(homeLayout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
        self.setObjectName("QHome")

