from PyQt6.QtCore import QEventLoop, QUrl
from PyQt6.QtNetwork import QNetworkReply, QNetworkRequest
from ..videoextractor import *
from typing import Dict,List
import json

class QVidcloud(QVideoExtractor):
    _sourcesBaseUrl: str = "https://rabbitstream.net/ajax/embed-4/getSources?id="
    _headers: Dict =  {
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/75.0.3770.142 Safari/537.36',
     'X-Requested-With': 'XMLHttpRequest'
     }
    _movKeyUrl =  "https://raw.githubusercontent.com/mov-cli/movkey/main/key.txt"
    _rapidclownKeyUrl = "https://raw.githubusercontent.com/consumet/rapidclown/main/key.txt"
    _enimaxkeyUrl = "https://raw.githubusercontent.com/enimax-anime/key/e4/key.txt"
    _keyUrls= [_movKeyUrl,_rapidclownKeyUrl,_enimaxkeyUrl]

    def __init__(self,parent: Optional[QObject] = None):
        super().__init__(parent=parent)

    def loadDecryptionKeys(self):
        loop: QEventLoop = QEventLoop()
        keys: List[str] = []
        for keyUrl in self._keyUrls:
            request: QNetworkRequest = QNetworkRequest(QUrl(keyUrl))
            reply: QNetworkReply = self.networkManager.get(request)
            #reply.finished.connect(self.keyReplyFinished)
            reply.finished.connect(loop.quit)
            loop.exec()
            if reply.error() == QNetworkReply.NetworkError.NoError:
                response: str = reply.readAll().data().decode()
                keys.append(response)
        return keys


    def extract(self,embed: str) -> None:
        embed = embed.rsplit("/",1)[-1].rstrip("?z=")
        sourceUrl: str = f"{self._sourcesBaseUrl}{embed}"
        request: QNetworkRequest = QNetworkRequest(QUrl(sourceUrl))
        for key,value in self._headers.items():
            request.setRawHeader(bytes(key,"utf-8"),bytes(value,"utf-8")) #pyright: ignore
        reply: QNetworkReply = self.networkManager.get(request)
        reply.finished.connect(self.extractReplyFinished)

    def extractReplyFinished(self):
        reply: QObject = self.sender()
        if isinstance(reply,QNetworkReply) and reply.error() == QNetworkReply.NetworkError.NoError:
            response: str = reply.readAll().data().decode()
            responseAsJson = json.loads(response)
            if not isinstance(responseAsJson.get("sources"),str):
                videoSources: List[Dict] = responseAsJson["sources"]
            else:
                keys: List[str] = self.loadDecryptionKeys()
                decryptedUrl = ""
                for key in keys:
                    decryptedUrl = self.decrypt(responseAsJson["sources"],key)
                    if(decryptedUrl.endswith("hls\"}]")):
                        break
                    else:
                        decryptedUrl = ""
                if not decryptedUrl:
                    self.videoLoaded.emit(VideoContainer([],[]))
                    return
                videoSources: List[Dict] = json.loads(decryptedUrl)

            videoTracks: List[Dict] = responseAsJson["tracks"]
            videos: list[Video] = []
            subtitles: list[Subtitle] = []
            for videoSource in videoSources:
                videos.append(Video(videoSource["file"],True))
            for track in videoTracks:
                if(track["kind"] == "thumbnails"):continue
                subtitles.append(Subtitle(track["label"],track["file"]))

            self.videoLoaded.emit(VideoContainer(videos,subtitles))
        else:
            self.videoLoaded.emit(VideoContainer([],[]))

