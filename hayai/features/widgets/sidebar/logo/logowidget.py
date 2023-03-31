from typing import Optional
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QWidget

class QLogo(QFrame):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        logoPixmap: QPixmap = QPixmap("hayai/widgets/sidebar/assets/icons/year-of-tiger.png")
        logoPixmap = logoPixmap.scaled(24,24)
        logoLabel: QLabel = QLabel()
        logoLabel.setPixmap(logoPixmap)

        hamburgerButton: QPushButton = QPushButton()
        hamburgerButton.setIcon(QIcon("hayai/widgets/sidebar/assets/icons/hamburger-menu.png"))

        logoLayout: QHBoxLayout = QHBoxLayout()
        logoLayout.addWidget(logoLabel)
        logoLayout.addWidget(hamburgerButton,alignment=Qt.AlignmentFlag.AlignRight)
        logoLayout.setContentsMargins(0,0,0,0)
        logoLayout.setSpacing(0)
        self.setLayout(logoLayout)

        self.setObjectName("QLogo")
