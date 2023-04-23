from abc import ABC ,abstractmethod
from typing import  List, Optional
from dataclasses import dataclass, field

from PyQt6.QtCore import QObject
from PyQt6.QtNetwork import QNetworkAccessManager

@dataclass(frozen=True)
class VideoServer:
    name: str
    serverId: str


@dataclass(frozen=True)
class Episode:
    episodeNumber: str 
    title: str 
    episodeId: str 


@dataclass(frozen=True)
class Season:
    seasonNumber: str
    seasonId: str


@dataclass(frozen=True,eq=True)
class Film:
    title: str
    link: str
    isTv: bool
    extra: str
    posterUrl: str

@dataclass(frozen=True)
class FilmInfo:
    title: str = ""
    release: str = ""
    description: str = ""
    genre: str = ""
    country: str = ""
    duration: str = ""
    posterUrl: str = ""
    recommendation: List[Film] = field(default_factory=list,compare=False,repr=False,hash=False)

@dataclass(frozen=True)
class PageInfo:
    currentPage: int = 1
    lastPage: int = 1
    hasNextPage: bool = False

@dataclass(frozen=True)
class Page:
    pageInfo: PageInfo 
    films: List

class QProvider(QObject):
    _headers =  {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
            }
    def __init__(self,parent: Optional[QObject] = None):
        super().__init__(parent=parent)
        self.networkAccessManager: QNetworkAccessManager = QNetworkAccessManager()

    @abstractmethod
    def search(self,query: str,page_number: int = 1) -> Page :
        raise NotImplemented

