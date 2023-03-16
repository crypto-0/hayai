from typing import Optional
from PyQt5.QtCore import QModelIndex, QRect, QSize, Qt
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QIcon, QPainter, QPalette, QPixmap, QTextOption
from PyQt5.QtWidgets import  QApplication, QStyleOptionViewItem, QStyledItemDelegate, QWidget

class QFilmDelegate(QStyledItemDelegate):

    def __init__(self, parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex): #pyright: ignore
        icon: QIcon = index.data(Qt.DecorationRole) #pyright: ignore
        iconRatio = option.decorationSize.height() / option.decorationSize.width()
        iconWidth: int = min(option.decorationSize.width(),option.rect.width())
        iconHeight: int = int(iconWidth * iconRatio)
        iconRect: QRect = QRect(option.rect.x(),option.rect.y(),iconWidth,iconHeight)
        painter.drawPixmap(iconRect,icon.pixmap(option.decorationSize))

        title: str = index.data(Qt.DisplayRole)  #pyright: ignore
        fontMetrics: QFontMetrics = option.fontMetrics
        titleSize: QSize = fontMetrics.size(Qt.TextSingleLine, title) #pyright: ignore
        titleRect: QRect = QRect(option.rect.x(),iconRect.bottom() + 5,option.rect.width(),titleSize.height())
        font: QFont = QFont('Arial', 10)
        painter.setFont(font)
        painter.setPen(QColor("#a1acbc"))
        title = fontMetrics.elidedText(title, Qt.ElideRight, titleRect.width()) #pyright: ignore
        painter.drawText(titleRect,Qt.TextSingleLine,title) #pyright: ignore

        extraData: str = index.data(Qt.UserRole) #pyright: ignore
        extraDataSize: QSize = fontMetrics.size(Qt.TextSingleLine, extraData) #pyright: ignore
        extraDataRect: QRect = QRect(option.rect.x(),titleRect.bottom() + 5,option.rect.width(),extraDataSize.height())
        painter.setPen(QColor("white"))
        extraData = fontMetrics.elidedText(extraData, Qt.ElideRight, titleRect.width()) #pyright: ignore
        painter.drawText(extraDataRect,Qt.TextSingleLine,extraData) #pyright: ignore

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:

        iconSize: QRect = option.decorationSize
        fontMetrics: QFontMetrics = option.fontMetrics
        title: str = index.data(Qt.DisplayRole)  #pyright: ignore
        titleSize: QSize = fontMetrics.size(Qt.TextSingleLine, title) #pyright: ignore
        extraData: str = index.data(Qt.UserRole)  #pyright: ignore
        extraDataSize: QSize = fontMetrics.size(Qt.TextSingleLine, extraData) #pyright: ignore
        height: int = iconSize.height() + titleSize.height() + extraDataSize.height() + 10
        width: int = iconSize.width()
        
        return QSize(width,height)

        
