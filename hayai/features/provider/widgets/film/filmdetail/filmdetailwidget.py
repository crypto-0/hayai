
from typing import Optional
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtProperty #pyright: ignore
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget


class QFilmDetail(QFrame):
    
    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        detailsFrame: QFrame = QFrame()
        detailsLabel: QLabel = QLabel("Details")
        detailsLabel.setObjectName("QDetailsLabel")

        genresFrame: QFrame = QFrame()
        genresLabel: QLabel = QLabel("Genres")
        genresLabel.setObjectName("QGenresLabel")
        self._genresContentLabel: QLabel = QLabel()

        countryFrame: QFrame = QFrame()
        countryLabel: QLabel = QLabel("Country")
        countryLabel.setObjectName("QCountryLabel")
        self._countryContentLabel: QLabel = QLabel()

        runtimeFrame: QFrame = QFrame()
        runtimeLabel: QLabel = QLabel("Runtime")
        runtimeLabel.setObjectName("QRuntimeLabel")
        self._runtimeContentLabel: QLabel = QLabel()

        detailsFrameLayout: QHBoxLayout = QHBoxLayout()
        detailsFrameLayout.addWidget(detailsLabel)
        detailsFrameLayout.setContentsMargins(0,0,0,0)
        detailsFrameLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        detailsFrame.setLayout(detailsFrameLayout)

        genresFrameLayout: QHBoxLayout = QHBoxLayout()
        genresFrameLayout.addWidget(genresLabel)
        genresFrameLayout.addWidget(self._genresContentLabel)
        genresFrameLayout.setContentsMargins(0,0,0,0)
        genresFrameLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        genresFrameLayout.setSpacing(33)
        genresFrame.setLayout(genresFrameLayout)

        countryFrameLayout: QHBoxLayout = QHBoxLayout()
        countryFrameLayout.addWidget(countryLabel)
        countryFrameLayout.addWidget(self._countryContentLabel)
        countryFrameLayout.setContentsMargins(0,0,0,0)
        countryFrameLayout.setSpacing(26)
        countryFrameLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        countryFrame.setLayout(countryFrameLayout)

        runtimeFrameLayout: QHBoxLayout = QHBoxLayout()
        runtimeFrameLayout.addWidget(runtimeLabel)
        runtimeFrameLayout.addWidget(self._runtimeContentLabel)
        runtimeFrameLayout.setContentsMargins(0,0,0,0)
        runtimeFrameLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        runtimeFrameLayout.setSpacing(20)
        runtimeFrame.setLayout(runtimeFrameLayout)

        detailsLayout: QVBoxLayout = QVBoxLayout()
        detailsLayout.addWidget(detailsFrame)
        detailsLayout.addWidget(genresFrame)
        detailsLayout.addWidget(countryFrame)
        detailsLayout.addWidget(runtimeFrame)
        detailsLayout.setContentsMargins(0,0,0,0)
        self.setLayout(detailsLayout)

        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)

    @property
    def genresContentLabel(self):
        return self._genresContentLabel
        
    @property
    def runtimeContentLabel(self):
        return self._runtimeContentLabel

    @property
    def countryContentLabel(self):
        return self._countryContentLabel

