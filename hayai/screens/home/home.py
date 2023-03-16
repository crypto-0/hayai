from typing import List, Optional, Type
from PyQt5.QtCore import QModelIndex, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import  QFrame, QHBoxLayout,  QLabel, QListView, QPushButton, QScrollArea,  QSizePolicy, QVBoxLayout
from PyQt5.QtWidgets import QWidget
from provider_parsers import ProviderParser

from hayai.widgets.film import QFilmListModel
from hayai.widgets import QResizableIconListView
from hayai.widgets.film import QFilmDelegate
from hayai.widgets.film import QFilmRow

class QHome(QFrame):

    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)
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


        scrollAreaFrameLayout: QVBoxLayout = QVBoxLayout()
        for category in providerParser.home_categories:
            filmRow: QFilmRow = QFilmRow(category)
            filmRow.setFilmGenerator(providerParser.parse_category(category=category))
            filmRow.filmClicked.connect(self.filmClicked)
            scrollAreaFrameLayout.addWidget(filmRow)

        scrollAreaFrameLayout.setContentsMargins(0,0,0,0)
        scrollAreaFrameLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scrollAreaFrameLayout.setSpacing(5)
        scrollAreaFrame.setLayout(scrollAreaFrameLayout)

        homeLayout: QHBoxLayout = QHBoxLayout()
        homeLayout.addWidget(scrollArea)
        homeLayout.setContentsMargins(0,0,0,0)
        homeLayout.setSpacing(0)
        self.setLayout(homeLayout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
        self.setObjectName("QHome")

