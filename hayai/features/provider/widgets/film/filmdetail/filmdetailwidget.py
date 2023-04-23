
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
        self.genresContentLabel: QLabel = QLabel()

        countryFrame: QFrame = QFrame()
        countryLabel: QLabel = QLabel("Country")
        countryLabel.setObjectName("QCountryLabel")
        self.countryContentLabel: QLabel = QLabel()

        runtimeFrame: QFrame = QFrame()
        runtimeLabel: QLabel = QLabel("Runtime")
        runtimeLabel.setObjectName("QRuntimeLabel")
        self.runtimeContentLabel: QLabel = QLabel()

        detailsFrameLayout: QHBoxLayout = QHBoxLayout()
        detailsFrameLayout.addWidget(detailsLabel)
        detailsFrameLayout.setContentsMargins(0,0,0,0)
        detailsFrameLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        detailsFrame.setLayout(detailsFrameLayout)

        genresFrameLayout: QHBoxLayout = QHBoxLayout()
        genresFrameLayout.addWidget(genresLabel)
        genresFrameLayout.addWidget(self.genresContentLabel)
        genresFrameLayout.setContentsMargins(0,0,0,0)
        genresFrameLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        genresFrameLayout.setSpacing(33)
        genresFrame.setLayout(genresFrameLayout)

        countryFrameLayout: QHBoxLayout = QHBoxLayout()
        countryFrameLayout.addWidget(countryLabel)
        countryFrameLayout.addWidget(self.countryContentLabel)
        countryFrameLayout.setContentsMargins(0,0,0,0)
        countryFrameLayout.setSpacing(26)
        countryFrameLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        countryFrame.setLayout(countryFrameLayout)

        runtimeFrameLayout: QHBoxLayout = QHBoxLayout()
        runtimeFrameLayout.addWidget(runtimeLabel)
        runtimeFrameLayout.addWidget(self.runtimeContentLabel)
        runtimeFrameLayout.setContentsMargins(0,0,0,0)
        runtimeFrameLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        runtimeFrameLayout.setSpacing(19)
        runtimeFrame.setLayout(runtimeFrameLayout)

        detailsLayout: QVBoxLayout = QVBoxLayout()
        detailsLayout.addWidget(detailsFrame)
        detailsLayout.addWidget(genresFrame)
        detailsLayout.addWidget(countryFrame)
        detailsLayout.addWidget(runtimeFrame)
        detailsLayout.setContentsMargins(0,0,0,0)
        self.setLayout(detailsLayout)

        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)

    @pyqtProperty(str)
    def filmGenres(self,genres: str):
        pass
    def updateDetail(self,genres: str, country: str, runtime: str):
        self.genresContentLabel.setText(genres)
        self.countryContentLabel.setText(country)
        self.runtimeContentLabel.setText(runtime)
        

