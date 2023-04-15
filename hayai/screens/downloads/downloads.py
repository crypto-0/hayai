from typing import Optional
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QWidget
from hayai.features.downloads.downloader import QHLSDownloader
from hayai.features.downloads.downloader import QDownloader
from hayai.features.downloads.widgets import QDownload

class QDownloads(QFrame):

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        url = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
        self.downloader: QDownloader = QHLSDownloader(url=url)
        download: QDownload = QDownload(self.downloader)

        downloadsLayout: QHBoxLayout = QHBoxLayout()
        downloadsLayout.addWidget(download)
        self.setLayout(downloadsLayout)

    def download(self):
        self.downloader.download()


