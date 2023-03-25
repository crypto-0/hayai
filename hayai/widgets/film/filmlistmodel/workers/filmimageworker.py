from typing import Optional
from PyQt5.QtCore import QModelIndex, QObject, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtGui import QImage
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from functools import partial

class QFilmImageWorker(QObject):
    result: pyqtSignal = pyqtSignal(QImage,QModelIndex)
    canceled: pyqtSignal = pyqtSignal()

    def __init__(self,parent:Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.networkManager: QNetworkAccessManager = QNetworkAccessManager(self)
        self.networkManager.finished.connect(self.handleReply)

    @pyqtSlot(str,QModelIndex)
    def fetchImage(self,url: str, index: QModelIndex):
        networkUrl: QUrl = QUrl(url)
        request: QNetworkRequest = QNetworkRequest(networkUrl)
        reply: QNetworkReply = self.networkManager.get(request)
        reply.setProperty("index",index)
        self.canceled.connect(reply.abort)
    
    def handleReply(self,reply: QNetworkReply):
        if reply.error()  == QNetworkReply.NoError: #pyright: ignore
            data = reply.readAll().data()
            image = QImage.fromData(data)
            self.result.emit(image,reply.property("index"))

        reply.deleteLater()

    def cancel(self):
        self.canceled.emit()


        

