from typing import Optional
from PyQt5.QtCore import  QEasingCurve, QEvent, QPropertyAnimation, QSize
from PyQt5.QtWidgets import  QListView, QWidget

from ..filmlistmodel import QFilmListModel

class QFilmListView(QListView):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        self.minimunIconSize: QSize = QSize(150,int(150 * 1.5))
        self.animation: QPropertyAnimation = QPropertyAnimation(self.horizontalScrollBar(), b"value")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)

        self.setLayoutMode(QListView.LayoutMode.Batched)
        self.setBatchSize(50)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setFlow(QListView.Flow.LeftToRight)
        self.setUniformItemSizes(True)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setIconSize(self.minimunIconSize)
        self.setSpacing(0)
        self.setContentsMargins(0,0,0,0)
        self.setWordWrap(True)
        self.viewport().installEventFilter(self)
        self.setObjectName("QFilmListView")
        self.currentIconSize: QSize = self.iconSize()
        self.setAutoScroll(True)
        #self.setFrameStyle(QFrame.NoFrame)

    def sizeHint(self) -> QSize:
        size: QSize = super().sizeHint()
        fontHeight: int = self.fontMetrics().height() * 2
        size.setHeight(self.iconSize().height() + self.frameWidth() * 2 +  fontHeight + self.spacing())
        return size

    def minimumSizeHint(self) -> QSize:
            return self.sizeHint()

    def scrollRight(self):
        currentPos = self.horizontalScrollBar().value()
        pageSize = self.horizontalScrollBar().pageStep()
        scrollPos = currentPos + pageSize

        self.animation.stop()
        self.animation.setStartValue(currentPos)
        self.animation.setEndValue(scrollPos)
        self.animation.start()

    def scrollLeft(self):
        currentPos = self.horizontalScrollBar().value()
        pageSize = self.horizontalScrollBar().pageStep()
        scrollPos = currentPos - pageSize

        self.animation.stop()
        self.animation.setStartValue(currentPos)
        self.animation.setEndValue(scrollPos)
        self.animation.start()

    def eventFilter(self, obj, event):
        if obj is self.viewport() and event.type() == QEvent.Resize: #pyright: ignore
            viewport_width = self.viewport().width()
            frameWidth = self.frameWidth()
            model = self.model()
            if isinstance(model,QFilmListModel ) and model.rowCount() > 1 :
                item_spacing = self.spacing() 
                available_width = viewport_width - (frameWidth * 2) - (item_spacing)
                max_items_per_row = available_width // self.minimunIconSize.width() 
                if max_items_per_row > 0:
                    iconWidth = (available_width // max_items_per_row ) - ( item_spacing ) - (frameWidth * 4)
                else:
                    iconWidth = self.minimunIconSize.width() - (item_spacing ) - (frameWidth * 4)
                iconHeight = int(iconWidth * 1.5)
                iconSize = QSize(iconWidth,iconHeight) 
                model.iconSize = iconSize
                self.setIconSize(iconSize)
                self.updateGeometry()

        return super().eventFilter(obj, event)
