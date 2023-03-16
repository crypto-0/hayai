from collections.abc import Iterator
from typing import Optional
from PyQt5.QtCore import QModelIndex, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from ..filmlistmodel import QFilmListModel
from ...resizableiconlistview import QResizableIconListView
from ..filmdelegate import QFilmDelegate

class QFilmRow(QFrame):
    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)

    def __init__(self,category: str,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        categoryFrame: QFrame = QFrame()
        categoryFrame.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)

        categoryTitle: QLabel = QLabel(category.capitalize())

        navFrame: QFrame = QFrame()
        navFrame.setFrameStyle(QFrame.NoFrame)

        leftNavButton: QPushButton = QPushButton()
        leftNavButton.setIcon(QIcon("hayai/screens/home/assets/icons/go-back.png"))
        leftNavButton.setIconSize(QSize(24,24))
        leftNavButton.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)


        righNavButton: QPushButton = QPushButton()
        righNavButton.setIcon(QIcon("hayai/screens/home/assets/icons/go-forward.png"))
        righNavButton.setIconSize(QSize(24,24))
        righNavButton.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)

        self.categoryModel: QFilmListModel = QFilmListModel()

        categoryView: QResizableIconListView = QResizableIconListView()
        categoryView.setItemDelegate(QFilmDelegate())
        categoryView.setModel(self.categoryModel)
        categoryView.setWrapping(False)
        categoryView.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        categoryView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #pyright: ignore
        categoryView.horizontalScrollBar().setEnabled(False)
        
        righNavButton.clicked.connect(categoryView.scrollRight)
        leftNavButton.clicked.connect(categoryView.scrollLeft)
        categoryView.clicked.connect(self.filmClicked)

        navFrameLayout: QHBoxLayout = QHBoxLayout()
        navFrameLayout.addWidget(categoryTitle)
        navFrameLayout.addWidget(leftNavButton,Qt.AlignmentFlag.AlignRight)
        navFrameLayout.addWidget(righNavButton,Qt.AlignmentFlag.AlignRight)
        navFrameLayout.setContentsMargins(0,0,10,0)
        navFrameLayout.setSpacing(10)
        navFrame.setLayout(navFrameLayout)
        categoryFrameLayout: QVBoxLayout = QVBoxLayout()
        categoryFrameLayout.setContentsMargins(5,10,0,0)
        categoryFrameLayout.setSpacing(0)
        categoryFrameLayout.addWidget(navFrame)
        categoryFrameLayout.addWidget(categoryView)
        categoryFrame.setLayout(categoryFrameLayout)

        filmRowLayout: QHBoxLayout = QHBoxLayout()
        filmRowLayout.addWidget(categoryFrame)
        self.setLayout(filmRowLayout)

    def setFilmGenerator(self,generator: Iterator):
        self.categoryModel.setFilmGenerator(generator)

