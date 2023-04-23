from PyQt6.QtCore import QUrl, pyqtSignal, pyqtSlot
from PyQt6.QtNetwork import QNetworkReply, QNetworkRequest
from ..provider import *
from typing import List, Optional 
import requests
import lxml.html

class QSol(QProvider):
    _host_url: str = "https://solarmovie.pe"
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

    def __init__(self,parent: Optional[QObject] = None) -> None:
        super().__init__(parent=parent)


    @pyqtSlot(str)
    def loadMovieServers(self,movieId: str) -> None:
        movieServerUrl : str = f"{self._host_url}/ajax/movie/episodes/{movieId}"
        request: QNetworkRequest = QNetworkRequest(QUrl(movieServerUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.movieServersReplyFinished)

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
    def loadServerLink(self,serverId: str):
        pass

    @pyqtSlot(str)
    def loadSeasons(self,showId: str) -> None:
        seasonUrl: str = f"{self._host_url}/ajax/v2/tv/seasons/{showId}"
        request: QNetworkRequest = QNetworkRequest(QUrl(seasonUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.seasonsReplyFinished)

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
        episodesUrl: str = f"{self._host_url}/ajax/v2/season/episodes/{seasonId}"
        request: QNetworkRequest = QNetworkRequest(QUrl(episodesUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.episodesReplyFinished)

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
        episodeServersUrl : str = f"{self._host_url}/ajax/v2/episode/servers/{seasonId}"
        request: QNetworkRequest = QNetworkRequest(QUrl(episodeServersUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.episodeServersReplyFinished)

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

    @pyqtSlot()
    def loadHome(self):
        homeUrl: str = f"{self._host_url}/home"
        request: QNetworkRequest = QNetworkRequest(QUrl(homeUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.finished.connect(self.homeReplyFinished)

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
            trendingMovies: List[Film] = list(map(self._extractFilmElement, trendingMoviesFLWItems))
            trendingShows: List[Film] = list(map(self._extractFilmElement, trendingShowsFLWItems))
            latestMovies: List[Film] = list(map(self._extractFilmElement, latestMoviesFLWItems))
            latestShows: List[Film] = list(map(self._extractFilmElement, latestShowsFLWItems))
            comingSoonFilms: List[Film] = list(map(self._extractFilmElement, comingSoonFLWItems))
            self.trendingMoviesLoaded.emit(Page(PageInfo(),trendingMovies))
            self.trendingShowsLoaded.emit(Page(PageInfo(),trendingShows))
            self.latestMoviesLoaded.emit(Page(PageInfo(),latestMovies))
            self.latestShowsLoaded.emit(Page(PageInfo(),latestShows))
            self.comingSoonLoaded.emit(Page(PageInfo(),comingSoonFilms))
            reply.deleteLater()

    @pyqtSlot(int)
    def loadMovies(self,pageNumber: int):
        moviesUrl: str = f"{self._host_url}/movie?page={pageNumber}"
        request: QNetworkRequest = QNetworkRequest(QUrl(moviesUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.setProperty("category","movies")
        reply.finished.connect(self.categoryReplyFinished)

    @pyqtSlot(int)
    def loadShows(self,pageNumber: int):
        showsUrl: str = f"{self._host_url}/tv-show?page={pageNumber}"
        request: QNetworkRequest = QNetworkRequest(QUrl(showsUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.setProperty("category","shows")
        reply.finished.connect(self.categoryReplyFinished)

    @pyqtSlot(int)
    def loadImdb(self,pageNumber: int):
        imdbUrl: str = f"{self._host_url}/top-imdb?page={pageNumber}"
        request: QNetworkRequest = QNetworkRequest(QUrl(imdbUrl))
        reply: QNetworkReply = self.networkAccessManager.get(request)
        reply.setProperty("category","imdb")
        reply.finished.connect(self.categoryReplyFinished)

    @pyqtSlot()
    def categoryReplyFinished(self):
        reply: QObject = self.sender()
        if isinstance(reply,QNetworkReply) and reply.error() == QNetworkReply.NetworkError.NoError:
            response: str = reply.readAll().data().decode()
            htmlDoc : lxml.html.HtmlElement = lxml.html.fromstring(response)
            pageNavigation: List[lxml.html.HtmlElement] = htmlDoc.cssselect(".pagination.pagination-lg li")
            currentPage: int = 1
            lastPage: int = 1
            hasNextPage: bool = False

            for pageItem in pageNavigation:
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
            filmsFLWItems: List[lxml.html.HtmlElement] = htmlDoc.cssselect(".flw-item")
            films: List[Film] = list(map(self._extractFilmElement,filmsFLWItems ))
            category: str = reply.property("category")
            if category == "movies":
                self.moviesLoaded.emit(Page(PageInfo(currentPage,lastPage,hasNextPage),films))
            elif category == "shows":
                self.showsLoaded.emit(Page(PageInfo(currentPage,lastPage,hasNextPage),films))
            else:
                self.imdbLoaded.emit(Page(PageInfo(currentPage,lastPage,hasNextPage),films))


    def get_film_info(self,url: str) -> FilmInfo:
        try:
            r = requests.get(url,headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return FilmInfo()
        html_doc : lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        description = html_doc.cssselect(".description")[0].text_content()
        elements: lxml.html.HtmlElement = html_doc.cssselect(".row-line")
        release = elements[0].text_content().split("Released: ")[-1].strip()
        genre: str = elements[1].cssselect("a")[0].text
        duration: str = elements[3].text_content().split("Duration: ")[-1].split()[0].strip()
        country: str = elements[4].cssselect("a")[0].text.strip()
        title = url.split("watch-")[-1].split("-free")[0].replace("-"," ")
        flw_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")
        recommendations: List[Film] = list(map(self._extractFilmElement,flw_items))
        poster_url:str = html_doc.cssselect(".detail_page-infor .film-poster-img")[0].get("src")
        poster_image: bytes = self.get_poster_image(poster_url)
        return FilmInfo(title=title,release=release,description=description.strip(),genre=genre,country=country,duration=duration,recommendation=recommendations,poster_image=poster_image)

    def search(self,query: str,page_number) -> Page:
        query = query.strip().replace(" ","-")
        search_url: str = f"{self._host_url}/search/{query}"
        try:
            r: requests.Response = requests.get(f"{search_url}?page={page_number}",headers=self._headers)
            r.raise_for_status()
        except Exception as e:
            return Page(PageInfo(1,1,False),[])
        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        page_navigation: List[lxml.html.HtmlElement] = html_doc.cssselect(".pagination.pagination-lg li")

        current_page: int = 1
        last_page: int = 1
        has_next_page: bool = False


        for page_item in page_navigation:
            class_name: str = page_item.get("class",0)
            a_tag: lxml.html.HtmlElement =  page_item.cssselect("a")[0]
            if class_name.endswith("active"):
                current_page = int(a_tag.text)
            else:
                title: str = a_tag.get("title","")
                href: str = a_tag.get("href","")
                if title == "Last":
                    last_page = int(href.rsplit("=",1)[1])
                if title == "Next":
                    has_next_page = True

        html_doc: lxml.html.HtmlElement = lxml.html.fromstring(r.text)
        flw_items: List[lxml.html.HtmlElement] = html_doc.cssselect(".flw-item")
        films: List[Film] = list(map(self._extractFilmElement, flw_items))
        page_info: PageInfo = PageInfo(current_page,last_page,has_next_page)
        return Page(page_info,films)

    def _extractFilmElement(self,element: lxml.html.HtmlElement) -> Film:
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

        return Film(title,self._host_url + link,is_tv,poster_url=poster_url,extra= extra_details)

    def get_poster_image(self, url: str) -> bytes:
        try:
            r: requests.Response = requests.get(url,headers=self._headers)
            r.raise_for_status()
            poster_data  = r.content
            return poster_data
        except:
            return bytes()
