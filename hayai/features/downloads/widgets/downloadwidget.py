from typing import Optional, Type
from ..downloader import QDownloader
from PyQt6.QtWidgets import QFrame, QLabel, QProgressBar, QVBoxLayout, QWidget

class QDownload(QFrame):

    def __init__(self,downloader: QDownloader,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        self.titleLabel: QLabel = QLabel()
        self.progressBar: QProgressBar = QProgressBar(self)
        self.downloader: QDownloader = downloader

        self.downloader.progress.connect(self.updateProgress)

        downloadLayout: QVBoxLayout = QVBoxLayout()
        downloadLayout.addWidget(self.titleLabel)
        downloadLayout.addWidget(self.progressBar)
        self.setLayout(downloadLayout)

    def updateProgress(self,current: int,total: int, title: str):
        print("gotProgress",current,total,title )
        self.progressBar.setRange(0,total)
        self.progressBar.setValue(current)
        self.titleLabel.setText(title)


