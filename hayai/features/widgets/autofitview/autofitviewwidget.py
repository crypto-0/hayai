import math
from typing import Optional
from PyQt6 import QtWidgets
from PyQt6.QtCore import  QEasingCurve, QEvent, QPropertyAnimation, QSize, Qt
from PyQt6.QtWidgets import  QListView, QWidget

class QAutoFitView(QListView):

    def __init__(self, minimumIconSize: QSize = QSize(150,225),showAll = False,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)


        self.showAll: bool = showAll
        self.iconSizeRatio: float = minimumIconSize.height() / minimumIconSize.width()
        self.minimumIconSize: QSize = minimumIconSize
        self.animation: QPropertyAnimation = QPropertyAnimation(self.horizontalScrollBar(), b"value") #pyright: ignore
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.setLayoutMode(QListView.LayoutMode.Batched)
        self.setBatchSize(50)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setFlow(QListView.Flow.LeftToRight)
        self.setUniformItemSizes(True)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setWordWrap(False)
        self.setWrapping(False)
        self.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.setIconSize(self.minimumIconSize)
        self.setSpacing(10)
        self.setContentsMargins(0,0,0,0)
        self.viewport().installEventFilter(self)
        self.setObjectName("QAutoFitView")
        self.currentIconSize: QSize = self.iconSize()
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.setAutoScroll(False)
        self.resize(QSize(0,0))


    def sizeHint(self) -> QSize:
        size: QSize = super().sizeHint()
        fontHeight: int = self.fontMetrics().height() * 2
        size.setHeight(self.iconSize().height() + self.frameWidth() * 2 +  fontHeight + self.spacing() + 10) 
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
        if obj is self.viewport() and event.type() == QEvent.Type.Resize: #pyright: ignore
            viewport_width = self.viewport().width()
            frameWidth = self.frameWidth()
            model = self.model()
            itemSpacing = self.spacing() 
            availableWidth = viewport_width - (frameWidth * 2) - (itemSpacing * 2) - self.verticalScrollBar().width()
            maxItemPerRow = availableWidth // self.minimumIconSize.width() 
            if maxItemPerRow > 1:
                iconWidth = (availableWidth // maxItemPerRow ) -(itemSpacing)
            else:
                iconWidth = self.minimumIconSize.width() - (itemSpacing * 2 ) - (frameWidth * 2) 
            iconHeight = int(iconWidth * self.iconSizeRatio)
            iconSize = QSize(iconWidth,iconHeight) 
            self.setIconSize(iconSize)

            if self.showAll:
                rowHeight = self.sizeHintForRow(0)
                colWidth = max(self.sizeHintForColumn(0),1)
                numCols: int = self.width() // colWidth
                numCols = max(1,numCols)
                rows: int = math.ceil(model.rowCount()/ numCols)
                totalHeight = rowHeight * rows
                self.setMinimumHeight(totalHeight)
            return True

        return super().eventFilter(obj, event)
    def scrollToTop(self):
        print("here at the top")
