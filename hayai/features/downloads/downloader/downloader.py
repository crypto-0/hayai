from typing import Dict, List,  Optional
from PyQt6.QtWidgets import QWidget
from m3u8 import loads, M3U8
import re
import subprocess
import os
from PyQt6.QtCore import QObject, QUrl, pyqtSignal, pyqtSlot
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class QDownloader(QObject):
    progress: pyqtSignal = pyqtSignal(int,int,str)
    finished: pyqtSignal = pyqtSignal()

    def __init__(self,url: str, quality: str = "1080", outputDir: str = ".", outputFileName: str = "temp", parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        self.networkManager: QNetworkAccessManager = QNetworkAccessManager(self) 
        self.url: str = url
        self.quality: str = quality
        self.outputDir: str = outputDir if outputDir else "."
        self.outputFileName: str = outputFileName if outputFileName else "temp"

    def download(self) -> None:
        return


class QHLSDownloader(QDownloader):

    def __init__(self,url: str, quality: str = "1080", outputDir: str = ".", outputFileName: str = "temp", parent: Optional[QWidget] = None):
        super().__init__(url,quality,outputDir,outputFileName,parent)
        
        self._segmentReplies: set[QNetworkReply] = set()
        self._totalSegments: int = 0

    @pyqtSlot()
    def download(self):
        if self.url.endswith('.m3u8'):
            for segmentReply in self._segmentReplies:
                segmentReply.abort()
            self._totalSegments = -1
            self._segmentReplies = set()
            request: QNetworkRequest = QNetworkRequest(QUrl(self.url))
            reply: QNetworkReply = self.networkManager.get(request)
            if reply.isFinished():
                self._handlePlaylistReply(reply)
            else:
                reply.finished.connect(self._handlePlaylistReply)

    @pyqtSlot()
    def _handlePlaylistReply(self,reply: Optional[QNetworkReply] = None):
        if reply is None:
            sender_reply = self.sender()
            if isinstance(sender_reply,QNetworkReply):
                reply = sender_reply
        if reply is not None:
            if reply.error()  == QNetworkReply.NetworkError.NoError: 
                playlist: M3U8 = loads(reply.readAll().data().decode())
                playlists: List[Dict] = playlist.data["playlists"]
                if len(playlists) == 0:
                    print("No playlists found!!")
                    return
                quality_playlist: Optional[Dict] = None
                playlists = sorted(playlists, key=lambda k: int(k["stream_info"].get("resolution","0x0").split("x")[0]), reverse=True)
                quality_playlist = playlists[0]
                if self.quality:
                    for p in playlists:
                        resolution = p["stream_info"].get("resolution","0x0").split("x")[0]
                        if resolution == self.quality:
                            quality_playlist = p
                            break

                url: str = str(reply.url().url())
                base_url: str = url.rsplit("/",1)[0] + "/"
                playlist_url: str = quality_playlist["uri"]
                if not  playlist_url.startswith("http"):
                    playlist_url = base_url + playlist_url

                request: QNetworkRequest = QNetworkRequest(QUrl(playlist_url))
                playlistReply: QNetworkReply = self.networkManager.get(request)
                if playlistReply.isFinished():
                    self._handleSegmentPlaylistReply(playlistReply)
                else:
                    playlistReply.finished.connect(self._handleSegmentPlaylistReply)
                    
            reply.deleteLater()

    @pyqtSlot()
    def _handleSegmentPlaylistReply(self, reply: Optional[QNetworkReply] = None):
        if reply is None:
            sender_reply = self.sender()
            if isinstance(sender_reply,QNetworkReply):
                reply = sender_reply
        if reply is not None :
            if reply.error()  == QNetworkReply.NetworkError.NoError: 
                segments = loads(reply.readAll().data().decode()).data["segments"]
                url: str = reply.url().url()
                baseUrl = url.rsplit("/",1)[0] + "/"
                if not self.outputFileName:
                    self.outputFileName = f"{self.quality if self.quality else 'temp'}"
                
                for i, segment in enumerate(segments):
                    segmentUrl: str = segment["uri"]
                    if not  segmentUrl.startswith("http"):
                        segmentUrl = baseUrl + segmentUrl
                    filename: str = f"{self.outputFileName}_segment{i:05}.ts"
                    #filename: str = self.outputFileName + "_segment" + str(i) + ".ts"
                    filename = os.path.join(self.outputDir,filename)
                    request: QNetworkRequest = QNetworkRequest(QUrl(segmentUrl))
                    segmentReply: QNetworkReply = self.networkManager.get(request)
                    self._segmentReplies.add(segmentReply)
                    self._totalSegments +=1
                    if segmentReply.isFinished():
                        self._handleSegmentReply(filename=filename,reply=segmentReply)
                    else:
                        segmentReply.finished.connect(lambda filename=filename : self._handleSegmentReply(filename=filename))
            else:
                print("got eror with reply",reply.error(),reply.url())
            reply.deleteLater()
        else:
            print("got empty reply")

    def _handleSegmentReply(self,filename: str,reply: Optional[QNetworkReply] = None ):
        if reply is None:
            sender_reply = self.sender()
            if isinstance(sender_reply,QNetworkReply):
                reply = sender_reply
        if reply is not None:
            if reply.error()  == QNetworkReply.NetworkError.NoError: 
                with open(filename, "wb") as f:
                        f.write(reply.readAll().data())
                if reply in self._segmentReplies:
                    self._segmentReplies.discard(reply)
                    self.progress.emit(self._totalSegments - len(self._segmentReplies),self._totalSegments,f"Downloading {self.outputFileName}")
            else:
                print("error downloading segment",reply.error())
                if reply in self._segmentReplies:
                    self._segmentReplies.discard(reply)
                    self.progress.emit(self._totalSegments - len(self._segmentReplies),self._totalSegments,f"downloading {self.outputFileName}")

            if len(self._segmentReplies) == 0:
                self._combine_segments()
                self._convert_video_format(os.path.join(self.outputDir,self.outputFileName + ".ts"))

            reply.deleteLater()
    def _handleSegmentReplyRetry(self,reply: Optional[QNetworkReply],filename,retryCount:int):
        pass


    def _combine_segments(self):
        if not os.path.exists(self.outputDir):
            return
        with open(os.path.join(self.outputDir,self.outputFileName + ".ts"), "wb") as f:  
            segmentsFileNames = []
            for filename in os.listdir(self.outputDir):
                segmentFileName = os.path.join(self.outputDir,filename)
                if os.path.isfile(segmentFileName) and filename.startswith(f"{self.outputFileName}_segment"):
                    segmentsFileNames.append(segmentFileName)
            for idx,filename in enumerate(sorted(segmentsFileNames)):
                with open(os.path.join(self.outputDir, filename), "rb") as segmentFile:
                    f.write(segmentFile.read())
                if filename != self.outputFileName + ".ts":
                    os.remove(os.path.join(self.outputDir, filename))
                self.progress.emit(idx,len(segmentsFileNames) -1,f"combining {filename}{self.outputFileName} segmets")

    def _string_time_to_int(self,text):
        if isinstance(text, float):
            num = str(text)
            nums = num.split('.')
        else:
            nums = text.split(':')
        if len(nums) == 2:
            st_sn = int(nums[0]) * 60 + float(nums[1])
            return int(st_sn)
        elif len(nums) == 3:
            st_sn = int(nums[0]) * 3600 + int(nums[1]) * 60 + float(nums[2])
            return int(st_sn)
        else:
            #raise ValueError("Not correct time")
            return -1
    def _convert_video_format(self,file_location: str, format = ".mp4"):
        if not os.path.exists(file_location) or file_location.endswith(format):
            return
        file_location_with_format = file_location.rsplit(".",1)[0] + format
        ffprobecmd = ["ffprobe", "-v","error","-show_entries" ,"format=duration","-of" ,"default=noprint_wrappers=1:nokey=1","-i", file_location]
        ffmpegcmd = ["ffmpeg","-y", "-v","quiet","-stats","-i", file_location,"-c","copy",file_location_with_format]
        ffprobe = subprocess.run(ffprobecmd,stdout=subprocess.PIPE,shell=False,universal_newlines=True)
        duration = float(ffprobe.stdout.rstrip())
        duration = int(duration)
        ffmpeg_process = subprocess.Popen(ffmpegcmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             universal_newlines=True
                             )
        if(ffmpeg_process.stdout is None):
            return
        title = os.path.basename(file_location) + " to " + format
        for line in iter(ffmpeg_process.stdout.readline,''):
            if line:
                time = re.search(r"\btime=\b",line)
                if time:
                    start_time = time.span()[-1]
                    time_as_int = self._string_time_to_int(line[start_time:start_time + 11])
                    if time_as_int < duration:
                        self.progress.emit(time_as_int,duration,title)
                    else:
                        self.progress.emit(duration,duration,title)

        return_code = ffmpeg_process.poll()
        if not return_code:
            os.unlink(file_location)

