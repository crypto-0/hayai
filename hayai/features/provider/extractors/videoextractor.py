from abc import abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
import base64
from hashlib import md5
from Cryptodome.Cipher import AES
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtNetwork import QNetworkAccessManager

@dataclass(frozen=True)
class Video:
    url: str = ""
    is_m3u8: bool = False

@dataclass(frozen=True)
class Subtitle:
    language: str = ""
    link: str = ""



@dataclass(frozen=True)
class VideoContainer:
    videos: List[Video] = field(default_factory=list)
    subtitles: List[Subtitle] = field(default_factory=list)

class QVideoExtractor(QObject):
    videoLoaded: pyqtSignal = pyqtSignal(VideoContainer)
    
    def __init__(self,parent: Optional[QObject] = None):
        super().__init__(parent=parent)
        self.networkManager: QNetworkAccessManager = QNetworkAccessManager()

    @abstractmethod
    def extract(self,embed: str) -> None: 
        raise NotImplemented

    def _pad(self,data):
        BLOCK_SIZE = 16
        length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
        return data + (chr(length)*length).encode()


    def _unpad(self,data):
        return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]


    def _bytesToKey(self,data, salt, output=48):
        assert len(salt) == 8, len(salt)
        data = bytes(data,"utf-8") + salt
        key = md5(data).digest()
        final_key = key
        while len(final_key) < output:
            key = md5(key + data).digest()
            final_key += key
        return final_key[:output]


    def decrypt(self,encrypted, passphrase):
        encrypted = base64.b64decode(encrypted)
        assert encrypted[0:8] == b"Salted__"
        salt = encrypted[8:16]
        key_iv = self._bytesToKey(passphrase, salt, 32+16)
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = AES.new(key, AES.MODE_CBC, iv)
        return self._unpad(aes.decrypt(encrypted[16:])).decode("utf-8","ignore").lstrip(" ")

