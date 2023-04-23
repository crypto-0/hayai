
from typing import Optional
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget


class QDescription(QFrame):

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__(parent = parent)

        self.titleLabel: QLabel = QLabel()
        self.titleLabel.setFixedHeight(40)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setObjectName("title")

        self.extraDetailLabel: QLabel = QLabel("Series(2017) . 5 seasons . 48 episodes")

        self.descriptionLabel: QLabel = QLabel()
        self.descriptionLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) 
        self.descriptionLabel.setFixedHeight(95)
        self.descriptionLabel.setMaximumWidth(600)
        self.descriptionLabel.setWordWrap(True)

        self.playButton: QPushButton = QPushButton("Download")
        self.playButton.setFixedSize(100,20)

        descriptionLayout: QVBoxLayout = QVBoxLayout()
        descriptionLayout.addWidget(self.titleLabel)
        descriptionLayout.addWidget(self.extraDetailLabel)
        descriptionLayout.addWidget(self.playButton)
        descriptionLayout.addWidget(self.descriptionLabel)
        descriptionLayout.setContentsMargins(0,0,0,0)
        descriptionLayout.setSpacing(20)
        self.setLayout(descriptionLayout)

    def updateDescription(self,title: str,description: str, extra: str):
        self.titleLabel.setText(title)
        self.descriptionLabel.setText(description)
        self.extraDetailLabel.setText(extra)




