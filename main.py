import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QStackedWidget, QPushButton, QWidget
from dashboard_page import DashboardPage
from mission_planning_page import MissionPlanningPage
from camera_visualization_page import CameraVisualizationPage
from data_visualization_page import DataVisualizationPage
from settings_page import SettingsPage

class GroundStationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BlackBird Ground Station")
        self.setGeometry(100, 100, 1000, 800)

        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.stacked_widget  = QStackedWidget()

        # Initialize the vehicle
        self.vehicle = None

        # Initialize the pages
        dashboard_page = DashboardPage(self.vehicle)
        mission_planning_page = MissionPlanningPage(self.vehicle)
        camera_visualization_page = CameraVisualizationPage()
        data_visualization_page = DataVisualizationPage(self.vehicle)
        settings_page = SettingsPage()

        self.stacked_widget.addWidget(dashboard_page)
        self.stacked_widget.addWidget(mission_planning_page)
        self.stacked_widget.addWidget(camera_visualization_page)
        self.stacked_widget.addWidget(data_visualization_page)
        self.stacked_widget.addWidget(settings_page)

        layout.addWidget(self.stacked_widget)

        # Add buttons to switch between pages
        self.dashboard_button = QPushButton("Dashboard")
        self.mission_planning_button = QPushButton("Mission Planning")
        self.camera_visualization_button = QPushButton("Camera Visualization")
        self.data_visualization_button = QPushButton("Data Visualization")
        self.settings_button = QPushButton("Settings")

        # Connect buttons to their corresponding page
        self.dashboard_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.mission_planning_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.camera_visualization_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.data_visualization_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.settings_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

        # Add buttons to the layout
        layout.addWidget(self.dashboard_button)
        layout.addWidget(self.mission_planning_button)
        layout.addWidget(self.camera_visualization_button)
        layout.addWidget(self.data_visualization_button)
        layout.addWidget(self.settings_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GroundStationApp()
    window.setFixedSize
    window.show()
    sys.exit(app.exec())