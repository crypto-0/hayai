from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import  QFrame, QHBoxLayout,QPushButton,QLabel, QStackedLayout,QVBoxLayout
from PyQt5.QtWidgets import QWidget
from typing import Optional

class QBanner(QFrame):
    playButtonClicked: pyqtSignal = pyqtSignal(bool)
    favoriteButtonToggled: pyqtSignal = pyqtSignal(bool)

    def __init__(self, title: str,playTitle: str, description: str,bannerImage: QPixmap, parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent)

        self.titleLabel: QLabel = QLabel(title)

        playFrame: QFrame = QFrame

        self.playButton: QPushButton = QPushButton(playTitle)

        self.favoriteButton: QPushButton = QPushButton("+")

        self.descriptionLabel: QLabel = QLabel(description)

        self.bannerImageLabel: QLabel = QLabel()
        self.bannerImageLabel.setPixmap(bannerImage)

        frontFrame: QFrame = QFrame()
        backgroundFrame: QFrame = QFrame()

        playFrameLayout: QVBoxLayout = QVBoxLayout()
        playFrameLayout.addWidget(self.playButton)
        playFrameLayout.addWidget(self.favoriteButton)

        frontFrameLayout: QVBoxLayout = QVBoxLayout()
        frontFrameLayout.addWidget(self.titleLabel)
        frontFrameLayout.addWidget(playFrame)
        frontFrameLayout.addWidget(self.descriptionLabel)
        frontFrameLayout.setContentsMargins(0,0,0,0)
        frontFrame.setLayout(frontFrameLayout)

        backgroundFrameLayout: QHBoxLayout = QHBoxLayout()
        backgroundFrameLayout.addWidget(self.bannerImageLabel)
        backgroundFrame.setLayout(backgroundFrameLayout)

        bannerLayout: QStackedLayout = QStackedLayout()
        bannerLayout.addWidget(frontFrame)
        bannerLayout.addWidget(backgroundFrame)
        bannerLayout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self.setLayout(bannerLayout)
