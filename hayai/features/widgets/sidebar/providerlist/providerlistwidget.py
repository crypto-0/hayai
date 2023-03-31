from typing import Optional
from typing import List
from PyQt6.QtCore import QSize, Qt

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QGroupBox, QSizePolicy, QVBoxLayout, QWidget
from PyQt6.QtWidgets import QPushButton

class QProviderList(QGroupBox):

    def __init__(self,providers: List[str],parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        providerButtons: List[QPushButton] = list(map(self.createProviderButton,providers))

        providerListLayout: QVBoxLayout = QVBoxLayout()
        for providerButton in providerButtons:
            providerListLayout.addWidget(providerButton)
        providerListLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) 
        providerListLayout.setContentsMargins(0,0,0,0)
        providerListLayout.setSpacing(20)
        self.setLayout(providerListLayout)

        self.setCheckable(False)
        self.setFlat(True)
        self.setObjectName("QProviderList")

    def createProviderButton(self,provider: str):
            providerButton: QPushButton =QPushButton()
            iconLocation = f"hayai/features/widgets/sidebar/assets/icons/{provider}.png"
            providerButton.setIcon(QIcon(iconLocation))
            providerButton.setIconSize(QSize(30,30))
            providerButton.setFlat(True)
            providerButton.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
            return providerButton



