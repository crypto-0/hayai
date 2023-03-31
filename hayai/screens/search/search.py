from PyQt6.QtCore import QModelIndex, pyqtSignal
from PyQt6.QtWidgets import  QFrame,  QVBoxLayout
from PyQt6.QtWidgets import QWidget
from typing import Optional, Type
from hayai.features.models.filmlist import QFilmListModel
from hayai.features.widgets.film import QFilmDelegate
from hayai.features.widgets.autofitview import QAutoFitView
from provider_parsers import ProviderParser
from hayai.features.widgets.searchbar import QSearchbar

class QSearch(QFrame):
    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)
    lineEditTextChanged: pyqtSignal = pyqtSignal(str)

    def __init__(self, providerParser: Type[ProviderParser], parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self.providerParser: Type[ProviderParser] = providerParser

        self.searchModel: QFilmListModel =QFilmListModel(parent=self)

        self.searchView: QAutoFitView = QAutoFitView()
        self.searchView.setWrapping(True)
        self.searchView.setModel(self.searchModel)
        self.searchView.setItemDelegate(QFilmDelegate())

        self.searchbar: QSearchbar = QSearchbar()

        self.searchView.clicked.connect(self.filmClicked)
        self.searchbar.lineEditTextChanged.connect(self.search)

        searchLayout: QVBoxLayout = QVBoxLayout()
        searchLayout.addWidget(self.searchbar)
        searchLayout.addWidget(self.searchView)
        searchLayout.setContentsMargins(0,0,0,0)
        searchLayout.setSpacing(0)
        self.setLayout(searchLayout)

        self.setObjectName("QSearch")

    def search(self,query: str):
        self.searchModel.reset(self.providerParser.parse_search(query,fetch_image = False))

