from typing import List, Optional, Type

from PyQt5.QtWidgets import QAbstractButton, QFrame, QListView, QSizePolicy, QVBoxLayout
from PyQt5.QtWidgets import QWidget
from provider_parsers import ProviderParser

from hayai.models import QFilmListModel

class QHome(QFrame):

    def __init__(self, providerParser: Type[ProviderParser] , parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self.providerParser: Type[ProviderParser] = providerParser

        self.categoryModels: List[QFilmListModel] = []

        self.categoryView: List[QListView] = []

        homeLayout: QVBoxLayout = QVBoxLayout()
        for category in providerParser.categories:
            categoryModel: QFilmListModel = QFilmListModel(self.providerParser.parse_category(category=category),maxFilms=30)
            categoryView: QListView = QListView()
            categoryView.setBatchSize(10)
            categoryView.setModel(categoryModel)
            categoryView.setLayoutMode(QListView.LayoutMode.Batched)
            categoryView.setFlow(QListView.Flow.LeftToRight)
            categoryView.setWrapping(False)
            categoryView.setViewMode(QListView.ViewMode.IconMode)
            categoryView.setUniformItemSizes(True)
            categoryView.setResizeMode(QListView.ResizeMode.Adjust)
            categoryView.setWordWrap(True)
            categoryView.setSpacing(10)
            categoryView.setFixedHeight(300)
            homeLayout.addWidget(categoryView)
        
        homeLayout.setContentsMargins(0,0,0,0)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Minimum)
        homeLayout.setSpacing(0)
        self.setLayout(homeLayout)

