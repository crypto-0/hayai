from enum import Enum
from typing import Optional

from PyQt6.QtCore import QFile, QPointF, QRectF
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen, QPixmap
from PyQt6.QtWidgets import QAbstractButton, QWidget
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtXml import QDomDocument

class TitleBarButtonState(Enum):
    NORMAL = 0
    HOVER = 1
    PRESSED = 2


class TitleBarButton(QAbstractButton):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setFixedSize(46, 32)
        self._state = TitleBarButtonState.NORMAL

        # icon color
        self._normalColor = QColor("#7c859E")
        self._hoverColor = QColor("white")
        self._pressedColor = QColor(0, 0, 0)

        # background color
        self._normalBgColor = QColor(0, 0, 0, 0)
        self._hoverBgColor = QColor(0, 0, 0, 26)
        self._pressedBgColor = QColor(0, 0, 0, 51)

    def setState(self, state: TitleBarButtonState):
        self._state: TitleBarButtonState = state
        self.update()

    def isPressed(self):
        return self._state == TitleBarButtonState.PRESSED
    def isHover(self):
        return self._state == TitleBarButtonState.HOVER

    def getNormalColor(self):
        return self._normalColor

    def getHoverColor(self):
        return self._hoverColor

    def getPressedColor(self):
        return self._pressedColor

    def getNormalBackgroundColor(self):
        return self._normalBgColor

    def getHoverBackgroundColor(self):
        return self._hoverBgColor

    def getPressedBackgroundColor(self):
        return self._pressedBgColor

    def setNormalColor(self, color: QColor):
        self._normalColor: QColor = QColor(color)
        self.update()

    def setHoverColor(self, color: QColor):
        self._hoverColor: QColor = QColor(color)
        self.update()

    def setPressedColor(self, color: QColor):
        self._pressedColor: QColor = QColor(color)
        self.update()

    def setNormalBackgroundColor(self, color: QColor):
        self._normalBgColor = QColor(color)
        self.update()

    def setHoverBackgroundColor(self, color):
        self._hoverBgColor = QColor(color)
        self.update()

    def setPressedBackgroundColor(self, color):
        self._pressedBgColor = QColor(color)
        self.update()

    def enterEvent(self, e):
        self.setState(TitleBarButtonState.HOVER)
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setState(TitleBarButtonState.NORMAL)
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() != Qt.MouseButton.LeftButton:
            return

        self.setState(TitleBarButtonState.PRESSED)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e) -> None:
        if e.button() != Qt.MouseButton.LeftButton:
            return
        self.setState(TitleBarButtonState.HOVER)
        return super().mouseReleaseEvent(e)

    def _getColors(self):
        """ get the icon color and background color """
        if self._state == TitleBarButtonState.NORMAL:
            return self._normalColor, self._normalBgColor
        elif self._state == TitleBarButtonState.HOVER:
            return self._hoverColor, self._hoverBgColor

        return self._pressedColor, self._pressedBgColor

    """
    normalColor = pyqtProperty(QColor, getNormalColor, setNormalColor)
    hoverColor = pyqtProperty(QColor, getHoverColor, setHoverColor)
    pressedColor = pyqtProperty(QColor, getPressedColor, setPressedColor)
    normalBackgroundColor = pyqtProperty(
        QColor, getNormalBackgroundColor, setNormalBackgroundColor)
    hoverBackgroundColor = pyqtProperty(
        QColor, getHoverBackgroundColor, setHoverBackgroundColor)
    pressedBackgroundColor = pyqtProperty(
        QColor, getPressedBackgroundColor, setPressedBackgroundColor)
        """


class SvgTitleBarButton(TitleBarButton):

    def __init__(self, iconPath: str, parent: Optional[QWidget]=None):
        super().__init__(parent)
        self._svgDom = QDomDocument()
        self.setIcon(iconPath)

    def setIcon(self, iconPath: str):
        f = QFile(iconPath)
        f.open(QFile.OpenModeFlag.ReadOnly)
        self._svgDom.setContent(f.readAll())
        f.close()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        color, bgColor = self._getColors()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        color = color.name()
        pathNodes = self._svgDom.elementsByTagName('path')
        for i in range(pathNodes.length()):
            element = pathNodes.at(i).toElement()
            element.setAttribute('stroke', color)

        renderer = QSvgRenderer(self._svgDom.toByteArray())
        renderer.render(painter, QRectF(self.rect()))

class PngTitleBarButton(TitleBarButton):
    def __init__(self, iconPath: str,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.pixmap = QPixmap(iconPath)
        self.hoverPixmap = self.createColoredPixmap(self.pixmap,self._hoverColor)

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        pixmap = self.pixmap
        if self.isHover() or self.isPressed():
            pixmap = self.hoverPixmap

        painter.drawPixmap(self.rect(), pixmap)
    def createColoredPixmap(self,pixmap: QPixmap,color: QColor):
        pixmap = pixmap.copy()
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()

        return pixmap


class MinimizeButton(TitleBarButton):

    def paintEvent(self, e):
        painter = QPainter(self)
        color, bgColor = self._getColors()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)


class MaximizeButton(TitleBarButton):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._isMax = False

    def setMaxState(self, isMax):
        """ update the maximized state and icon """
        if self._isMax == isMax:
            return

        self._isMax = isMax
        self.setState(TitleBarButtonState.NORMAL)

    def paintEvent(self, e):
        painter = QPainter(self)
        color, bgColor = self._getColors()

        # draw background
        painter.setBrush(bgColor)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)

        r = self.devicePixelRatioF()
        painter.scale(1/r, 1/r)
        if not self._isMax:
            painter.drawRect(int(18*r), int(11*r), int(10*r), int(10*r))
        else:
            painter.drawRect(int(18*r), int(13*r), int(8*r), int(8*r))
            x0 = int(18*r)+int(2*r)
            y0 = 13*r
            dw = int(2*r)
            path = QPainterPath(QPointF(x0, y0))
            path.lineTo(x0, y0-dw)
            path.lineTo(x0+8*r, y0-dw)
            path.lineTo(x0+8*r, y0-dw+8*r)
            path.lineTo(x0+8*r-dw, y0-dw+8*r)
            painter.drawPath(path)


class CloseButton(SvgTitleBarButton):
    """ Close button """

    def __init__(self, parent=None):
        super().__init__("hayai/features/widgets/titlebar/assets/close.svg", parent)
        self.setHoverColor(QColor("white"))
        self.setPressedColor(QColor("white"))
        self.setHoverBackgroundColor(QColor(232, 17, 35))
        self.setPressedBackgroundColor(QColor(241, 112, 122))

