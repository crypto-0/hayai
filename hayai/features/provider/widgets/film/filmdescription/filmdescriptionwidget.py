
from typing import Optional
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtProperty #pyright: ignore

class QFilmDescription(QFrame):
    playButtonClicked: pyqtSignal = pyqtSignal()

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__(parent = parent)

        self._titleLabel: QLabel = QLabel()
        self._titleLabel.setFixedHeight(40)
        self._titleLabel.setWordWrap(True)
        self._titleLabel.setObjectName("title")

        self._extraDetailLabel: QLabel = QLabel()

        self._descriptionLabel: QLabel = QLabel()
        self._descriptionLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) 
        self._descriptionLabel.setFixedHeight(95)
        self._descriptionLabel.setMaximumWidth(600)
        self._descriptionLabel.setWordWrap(True)

        self._playButton: QPushButton = QPushButton("Play")
        self._playButton.setFixedSize(100,20)

        self._playButton.clicked.connect(self.playButtonClicked)

        descriptionLayout: QVBoxLayout = QVBoxLayout()
        descriptionLayout.addWidget(self._titleLabel)
        descriptionLayout.addWidget(self._extraDetailLabel)
        descriptionLayout.addWidget(self._playButton)
        descriptionLayout.addWidget(self._descriptionLabel)
        descriptionLayout.setContentsMargins(0,0,0,0)
        descriptionLayout.setSpacing(20)
        self.setLayout(descriptionLayout)

    @property
    def titleLabel(self):#pyright: ignore
        return self._titleLabel

    @property
    def descriptionLabel(self):#pyright: ignore
        return self._descriptionLabel


