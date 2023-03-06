from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractButton, QFrame, QHBoxLayout, QListView
from PyQt5.QtWidgets import QWidget
from typing import Optional, Type
from hayai.models import QFilmListModel
from provider_parsers import ProviderParser

class QBrowse(QFrame):

    def __init__(self, providerParser: Type[ProviderParser], parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self.providerParser: Type[ProviderParser] = providerParser

        self.browseModel: QFilmListModel =QFilmListModel()


        self.browseView: QListView = QListView()
        self.browseView.setModel(self.browseModel)
        self.browseView.setLayoutMode(QListView.LayoutMode.Batched)
        self.browseView.setBatchSize(10)
        self.browseView.setViewMode(QListView.ViewMode.IconMode)
        self.browseView.setFlow(QListView.Flow.LeftToRight)
        self.browseView.setUniformItemSizes(True)
        self.browseView.setResizeMode(QListView.ResizeMode.Adjust)
        self.browseView.setWordWrap(True)
        #self.browseView.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.browseView.setSpacing(15)
        self.browseView.setContentsMargins(0,0,0,0)


        browseLayout: QHBoxLayout = QHBoxLayout()
        browseLayout.addWidget(self.browseView)
        browseLayout.setContentsMargins(0,0,0,0)
        browseLayout.setSpacing(0)
        self.setLayout(browseLayout)


    def browseCategory(self,categoryButton: QAbstractButton):
        self.browseModel.setFilmGenerator(self.providerParser.parse_category(category=categoryButton.text().lower()))
