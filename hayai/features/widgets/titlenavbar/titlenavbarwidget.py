from typing import Optional
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget

class QTitleNavbar(QFrame):
    forward: pyqtSignal = pyqtSignal()
    back: pyqtSignal = pyqtSignal()

    def __init__(self,title,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        titleLabel: QLabel = QLabel(title.capitalize())


        self.leftNavButton: QPushButton = QPushButton()
        self.leftNavButton.setIcon(QIcon("hayai/screens/home/assets/icons/go-back.png"))
        self.leftNavButton.setIconSize(QSize(24,24))
        self.leftNavButton.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)


        self.righNavButton: QPushButton = QPushButton()
        self.righNavButton.setIcon(QIcon("hayai/screens/home/assets/icons/go-forward.png"))
        self.righNavButton.setIconSize(QSize(24,24))
        self.righNavButton.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)

        self.righNavButton.clicked.connect(self.forward)
        self.leftNavButton.clicked.connect(self.back)


        titleNavBarLayout: QHBoxLayout = QHBoxLayout()
        titleNavBarLayout.addWidget(titleLabel)
        titleNavBarLayout.addWidget(self.leftNavButton,Qt.AlignmentFlag.AlignRight)
        titleNavBarLayout.addWidget(self.righNavButton,Qt.AlignmentFlag.AlignRight)
        titleNavBarLayout.setContentsMargins(0,0,0,0)
        titleNavBarLayout.setSpacing(5)
        self.setLayout(titleNavBarLayout)
        self.setObjectName("QTitleNavbar")
