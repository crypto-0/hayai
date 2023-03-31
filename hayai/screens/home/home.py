from typing import List, Optional, Type
from PyQt6.QtCore import QModelIndex, Qt, pyqtSignal

from PyQt6.QtWidgets import  QFrame, QHBoxLayout,  QListView,  QScrollArea,  QSizePolicy, QVBoxLayout
from PyQt6.QtWidgets import QWidget
from provider_parsers import ProviderParser

from hayai.features.models.filmlist import QFilmListModel
from hayai.features.widgets.autofitview import QAutoFitView
from hayai.features.widgets.film import QFilmDelegate
from hayai.features.widgets.film import QFilmRow

class QHome(QFrame):

    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)
    scrollbarValueChanged: pyqtSignal = pyqtSignal(int)
    def __init__(self, providerParser: Type[ProviderParser] , parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self.providerParser: Type[ProviderParser] = providerParser

        self.categoryModels: List[QFilmListModel] = []

        self.categoryView: List[QListView] = []


        scrollAreaFrame: QFrame = QFrame()

        scrollArea = QScrollArea()
        scrollArea.setObjectName("scroll-area")
        scrollArea.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        
        scrollArea.setWidget(scrollAreaFrame)
        scrollArea.horizontalScrollBar().setEnabled(False)
        scrollArea.verticalScrollBar().setEnabled(True)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setWidgetResizable(True)
        scrollArea.setContentsMargins(0,0,0,0)

        scrollArea.verticalScrollBar().valueChanged.connect(self.scrollbarValueChanged)
        scrollAreaFrameLayout: QVBoxLayout = QVBoxLayout()
        for category in providerParser.home_categories:
            filmModel: QFilmListModel = QFilmListModel(providerParser.parse_category(category=category))
            filmView: QAutoFitView = QAutoFitView()
            filmView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            filmView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            filmView.setItemDelegate(QFilmDelegate())
            filmView.setModel(filmModel)
            filmRow: QFilmRow = QFilmRow(category,filmView,parent=self)
            filmView.clicked.connect(self.filmClicked)
            scrollAreaFrameLayout.addWidget(filmRow)

        scrollAreaFrameLayout.setContentsMargins(0,0,0,0)
        scrollAreaFrameLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scrollAreaFrameLayout.setSpacing(0)
        scrollAreaFrame.setLayout(scrollAreaFrameLayout)

        homeLayout: QHBoxLayout = QHBoxLayout()
        homeLayout.addWidget(scrollArea)
        homeLayout.setContentsMargins(0,0,0,0)
        homeLayout.setSpacing(0)
        self.setLayout(homeLayout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
        self.setObjectName("QHome")

