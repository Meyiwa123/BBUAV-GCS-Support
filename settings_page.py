from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.label = QLabel("This is the Settings Page")
        layout.addWidget(self.label)

        self.setLayout(layout)
