from typing import Optional
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QPushButton

class QNav(QGroupBox):

    def __init__(self,title:str,navLinks: List[str],parent: Optional[QWidget] = None):
        super().__init__(title,parent=parent)

        navLinkButtons: List[QPushButton] = list(map(self.createNavButton,navLinks))

        navLayout: QVBoxLayout = QVBoxLayout()
        for navLinkButton in navLinkButtons:
            navLayout.addWidget(navLinkButton)
        navLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) #pyright: ignore
        navLayout.setContentsMargins(0,0,0,0)
        self.setLayout(navLayout)

        self.setCheckable(False)
        #self.setFrameStyle(QFrame.Shape.HLine)
        self.setFlat(True)
        self.setObjectName("QNav")

    def createNavButton(self,navLink: str):
            navButton: QPushButton =QPushButton(navLink.capitalize())
            iconLocation = f"hayai/widgets/sidebar/assets/icons/{navLink}.png"
            navButton.setIcon(QIcon(iconLocation))
            navButton.setFlat(True)
            navButton.setStyleSheet("QPushButton { text-align: left; }")
            return navButton



