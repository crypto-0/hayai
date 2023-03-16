from PyQt5.QtCore import QModelIndex, pyqtSignal
from PyQt5.QtWidgets import  QFrame, QHBoxLayout
from PyQt5.QtWidgets import QWidget
from typing import Optional, Type
from hayai.widgets.film import QFilmListModel
from hayai.widgets import QResizableIconListView
from provider_parsers import ProviderParser

class QSearch(QFrame):
    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)

    def __init__(self, providerParser: Type[ProviderParser], parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self.providerParser: Type[ProviderParser] = providerParser

        self.searchModel: QFilmListModel =QFilmListModel()

        self.searchView: QResizableIconListView = QResizableIconListView()
        self.searchView.setWrapping(True)
        self.searchView.setModel(self.searchModel)

        self.searchView.clicked.connect(self.filmClicked)

        searchLayout: QHBoxLayout = QHBoxLayout()
        searchLayout.addWidget(self.searchView)
        searchLayout.setContentsMargins(5,10,0,0)
        searchLayout.setSpacing(0)
        self.setLayout(searchLayout)

        self.setObjectName("QSearch")

    def search(self,query: str):
        self.searchModel.setFilmGenerator(self.providerParser.parse_search(query,fetch_image = False))

