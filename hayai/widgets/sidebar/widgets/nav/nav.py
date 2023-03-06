from typing import Optional
from typing import List

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAbstractButton, QButtonGroup, QGroupBox, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QPushButton

class QNav(QGroupBox):
    navButtonToggled: pyqtSignal = pyqtSignal(QAbstractButton)

    def __init__(self,title:str,navLinks: List[str],parent: Optional[QWidget] = None):
        super().__init__(title,parent=parent)

        navLinkButtons: List[QPushButton] = list(map(self.createNavButton,navLinks))

        self.navButtonGroup: QButtonGroup = QButtonGroup()

        self.navButtonGroup.buttonToggled.connect(self.navButtonToggled)

        navLayout: QVBoxLayout = QVBoxLayout()
        for navLinkButton in navLinkButtons:
            navLayout.addWidget(navLinkButton)
            self.navButtonGroup.addButton(navLinkButton)
        navLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) #pyright: ignore
        navLayout.setContentsMargins(0,0,0,0)
        self.setLayout(navLayout)

        self.setCheckable(False)
        self.setFlat(True)
        self.setObjectName("QNav")

    def createNavButton(self,navLink: str):
            navButton: QPushButton =QPushButton(navLink.capitalize())
            iconLocation = f"hayai/widgets/sidebar/assets/icons/{navLink}.png"
            navButton.setIcon(QIcon(iconLocation))
            navButton.setFlat(True)
            navButton.setCheckable(True)
            navButton.setStyleSheet("QPushButton { text-align: left; }")
            return navButton

    def getNavButtons(self):
        return self.navButtonGroup.buttons()

