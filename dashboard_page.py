from pymavlink import mavutil
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QComboBox, QPushButton, QMessageBox, QDialog, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
import folium
import geocoder

class MapWidget(QWebEngineView):
    def __init__(self):
        super().__init__()

        self.drone_marker = None
        self.init_map()

    def init_map(self):
        # Create a map centered at a default location
        self.map = folium.Map(location=[51.5074, -0.1278], zoom_start=10)

        # Convert the folium map to HTML and load it into the web view
        map_html = self.map._repr_html_()
        self.setHtml(map_html)

    def update_drone_location(self, latitude, longitude):
        # Remove the previous drone marker if it exists
        if self.drone_marker:
            self.map.get_root().add_child(self.drone_marker)
            self.drone_marker = None

        # Create a marker with a custom drone icon at the drone's location
        drone_icon = folium.features.CustomIcon(icon_image='assets/drone_icon.png', icon_size=(50, 50))
        self.drone_marker = folium.Marker([latitude, longitude], icon=drone_icon)

        # Add the drone marker to the map
        self.map.get_root().add_child(self.drone_marker)

        # Convert the updated folium map to HTML and reload it into the web view
        map_html = self.map._repr_html_()
        self.setHtml(map_html)

    def show_user_location(self):
        # Get the user's current location using geocoder based on their IP address
        g = geocoder.ip('me')
        user_latitude, user_longitude = g.latlng

        # Create a marker for the user's location
        user_marker = folium.Marker([user_latitude, user_longitude], popup='Your Location')

        # Add the user marker to the map
        self.map.get_root().add_child(user_marker)

        # Set the map view to the user's location
        self.map.location = [user_latitude, user_longitude]
        self.map.zoom_start = 12

        # Convert the updated folium map to HTML and reload it into the web view
        map_html = self.map._repr_html_()
        self.setHtml(map_html)


class DashboardPage(QWidget):
    def __init__(self, vehicle):
        super().__init__()

        self.vehicle = vehicle
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Dashboard")
        layout = QVBoxLayout()

        # Connection section in the header
        connection_layout = QHBoxLayout()

        self.connection_type_dropdown = QComboBox()
        self.connection_type_dropdown.addItems(["UDP", "TCP"])
        connection_layout.addWidget(self.connection_type_dropdown)

        self.connect_button = QPushButton("Connect to Drone")
        self.connect_button.clicked.connect(self.show_connection_dialog)
        connection_layout.addWidget(self.connect_button)

        layout.addLayout(connection_layout)

        # Add the map widget to the layout
        self.map_widget = MapWidget()
        layout.addWidget(self.map_widget)

        # Add a label for the drone's location
        self.update_map(drone_connected=False)

        # Add a label for weather information
        self.weather_label = QLabel("Weather: N/A")
        # Update the weather information
        self.update_weather_info()
        layout.addWidget(self.weather_label)

        self.setLayout(layout)

    def show_connection_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Connect to Drone")
        dialog_layout = QVBoxLayout()

        hostname_label = QLabel("Hostname/IP:")
        self.hostname_input = QLineEdit()
        dialog_layout.addWidget(hostname_label)
        dialog_layout.addWidget(self.hostname_input)

        port_label = QLabel("Port:")
        self.port_input = QLineEdit()
        dialog_layout.addWidget(port_label)
        dialog_layout.addWidget(self.port_input)

        confirm_button = QPushButton("Connect")
        confirm_button.clicked.connect(self.connect_to_drone)
        dialog_layout.addWidget(confirm_button)

        dialog.setLayout(dialog_layout)
        dialog.exec()

    def connect_to_drone(self):
        hostname = self.hostname_input.text()
        port_number = self.port_input.text()

        if not hostname or not port_number:
            QMessageBox.warning(self, "Error", "Please enter the hostname/IP and port number.")
            return

        try:
            port = int(port_number)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid port number. Please enter a valid integer.")
            return

        connection_type = self.connection_type_dropdown.currentText()
        connection_string = f"{connection_type.lower()}:{hostname}:{port}"

        # Establish connection using MAVLink
        try:
            self.vehicle = mavutil.mavlink_connection(connection_string)
            QMessageBox.information(self, "Success", "Connected to the drone successfully.")
            self.show_connection_status(hostname, port)
            self.vehicle.add_message_listener('GLOBAL_POSITION_INT', self.on_global_position_int)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to the drone: {str(e)}")

    def show_connection_status(self, hostname, port):
        status_label = QLabel(f"Connected to Drone on {hostname} port {port}")
        layout = self.layout()
        layout.insertWidget(0, status_label)  # Insert the status label at the top

    def update_map(self, drone_connected, latitude=None, longitude=None):
        if drone_connected:
            self.map_widget.update_drone_location(latitude, longitude)
        else:
            self.map_widget.show_user_location()

    def update_weather_info(self):
        # Get the weather information using the OpenWeatherMap API
        pass

    def on_global_position_int(self, _, msg):
        # Callback function to receive the GLOBAL_POSITION_INT message and update the map
        latitude = msg.lat / 1e7
        longitude = msg.lon / 1e7
        self.update_map(drone_connected=True, latitude=latitude, longitude=longitude)
