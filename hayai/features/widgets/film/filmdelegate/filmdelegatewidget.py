from typing import Optional
from PyQt6.QtCore import QModelIndex, QRect, QSize, Qt
from PyQt6.QtGui import QColor, QFont, QFontMetrics, QIcon, QPainter 
from PyQt6.QtWidgets import   QStyleOptionViewItem, QStyledItemDelegate, QWidget

class QFilmDelegate(QStyledItemDelegate):

    def __init__(self, parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex): 
        icon: QIcon = index.data(Qt.ItemDataRole.DecorationRole) 
        iconRatio = option.decorationSize.height() / option.decorationSize.width()
        iconWidth: int = min(option.decorationSize.width(),option.rect.width())
        iconHeight: int = int(iconWidth * iconRatio)
        iconRect: QRect = QRect(option.rect.x(),option.rect.y(),iconWidth,iconHeight)
        painter.drawPixmap(iconRect,icon.pixmap(option.decorationSize))

        title: str = index.data(Qt.ItemDataRole.DisplayRole)  
        fontMetrics: QFontMetrics = option.fontMetrics
        titleSize: QSize = fontMetrics.size(Qt.TextFlag.TextSingleLine, title) 
        titleRect: QRect = QRect(option.rect.x(),iconRect.bottom() + 5,option.rect.width(),titleSize.height())
        font: QFont = QFont('Arial', 10)
        painter.setFont(font)
        painter.setPen(QColor("#a1acbc"))
        title = fontMetrics.elidedText(title, Qt.TextElideMode.ElideRight, titleRect.width()) 
        painter.drawText(titleRect,Qt.TextFlag.TextSingleLine,title) 

        extraData: str = index.data(Qt.ItemDataRole.UserRole)
        extraDataSize: QSize = fontMetrics.size(Qt.TextFlag.TextSingleLine, extraData) 
        extraDataRect: QRect = QRect(option.rect.x(),titleRect.bottom() + 5,option.rect.width(),extraDataSize.height())
        painter.setPen(QColor("white"))
        extraData = fontMetrics.elidedText(extraData, Qt.TextElideMode.ElideRight, titleRect.width()) 
        painter.drawText(extraDataRect,Qt.TextFlag.TextSingleLine,extraData) 

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:

        iconSize: QSize = option.decorationSize
        fontMetrics: QFontMetrics = option.fontMetrics
        title: str = index.data(Qt.ItemDataRole.DisplayRole)  
        titleSize: QSize = fontMetrics.size(Qt.TextFlag.TextSingleLine, title) 
        extraData: str = index.data(Qt.ItemDataRole.UserRole)  
        extraDataSize: QSize = fontMetrics.size(Qt.TextFlag.TextSingleLine, extraData) 
        height: int = iconSize.height() + titleSize.height() + extraDataSize.height() + 10
        width: int = iconSize.width()
        
        return QSize(width,height)
