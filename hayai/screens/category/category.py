from PyQt6.QtCore import QModelIndex, pyqtSignal
from PyQt6.QtWidgets import QAbstractButton, QFrame, QHBoxLayout
from PyQt6.QtWidgets import QWidget
from typing import Optional, Type
from hayai.features.widgets.film import QFilmDelegate
from hayai.features.models.filmlist import QFilmListModel
from hayai.features.widgets.autofitview import QAutoFitView
from provider_parsers import ProviderParser

class QCategory(QFrame):
    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)

    def __init__(self, providerParser: Type[ProviderParser], parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self.providerParser: Type[ProviderParser] = providerParser

        self.categoryModel: QFilmListModel =QFilmListModel(parent=self)

        self.categoryView: QAutoFitView = QAutoFitView()
        self.categoryView.setWrapping(True)
        self.categoryView.setModel(self.categoryModel)
        self.categoryView.setItemDelegate(QFilmDelegate())
        self.categoryView.setBatchSize(50)
        self.categoryView.horizontalScrollBar().setEnabled(False)

        self.categoryView.clicked.connect(self.filmClicked)

        categoryLayout: QHBoxLayout = QHBoxLayout()
        categoryLayout.addWidget(self.categoryView)
        categoryLayout.setContentsMargins(0,0,0,0)
        categoryLayout.setSpacing(0)
        self.setLayout(categoryLayout)

        self.setObjectName("QCategory")

    def load(self,categoryButton: QAbstractButton):
        self.categoryModel.reset(self.providerParser.parse_category(category=categoryButton.text().lower(),fetch_image=False))
