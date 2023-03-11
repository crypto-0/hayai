from PyQt5.QtWidgets import QAbstractButton, QFrame, QHBoxLayout
from PyQt5.QtWidgets import QWidget
from typing import Optional, Type
from hayai.widgets.film import QFilmListModel
from hayai.widgets.film import QFilmListView
from provider_parsers import ProviderParser

class QCategory(QFrame):

    def __init__(self, providerParser: Type[ProviderParser], parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self.providerParser: Type[ProviderParser] = providerParser

        self.categoryModel: QFilmListModel =QFilmListModel()

        self.categoryView: QFilmListView = QFilmListView()
        self.categoryView.setWrapping(True)
        self.categoryView.setModel(self.categoryModel)


        categoryLayout: QHBoxLayout = QHBoxLayout()
        categoryLayout.addWidget(self.categoryView)
        categoryLayout.setContentsMargins(0,0,0,0)
        categoryLayout.setSpacing(0)
        self.setLayout(categoryLayout)

        self.setObjectName("QCategory")

    def load(self,categoryButton: QAbstractButton):
        self.categoryModel.setFilmGenerator(self.providerParser.parse_category(category=categoryButton.text().lower()))
        #self.categoryModel.setFilmGenerator(None)

