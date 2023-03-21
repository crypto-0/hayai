from typing import Optional
from PyQt5.QtCore import Qt
import mpv

from PyQt5.QtWidgets import QFrame, QWidget


class QPlayer(QFrame):
    def __init__(self,id, parent: Optional[QWidget]=None):
        super().__init__(parent)
        
        self.setAttribute(Qt.WA_DontCreateNativeAncestors) #pyright: ignore
        self.setAttribute(Qt.WA_NativeWindow) #pyright: ignore
        #self.player = mpv.MPV(wid=str(int(self.winId())),
        self.player = mpv.MPV(wid=str(int(id)),
                vo='x11', # You may not need this
                loglevel='debug',input_default_bindings=False,input_vo_keyboard=False,osc=True,script_opts='osc-layout=box,osc-seekbarstyle=bar,osc-deadzonesize=0,osc-minmousemove=3')
    def play(self):
        self.player.play('/home/tae/godzilla vs kong (2021)/godzilla vs kong (2021).mp4')
        #player.play("https://t-eu-3.onthecloudcdn.com/_v10/236850c4c87803d04774edfde9e151e5e4238646b5137a01d3f5c83f27ff6f23100180ab080c2906c6cba4b39e87edff2845f42fea0cb2736def27e801e321c96d0a0617811e58a445f1206ee1edface5ef5d67f81349d858c20b657ed2cc98168d4b1c3535e66f1583a955e5eae62f184688592ddd44715433cc232e98c21aa/playlist.m3u8")

    def stop(self):
        self.player.stop()

