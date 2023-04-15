from typing import Optional
from PyQt6.QtCore import  QObject, pyqtSignal, QUrl
from PyQt6.QtGui import QImage
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class QFilmImageLoader(QObject):
    image: pyqtSignal = pyqtSignal(QImage,object)
    _canceled: pyqtSignal = pyqtSignal()

    def __init__(self,parent:Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.networkManager: QNetworkAccessManager = QNetworkAccessManager(self)

    def loadImage(self,url: str, filmHash: int):
        networkUrl: QUrl = QUrl(url)
        request: QNetworkRequest = QNetworkRequest(networkUrl)
        reply: QNetworkReply = self.networkManager.get(request)
        if reply.isFinished():
            self._handleImageReply(filmHash,reply)
        else:
            reply.finished.connect(lambda : self._handleImageReply(filmHash))
        self._canceled.connect(reply.abort)
    
    def _handleImageReply(self,filmHash: int,reply: Optional[QNetworkReply] = None):
        if reply is None:
            sender_reply = self.sender()
            if isinstance(sender_reply,QNetworkReply):
                reply = sender_reply
        if reply is not None:
            if reply.error()  == QNetworkReply.NetworkError.NoError: 
                data = reply.readAll().data()
                image = QImage.fromData(data) #pyright: ignore
                self.image.emit(image,filmHash)

            reply.deleteLater()

    def cancel(self):
        self._canceled.emit()


        

