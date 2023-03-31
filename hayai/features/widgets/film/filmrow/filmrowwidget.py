from typing import Optional
from PyQt6.QtCore import QModelIndex, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from hayai.features.widgets.autofitview import QAutoFitView

class QFilmRow(QFrame):

    def __init__(self,category: str,view: QAutoFitView,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        categoryFrame: QFrame = QFrame()
        categoryFrame.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)

        categoryTitle: QLabel = QLabel(category.capitalize())

        navFrame: QFrame = QFrame()
        #navFrame.setFrameStyle() 

        leftNavButton: QPushButton = QPushButton()
        leftNavButton.setIcon(QIcon("hayai/screens/home/assets/icons/go-back.png"))
        leftNavButton.setIconSize(QSize(24,24))
        leftNavButton.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)


        righNavButton: QPushButton = QPushButton()
        righNavButton.setIcon(QIcon("hayai/screens/home/assets/icons/go-forward.png"))
        righNavButton.setIconSize(QSize(24,24))
        righNavButton.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)

        righNavButton.clicked.connect(view.scrollRight)
        leftNavButton.clicked.connect(view.scrollLeft)

        navFrameLayout: QHBoxLayout = QHBoxLayout()
        navFrameLayout.addWidget(categoryTitle)
        navFrameLayout.addWidget(leftNavButton,Qt.AlignmentFlag.AlignRight)
        navFrameLayout.addWidget(righNavButton,Qt.AlignmentFlag.AlignRight)
        navFrameLayout.setContentsMargins(0,0,0,0)
        navFrameLayout.setSpacing(5)
        navFrame.setLayout(navFrameLayout)
        categoryFrameLayout: QVBoxLayout = QVBoxLayout()
        categoryFrameLayout.setContentsMargins(0,0,0,0)
        categoryFrameLayout.setSpacing(0)
        categoryFrameLayout.addWidget(navFrame)
        categoryFrameLayout.addWidget(view)
        categoryFrame.setLayout(categoryFrameLayout)

        filmRowLayout: QHBoxLayout = QHBoxLayout()
        filmRowLayout.addWidget(categoryFrame)
        self.setLayout(filmRowLayout)

