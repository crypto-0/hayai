import sys
from typing import Optional

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)
import vlc
from vlc import Instance, MediaPlayer

from ..screen import QScreen

class QPlayer(QScreen):
    def __init__(self,mediaUrl: str = "", parent: Optional[QWidget]=None):
        super().__init__(parent)
        self._title = "Media Player"
        self._instance: Instance = vlc.Instance("--quiet")
        self._mediaPlayer: MediaPlayer = self._instance.media_player_new()
        self._mediaPlayerEventManager = self._mediaPlayer.event_manager()
        self._playIcon: QIcon = QIcon("hayai/screens/playerscreen/assets/icons/play.png")
        self._pauseIcon: QIcon = QIcon("hayai/screens/playerscreen/assets/icons/pause.png")
        self._forward10Icon: QIcon = QIcon("hayai/screens/playerscreen/assets/icons/forward10.png")
        self._replay10Icon: QIcon = QIcon("hayai/screens/playerscreen/assets/icons/replay10.png")
        videoframe: QFrame = QFrame(self)
        videoframe.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        videoframe.setMinimumWidth(480)
        videoframe.setFrameShape(QFrame.Shape.Box)
        videoframe.setFrameShadow(QFrame.Shadow.Raised)

        if sys.platform.startswith("linux"):  # for Linux using the X Server
            self._mediaPlayer.set_xwindow(videoframe.winId())
        elif sys.platform == "win32":  # for Windows
            self._mediaPlayer.set_hwnd(videoframe.winId())
        elif sys.platform == "darwin":  # for MacOS
            self._mediaPlayer.set_nsobject(videoframe.winId())

        controlsFrame: QFrame = QFrame()
        controlsFrame.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed)
        self._playPauseButton: QPushButton = QPushButton()
        self._playPauseButton.setIcon(self._playIcon)
        self._playPauseButton.setIconSize(QSize(24,24))
        self._playPauseButton.setFixedSize(30,30)

        self._rewind10secButton: QPushButton = QPushButton()
        self._rewind10secButton.setIcon(self._replay10Icon)
        self._rewind10secButton.setIconSize(QSize(24,24))
        self._rewind10secButton.setFixedSize(30,30)

        self._forward10secButton: QPushButton = QPushButton()
        self._forward10secButton.setIcon(self._forward10Icon)
        self._forward10secButton.setIconSize(QSize(24,24))
        self._forward10secButton.setFixedSize(30,30)

        self._slider: QSlider = QSlider(Qt.Orientation.Horizontal,self)
        self._slider.setPageStep(5)
        self._durationLabel: QLabel = QLabel()

        self._playPauseButton.clicked.connect(self.playPause)
        self._rewind10secButton.clicked.connect(self.onRewind10secButtonClicked)
        self._forward10secButton.clicked.connect(self.onForward10secButtonClicked)
        self._slider.sliderPressed.connect(self.onSliderPressed)
        self._slider.sliderReleased.connect(self.onSliderRelease)
        self._mediaPlayerEventManager.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.onMediaPlayerPostionChanged) #pyright:ignore
        self._mediaPlayerEventManager.event_attach(vlc.EventType.MediaPlayerPlaying, self.onMediaPlayerPlaying) #pyright:ignore
        self._mediaPlayerEventManager.event_attach(vlc.EventType.MediaPlayerPaused, self.onMediaPlayerPaused) #pyright:ignore
        self._mediaPlayerEventManager.event_attach(vlc.EventType.MediaPlayerStopped, self.onMediaPlayerStopped) #pyright:ignore

        controlsFrameLayout: QHBoxLayout = QHBoxLayout()
        controlsFrameLayout.addWidget(self._playPauseButton,Qt.AlignmentFlag.AlignLeft)
        controlsFrameLayout.addWidget(self._rewind10secButton,Qt.AlignmentFlag.AlignLeft)
        controlsFrameLayout.addWidget(self._forward10secButton,Qt.AlignmentFlag.AlignLeft)
        controlsFrameLayout.addWidget(self._slider,Qt.AlignmentFlag.AlignLeft)
        controlsFrameLayout.addWidget(self._durationLabel)
        controlsFrame.setLayout(controlsFrameLayout)

        playerLayout: QVBoxLayout = QVBoxLayout()
        playerLayout.addWidget(videoframe)
        playerLayout.addWidget(controlsFrame,Qt.AlignmentFlag.AlignTop)
        playerLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(playerLayout)

        media = self._instance.media_new(mediaUrl)
        self._mediaPlayer.set_media(media)
        self._slider.setRange(0,1000)
        self._mediaPlayer.play()

    def onDestroy(self):
        self._mediaPlayer.stop()
        self._instance.release()
        self._mediaPlayerEventManager.event_detach(vlc.EventType.MediaPlayerPositionChanged) #pyright:ignore
        return super().onDestroy()

    def playPause(self):
        if self._mediaPlayer.is_playing():
            self._mediaPlayer.pause()
        else:
            self._mediaPlayer.play()

    def onSliderPressed(self):
        self._mediaPlayerEventManager.event_detach(vlc.EventType.MediaPlayerPositionChanged) #pyright:ignore

    def onSliderRelease(self):
        self._mediaPlayerEventManager.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.onMediaPlayerPostionChanged) #pyright:ignore
        position = self._slider.value() / self._slider.maximum()
        self._mediaPlayer.set_position(position)


    def onRewind10secButtonClicked(self):
        position: float = self._mediaPlayer.get_position()
        position = position * self._slider.maximum()
        position -=10
        position = max(0,position)
        self._slider.setValue(int(position))
        self._mediaPlayer.set_position(position/self._slider.maximum())

    def onForward10secButtonClicked(self):
        position: float = self._mediaPlayer.get_position()
        position = position * self._slider.maximum()
        position +=10
        position = max(0,position)
        self._slider.setValue(int(position))
        self._mediaPlayer.set_position(position/self._slider.maximum())

    def onMediaPlayerPostionChanged(self,event):
        if not self._durationLabel.text():
            self.updateDurationLabel()
        position: float = self._mediaPlayer.get_position()
        self._slider.setValue(int(position * self._slider.maximum()))

    def onMediaPlayerPlaying(self,event):
        self._playPauseButton.setIcon(self._pauseIcon)

    def onMediaPlayerPaused(self,event):
        self._playPauseButton.setIcon(self._playIcon)

    def onMediaPlayerStopped(self,event):
        self._playPauseButton.setIcon(self._playIcon)

    def updateDurationLabel(self):
        duration: int = self._mediaPlayer.get_length()
        totalSeconds = duration// 1000
        hours = totalSeconds // 3600
        remainingSeconds = totalSeconds % 3600
        minutes = remainingSeconds // 60
        seconds = remainingSeconds % 60
        if hours > 0:
            self._durationLabel.setText(f"{hours}:{minutes:02d}:{seconds:02d}")
        else:
            self._durationLabel.setText(f"{minutes:02d}:{seconds:02d}")

