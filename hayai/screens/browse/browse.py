from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QAbstractButton, QFrame, QHBoxLayout, QListView, QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QResizeEvent
from typing import Optional, Type
from hayai.widgets.film import QFilmListModel
from hayai.widgets.film import QFilmListView
from provider_parsers import ProviderParser

class QBrowse(QFrame):

    def __init__(self, providerParser: Type[ProviderParser], parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self.providerParser: Type[ProviderParser] = providerParser

        self.browseModel: QFilmListModel =QFilmListModel()

        self.browseView: QFilmListView = QFilmListView()
        self.browseView.setWrapping(True)
        self.browseView.setModel(self.browseModel)


        browseLayout: QHBoxLayout = QHBoxLayout()
        browseLayout.addWidget(self.browseView)
        browseLayout.setContentsMargins(0,0,0,0)
        browseLayout.setSpacing(0)
        self.setLayout(browseLayout)

        self.setObjectName("QBrowse")

    def browseCategory(self,categoryButton: QAbstractButton):
        self.browseModel.setFilmGenerator(self.providerParser.parse_category(category=categoryButton.text().lower()))

