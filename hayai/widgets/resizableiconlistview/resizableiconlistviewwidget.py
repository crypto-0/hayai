import math
from typing import Optional
from PyQt5 import QtWidgets
from PyQt5.QtCore import  QEasingCurve, QEvent, QPropertyAnimation, QSize
from PyQt5.QtWidgets import  QListView, QSizePolicy, QWidget

class QResizableIconListView(QListView):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)


        self.showAll: bool = False
        self.iconSizeRatio: float = 1.5
        self.minimumIconSize: QSize = QSize(150,int(150 * 1.5))
        self.animation: QPropertyAnimation = QPropertyAnimation(self.horizontalScrollBar(), b"value")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)

        self.setLayoutMode(QListView.LayoutMode.Batched)
        self.setBatchSize(50)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setFlow(QListView.Flow.LeftToRight)
        self.setUniformItemSizes(True)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setIconSize(self.minimumIconSize)
        self.setSpacing(5)
        self.setContentsMargins(0,0,0,0)
        self.setWordWrap(True)
        self.viewport().installEventFilter(self)
        self.setObjectName("QResizableIconListView")
        self.currentIconSize: QSize = self.iconSize()
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

    def setMinimumIconSize(self,width: int, height: int):
        self.minimumIconSize.setWidth(width)
        self.minimumIconSize.setHeight(height)

    def setShowAll(self,showAll: bool):
        self.showAll = showAll

    def setIconRatio(self,ratio: float):
        self.iconSizeRatio = ratio

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
        if obj is self.viewport() and event.type() == QEvent.Resize: #pyright: ignore
            viewport_width = self.viewport().width()
            frameWidth = self.frameWidth()
            model = self.model()
            if  model.rowCount() > 1 :
                item_spacing = self.spacing() 
                available_width = viewport_width - (frameWidth * 2) - (item_spacing * 2)
                max_items_per_row = available_width // self.minimumIconSize.width() 
                if max_items_per_row > 1:
                    iconWidth = (available_width // max_items_per_row ) - ( item_spacing) - (frameWidth * 4) 
                else:
                    iconWidth = self.minimumIconSize.width() - (item_spacing ) - (frameWidth * 4) 
                iconHeight = int(iconWidth * self.iconSizeRatio)
                iconSize = QSize(iconWidth,iconHeight) 
                self.setIconSize(iconSize)
                #self.updateGeometry()
            if self.showAll:
                rowHeight = self.sizeHintForRow(0)
                colWidth = self.sizeHintForColumn(0)
                numCols: int = self.width() // colWidth
                numCols = max(1,numCols)
                rows: int = math.ceil(model.rowCount()/ numCols)
                totalHeight = rowHeight * rows
                self.setMinimumHeight(totalHeight)

        return super().eventFilter(obj, event)
