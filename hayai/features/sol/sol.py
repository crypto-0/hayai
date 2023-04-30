import json
from PyQt6.QtCore import QEventLoop, QUrl, pyqtSignal, pyqtSlot
from PyQt6.QtNetwork import QNetworkReply, QNetworkRequest
from ..provider import *
from ..provider.extractors.upcloud import QUpCloud
from ..provider.extractors.vidcloud import QVidcloud
from ..provider.extractors.videoextractor import VideoContainer,QVideoExtractor
from typing import Dict, List, Optional 
import lxml.html

class QSol(QProvider):
    _hostUrl: str = "https://solarmovie.pe"
    seasonsLoaded: pyqtSignal = pyqtSignal(list)
    episodesLoaded: pyqtSignal = pyqtSignal(list)
    movieServersLoaded: pyqtSignal = pyqtSignal(list)
    episodeServersLoaded: pyqtSignal = pyqtSignal(list)
    trendingMoviesLoaded: pyqtSignal = pyqtSignal(Page)
    trendingShowsLoaded: pyqtSignal = pyqtSignal(Page)
    latestMoviesLoaded: pyqtSignal = pyqtSignal(Page)
    latestShowsLoaded: pyqtSignal = pyqtSignal(Page)
    comingSoonLoaded: pyqtSignal = pyqtSignal(Page)
    moviesLoaded: pyqtSignal = pyqtSignal(Page)
    showsLoaded: pyqtSignal = pyqtSignal(Page)
    imdbLoaded: pyqtSignal = pyqtSignal(Page)
    searchLoaded: pyqtSignal = pyqtSignal(Page)
    filmInfoLoaded: pyqtSignal = pyqtSignal(FilmInfo)
    videoLoaded: pyqtSignal = pyqtSignal(VideoContainer)
    _abort: pyqtSignal = pyqtSignal()

    def __init__(self,parent: Optional[QObject] = None) -> None:
        super().__init__(parent=parent)
        upcloud: QUpCloud = QUpCloud(self)
        vidcloud: QVidcloud = QVidcloud(self)
        upcloud.videoLoaded.connect(self.videoLoaded)
        vidcloud.videoLoaded.connect(self.videoLoaded)
        self._extractors: Dict[str,QVideoExtractor] = {
                "Server UpCloud": upcloud,
                "UpCloud": upcloud,
                "Server Vidcloud": vidcloud,
                "Vidcloud": vidcloud
                }

    @pyqtSlot(str)
    def loadMovieServers(self,movieId: str) -> None:
        movieServerUrl : str = f"{self._hostUrl}/ajax/movie/episodes/{movieId}"
        request: QNetworkRequest = QNetworkRequest(QUrl(movieServerUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.movieServersReplyFinished)
        self._abort.connect(reply.abort)

    @pyqtSlot()
    def movieServersReplyFinished(self) -> None:
        reply: QObject = self.sender()
        if isinstance(reply,QNetworkReply) and reply.error() == QNetworkReply.NetworkError.NoError:
            response: str = reply.readAll().data().decode()
            htmlDoc : lxml.html.HtmlElement = lxml.html.fromstring(response)
            serverElements : List[lxml.html.HtmlElement] = htmlDoc.cssselect(".nav-item a")
            servers: List[VideoServer] = [] 
            for serverElement in serverElements:
                serverId: str = serverElement.get("data-linkid")
                serverTitle: str = serverElement.get("title")
                servers.append(VideoServer(serverTitle,serverId))
            self.movieServersLoaded.emit(servers)
            reply.deleteLater()


    @pyqtSlot(str)
    def loadSeasons(self,showId: str) -> None:
        seasonUrl: str = f"{self._hostUrl}/ajax/v2/tv/seasons/{showId}"
        request: QNetworkRequest = QNetworkRequest(QUrl(seasonUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.seasonsReplyFinished)
        self._abort.connect(reply.abort)

    @pyqtSlot()
    def seasonsReplyFinished(self):
        reply: QObject = self.sender()
        if isinstance(reply,QNetworkReply) and reply.error() == QNetworkReply.NetworkError.NoError:
            response: str = reply.readAll().data().decode()
            htmlDoc : lxml.html.HtmlElement = lxml.html.fromstring(response)
            seasonElements: List[lxml.html.HtmlElement] = htmlDoc.cssselect(".dropdown-item")
            seasons: List[Season] =[]
            for seasonElement in seasonElements:
                seasonNumber: str = seasonElement.text.split()[-1]
                seasonId: str = seasonElement.get("data-id")
                seasons.append(Season(seasonNumber,seasonId))
            self.seasonsLoaded.emit(seasons)
            reply.deleteLater()


    @pyqtSlot(str)
    def loadEpisodes(self,seasonId: str) -> None:
        episodesUrl: str = f"{self._hostUrl}/ajax/v2/season/episodes/{seasonId}"
        request: QNetworkRequest = QNetworkRequest(QUrl(episodesUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.episodesReplyFinished)
        self._abort.connect(reply.abort)

    @pyqtSlot()
    def episodesReplyFinished(self) -> None:
        reply: QObject = self.sender()
        if isinstance(reply,QNetworkReply) and reply.error() == QNetworkReply.NetworkError.NoError:
            response: str = reply.readAll().data().decode()
            htmlDoc : lxml.html.HtmlElement = lxml.html.fromstring(response)
            episodeElements:List[lxml.html.HtmlElement] = htmlDoc.cssselect("a")
            episodes : List[Episode] = []
            for episodeElement in episodeElements:
                episodeNumber: str = episodeElement.get("title").split(":")[0].split()[-1]
                episodeId = episodeElement.get("data-id")
                episodeTitle = episodeElement.get("title").split(":")[-1]
                episodes.append(Episode(episodeNumber,episodeTitle,episodeId))
            self.episodesLoaded.emit(episodes)
            reply.deleteLater()


    @pyqtSlot(str)
    def loadEpisodeServers(self,seasonId: str) -> None:
        episodeServersUrl : str = f"{self._hostUrl}/ajax/v2/episode/servers/{seasonId}"
        request: QNetworkRequest = QNetworkRequest(QUrl(episodeServersUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.episodeServersReplyFinished)
        self._abort.connect(reply.abort)

    @pyqtSlot()
    def episodeServersReplyFinished(self):
        reply: QObject = self.sender()
        if isinstance(reply,QNetworkReply) and reply.error() == QNetworkReply.NetworkError.NoError:
            response: str = reply.readAll().data().decode()
            htmlDoc : lxml.html.HtmlElement = lxml.html.fromstring(response)
            serverElements : List[lxml.html.HtmlElement] = htmlDoc.cssselect(".nav-item a")
            servers: List[VideoServer] = [] 
            for serverElement in serverElements:
                serverId: str = serverElement.get("data-id")
                serverTitle: str = serverElement.get("title")
                servers.append(VideoServer(serverTitle,serverId))
            self.episodeServersLoaded.emit(servers)
            reply.deleteLater()

    @pyqtSlot(str)
    def loadVideo(self,server: VideoServer):
        serverEmbedUrl: str = f"{self._hostUrl}/ajax/get_link/{server.serverId}"
        loop: QEventLoop = QEventLoop(self)
        request: QNetworkRequest = QNetworkRequest(QUrl(serverEmbedUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(loop.quit)
        self._abort.connect(reply.abort)
        loop.exec()
        if reply.error() == QNetworkReply.NetworkError.NoError:
            response: str = reply.readAll().data().decode()
            responseAsJson = json.loads(response)
            embed: str = responseAsJson["link"]
            extractor: Optional[QVideoExtractor] = self._extractors.get(server.name)
            if extractor is not None:
                extractor.extract(embed)
            else:
                self.videoLoaded.emit(VideoContainer([],[]))
        else:
            self.videoLoaded.emit(VideoContainer([],[]))

    @pyqtSlot()
    def loadHome(self):
        homeUrl: str = f"{self._hostUrl}/home"
        request: QNetworkRequest = QNetworkRequest(QUrl(homeUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.homeReplyFinished)
        self._abort.connect(reply.abort)

    @pyqtSlot()
    def homeReplyFinished(self):
        reply: QObject = self.sender()
        if isinstance(reply,QNetworkReply) and reply.error() == QNetworkReply.NetworkError.NoError:
            response: str = reply.readAll().data().decode()
            htmlDoc : lxml.html.HtmlElement = lxml.html.fromstring(response)
            trendingMoviesFLWItems: List[lxml.html.HtmlElement] = htmlDoc.cssselect(".section-id-01 #trending-movies .flw-item")
            trendingShowsFLWItems: List[lxml.html.HtmlElement] = htmlDoc.cssselect(".section-id-01 #trending-tv .flw-item")
            sectionElements : List[lxml.html.HtmlElement] = htmlDoc.cssselect(".section-id-02")
            latestMoviesFLWItems: List[lxml.html.HtmlElement] = sectionElements[0].cssselect(".flw-item" )
            latestShowsFLWItems: List[lxml.html.HtmlElement] = sectionElements[1].cssselect(".flw-item")
            comingSoonFLWItems: List[lxml.html.HtmlElement] = sectionElements[2].cssselect(".flw-item")
            trendingMovies: List[Film] = list(map(self.parseFLWElement, trendingMoviesFLWItems))
            trendingShows: List[Film] = list(map(self.parseFLWElement, trendingShowsFLWItems))
            latestMovies: List[Film] = list(map(self.parseFLWElement, latestMoviesFLWItems))
            latestShows: List[Film] = list(map(self.parseFLWElement, latestShowsFLWItems))
            comingSoonFilms: List[Film] = list(map(self.parseFLWElement, comingSoonFLWItems))
            self.trendingMoviesLoaded.emit(Page(PageInfo(),trendingMovies))
            self.trendingShowsLoaded.emit(Page(PageInfo(),trendingShows))
            self.latestMoviesLoaded.emit(Page(PageInfo(),latestMovies))
            self.latestShowsLoaded.emit(Page(PageInfo(),latestShows))
            self.comingSoonLoaded.emit(Page(PageInfo(),comingSoonFilms))
            reply.deleteLater()

    @pyqtSlot(int)
    def loadMovies(self,pageNumber: int):
        moviesUrl: str = f"{self._hostUrl}/movie?page={pageNumber}"
        request: QNetworkRequest = QNetworkRequest(QUrl(moviesUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.moviesReplyFinished)
        self._abort.connect(reply.abort)

    def moviesReplyFinished(self):
        reply: QObject = self.sender()
        if isinstance(reply,QNetworkReply) and reply.error() == QNetworkReply.NetworkError.NoError:
            response: str = reply.readAll().data().decode()
            htmlDoc : lxml.html.HtmlElement = lxml.html.fromstring(response)
            paginationElements: List[lxml.html.HtmlElement] = htmlDoc.cssselect(".pagination.pagination-lg li")
            pageInfo: PageInfo = self.parsePaginationElements(paginationElements)
            filmsFLWItems: List[lxml.html.HtmlElement] = htmlDoc.cssselect(".flw-item")
            films: List[Film] = list(map(self.parseFLWElement,filmsFLWItems ))
            self.moviesLoaded.emit(Page(pageInfo,films))
            reply.deleteLater()

    @pyqtSlot(int)
    def loadShows(self,pageNumber: int):
        showsUrl: str = f"{self._hostUrl}/tv-show?page={pageNumber}"
        request: QNetworkRequest = QNetworkRequest(QUrl(showsUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.showsReplyFinished)
        self._abort.connect(reply.abort)

    def showsReplyFinished(self):
        reply: QObject = self.sender()
        if isinstance(reply,QNetworkReply) and reply.error() == QNetworkReply.NetworkError.NoError:
            response: str = reply.readAll().data().decode()
            htmlDoc : lxml.html.HtmlElement = lxml.html.fromstring(response)
            paginationElements: List[lxml.html.HtmlElement] = htmlDoc.cssselect(".pagination.pagination-lg li")
            pageInfo: PageInfo = self.parsePaginationElements(paginationElements)
            filmsFLWItems: List[lxml.html.HtmlElement] = htmlDoc.cssselect(".flw-item")
            films: List[Film] = list(map(self.parseFLWElement,filmsFLWItems ))
            self.showsLoaded.emit(Page(pageInfo,films))
            reply.deleteLater()


    @pyqtSlot(int)
    def loadImdb(self,pageNumber: int):
        imdbUrl: str = f"{self._hostUrl}/top-imdb?page={pageNumber}"
        request: QNetworkRequest = QNetworkRequest(QUrl(imdbUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.imdbReplyFinished)
        self._abort.connect(reply.abort)

    def imdbReplyFinished(self):
        reply: QObject = self.sender()
        if isinstance(reply,QNetworkReply) and reply.error() == QNetworkReply.NetworkError.NoError:
            response: str = reply.readAll().data().decode()
            htmlDoc : lxml.html.HtmlElement = lxml.html.fromstring(response)
            paginationElements: List[lxml.html.HtmlElement] = htmlDoc.cssselect(".pagination.pagination-lg li")
            pageInfo: PageInfo = self.parsePaginationElements(paginationElements)
            filmsFLWItems: List[lxml.html.HtmlElement] = htmlDoc.cssselect(".flw-item")
            films: List[Film] = list(map(self.parseFLWElement,filmsFLWItems ))
            self.imdbLoaded.emit(Page(pageInfo,films))
            reply.deleteLater()

    def loadSearch(self,query: str,pageNumber):
        query = query.strip().replace(" ","-")
        searchUrl: str = f"{self._hostUrl}/search/{query}?page={pageNumber}"
        request: QNetworkRequest = QNetworkRequest(QUrl(searchUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.searchReplyFinished)
        self._abort.connect(reply.abort)

    def searchReplyFinished(self):
        reply: QObject = self.sender()
        if isinstance(reply,QNetworkReply) and reply.error() == QNetworkReply.NetworkError.NoError:
            response: str = reply.readAll().data().decode()
            htmlDoc : lxml.html.HtmlElement = lxml.html.fromstring(response)
            paginationElements: List[lxml.html.HtmlElement] = htmlDoc.cssselect(".pagination.pagination-lg li")
            pageInfo: PageInfo = self.parsePaginationElements(paginationElements)
            filmsFLWItems: List[lxml.html.HtmlElement] = htmlDoc.cssselect(".flw-item")
            films: List[Film] = list(map(self.parseFLWElement,filmsFLWItems ))
            self.searchLoaded.emit(Page(pageInfo,films))
            reply.deleteLater()

    def loadFilmInfo(self,url: str) -> None:
        request: QNetworkRequest = QNetworkRequest(QUrl(url))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.filmInfoReplyFinished)
        self._abort.connect(reply.abort)

    def filmInfoReplyFinished(self):
        reply: QObject = self.sender()
        if isinstance(reply,QNetworkReply) and reply.error() == QNetworkReply.NetworkError.NoError:
            response: str = reply.readAll().data().decode()
            htmlDoc : lxml.html.HtmlElement = lxml.html.fromstring(response)
            description = htmlDoc.cssselect(".description")[0].text_content()
            elements: lxml.html.HtmlElement = htmlDoc.cssselect(".row-line")
            release = elements[0].text_content().split("Released: ")[-1].strip()
            genreElement: lxml.html.HtmlElement = elements[1].cssselect("a")
            genre: str = "NA"
            if genreElement:
                genre = genreElement[0].text
            duration: str = elements[3].text_content().split("Duration: ")[-1].split()[0].strip()
            country: str = elements[4].cssselect("a")[0].text.strip()
            title = reply.request().url().url().split("watch-")[-1].split("-free")[0].replace("-"," ")
            flwItems: List[lxml.html.HtmlElement] = htmlDoc.cssselect(".flw-item")
            recommendations: List[Film] = list(map(self.parseFLWElement,flwItems))
            posterUrl:str = htmlDoc.cssselect(".detail_page-infor .film-poster-img")[0].get("src")
            filmInfo: FilmInfo = FilmInfo(title=title,release=release,description=description.strip(),genre=genre,country=country,duration=duration,posterUrl=posterUrl,recommendation=recommendations)
            self.filmInfoLoaded.emit(filmInfo)
            reply.deleteLater()


    def parseFLWElement(self,element: lxml.html.HtmlElement) -> Film:
        poster_url: lxml.html.HtmlElement = element.cssselect(".film-poster > img")[0].get("data-src")
        link_tag: lxml.html.HtmlElement = element.cssselect(".film-poster > a")[0]
        title: str = link_tag.get("title")
        link: str = link_tag.get("href")
        film_info_tags: List[lxml.html.HtmlElement] = element.cssselect(".film-detail .fd-infor span")
        
        extra_details: str = ""
        for info_tag in film_info_tags:
            extra_details += (info_tag.text + " . ") if info_tag.text is not None else ""
        extra_details = extra_details.strip()
        extra_details = extra_details.strip("  .  ")
        is_tv: bool = True if film_info_tags[-1].text == "TV" else False

        return Film(title,self._hostUrl + link,is_tv,posterUrl=poster_url,extra= extra_details)

    def parsePaginationElements(self,elements: List[lxml.html.HtmlElement]) -> PageInfo:
        currentPage: int = 1
        lastPage: int = 1
        hasNextPage: bool = False

        for pageItem in elements:
            className: str = pageItem.get("class",0)
            aTag: lxml.html.HtmlElement =  pageItem.cssselect("a")[0]
            if className.endswith("active"):
                currentPage = int(aTag.text)
            else:
                title: str = aTag.get("title","")
                href: str = aTag.get("href","")
                if title == "Last":
                    lastPage = int(href.rsplit("=",1)[1].strip())
                if title == "Next":
                    hasNextPage = True

        return PageInfo(currentPage,lastPage,hasNextPage)

    def abort(self):
        self._abort.emit()

