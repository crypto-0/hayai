from PyQt5.QtCore import QModelIndex, Qt, pyqtSignal
from PyQt5.QtWidgets import QAbstractButton, QFrame, QHBoxLayout
from PyQt5.QtWidgets import QWidget
from typing import Optional, Type
from hayai.widgets.film import QFilmListModel, QFilmDelegate
from hayai.widgets import QResizableIconListView
from provider_parsers import ProviderParser

class QCategory(QFrame):
    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)

    def __init__(self, providerParser: Type[ProviderParser], parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self.providerParser: Type[ProviderParser] = providerParser

        self.categoryModel: QFilmListModel =QFilmListModel()

        self.categoryView: QResizableIconListView = QResizableIconListView()
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
        #self.categoryModel.setFilmGenerator(self.providerParser.parse_category(category=categoryButton.text().lower(),fetch_image=False))
        pass

