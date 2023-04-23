from typing import Optional
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy, QVBoxLayout, QWidget

from .poster import QPoster
from .detail import QDetail
from .description import QDescription

class QOverview(QFrame):

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        self.poster: QPoster = QPoster()

        self.description: QDescription = QDescription()

        self.detail : QDetail = QDetail()

        
        leftFrame: QFrame = QFrame()
        leftFrame.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.MinimumExpanding)

        rightFrame: QFrame = QFrame()

        leftFrameLayout: QVBoxLayout = QVBoxLayout()
        leftFrameLayout.addWidget(self.poster)
        leftFrameLayout.addStretch()
        leftFrameLayout.setContentsMargins(0,0,0,0)
        leftFrameLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        leftFrame.setLayout(leftFrameLayout)


        rightFrameLayout: QVBoxLayout = QVBoxLayout()
        rightFrameLayout.addWidget(self.description)
        rightFrameLayout.addWidget(self.detail)
        rightFrameLayout.setContentsMargins(30,20,5,0)
        rightFrameLayout.setSpacing(10)
        rightFrame.setLayout(rightFrameLayout)

        overviewLayout: QHBoxLayout = QHBoxLayout()
        overviewLayout.addWidget(leftFrame)
        overviewLayout.addWidget(rightFrame)
        overviewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        overviewLayout.setContentsMargins(0,0,0,0)
        overviewLayout.setSpacing(5)
        self.setLayout(overviewLayout)

        self.setObjectName("QOverview")
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.Fixed)

    def updateOverview(self,posterIcon: QIcon, title: str, description: str,genre: str, country: str, duration: str,extra: str):
        size: QSize = posterIcon.actualSize(QSize(1920,1080))
        pixmap: QPixmap = posterIcon.pixmap(size)
        self.poster.setPixmap(pixmap)
        self.description.updateDescription(title=title.capitalize(),description=description,extra=extra.capitalize())
        self.detail.updateDetail(genres=genre,country=country,runtime=duration)

