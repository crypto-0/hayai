from typing import Optional
from PyQt6.QtCore import QModelIndex, QObject, pyqtSignal, pyqtSlot, QUrl
from PyQt6.QtGui import QImage
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class QFilmImageWorker(QObject):
    result: pyqtSignal = pyqtSignal(QModelIndex,QImage)
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
    
    @pyqtSlot(QNetworkReply)
    def handleReply(self,reply: QNetworkReply):
        if reply.error()  == QNetworkReply.NetworkError.NoError: 
            data = reply.readAll().data()
            image = QImage.fromData(data) #pyright: ignore
            self.result.emit(reply.property("index"),image)

        reply.deleteLater()

    def cancel(self):
        self.canceled.emit()


        

