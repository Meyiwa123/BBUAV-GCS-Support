from pymavlink import mavutil
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, \
    QPushButton, QDialog, QLineEdit, QRadioButton, QMessageBox

class MissionPlanningPage(QWidget):
    def __init__(self, vehicle):
        super().__init__()

        self.missions_data = []
        self.vehicle = vehicle

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Mission Planning")
        layout = QVBoxLayout()

        # List of missions
        self.missions_list = QListWidget()
        self.update_missions_list()
        layout.addWidget(self.missions_list)

        # Buttons to create, delete, and edit missions
        buttons_layout = QHBoxLayout()
        self.create_button = QPushButton("Create Mission")
        self.delete_button = QPushButton("Delete Mission")
        self.edit_button = QPushButton("Edit Mission")
        self.uplad_mission = QPushButton("Upload Mission")
        buttons_layout.addWidget(self.create_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.uplad_mission)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Connect button signals to corresponding functions
        self.create_button.clicked.connect(self.create_mission)
        self.delete_button.clicked.connect(self.delete_mission)
        self.edit_button.clicked.connect(self.edit_mission)
        self.uplad_mission.clicked.connect(self.upload_mission)

    def update_missions_list(self):
        self.missions_list.clear()
        for idx, mission_data in enumerate(self.missions_data, start=1):
            mission_info = f"Mission {idx}:"
            waypoint = mission_data["waypoint"]
            latitude_info = f"Latitude: {waypoint[0]}"
            longitude_info = f"Longitude: {waypoint[1]}"
            altitude_info = f"Altitude: {waypoint[2]}"
            mission_type_info = f"Mission Type: {mission_data['mission_type']}"

            mission_label = QLabel(mission_info)
            latitude_label = QLabel(latitude_info)
            longitude_label = QLabel(longitude_info)
            altitude_label = QLabel(altitude_info)
            mission_type_label = QLabel(mission_type_info)

            # Create a container widget for the mission item
            container_widget = QWidget()
            container_layout = QVBoxLayout()
            container_layout.addWidget(mission_label)
            container_layout.addWidget(latitude_label)
            container_layout.addWidget(longitude_label)
            container_layout.addWidget(altitude_label)
            container_layout.addWidget(mission_type_label)
            container_widget.setLayout(container_layout)

            # Set the size hint for the list widget item
            item = QListWidgetItem(self.missions_list)
            item.setSizeHint(container_widget.sizeHint())
            self.missions_list.addItem(item)
            self.missions_list.setItemWidget(item, container_widget)

    def create_mission(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Create Waypoint")
        dialog_layout = QVBoxLayout()

        latitude_label = QLabel("Latitude:")
        self.latitude_input = QLineEdit()
        dialog_layout.addWidget(latitude_label)
        dialog_layout.addWidget(self.latitude_input)

        longitude_label = QLabel("Longitude:")
        self.longitude_input = QLineEdit()
        dialog_layout.addWidget(longitude_label)
        dialog_layout.addWidget(self.longitude_input)

        altitude_label = QLabel("Altitude:")
        self.altitude_input = QLineEdit()
        dialog_layout.addWidget(altitude_label)
        dialog_layout.addWidget(self.altitude_input)

        # Mission type selection
        mission_type_label = QLabel("Mission Type:")
        self.takeoff_radio = QRadioButton("Takeoff")
        self.flight_radio = QRadioButton("Flight")
        self.land_radio = QRadioButton("Land")

        mission_type_layout = QHBoxLayout()
        mission_type_layout.addWidget(mission_type_label)
        mission_type_layout.addWidget(self.takeoff_radio)
        mission_type_layout.addWidget(self.flight_radio)
        mission_type_layout.addWidget(self.land_radio)

        dialog_layout.addLayout(mission_type_layout)

        create_button = QPushButton("Create")
        create_button.clicked.connect(self.add_waypoint)
        dialog_layout.addWidget(create_button)

        dialog.setLayout(dialog_layout)
        dialog.exec()

    def add_waypoint(self):
        # Check if a mission type is selected
        if not self.takeoff_radio.isChecked() and not self.flight_radio.isChecked() and not self.land_radio.isChecked():
            QMessageBox.warning(self, "Error", "Please select a mission type.")
            return

        latitude_text = self.latitude_input.text()
        longitude_text = self.longitude_input.text()
        altitude_text = self.altitude_input.text()

        try:
            latitude = float(latitude_text)
            longitude = float(longitude_text)
            altitude = float(altitude_text)

            # Determine the selected mission type
            mission_type = None
            if self.takeoff_radio.isChecked():
                mission_type = "Takeoff"
            elif self.flight_radio.isChecked():
                mission_type = "Flight"
            elif self.land_radio.isChecked():
                mission_type = "Land"

            # Create a new mission with the waypoint and mission type
            new_mission = {"waypoint": (latitude, longitude, altitude), "mission_type": mission_type}
            self.missions_data.append(new_mission)

            self.update_missions_list()

        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid input. Please enter valid numbers for latitude, longitude, and altitude.")

        # Close the pop-up dialog after creating a new mission
        self.sender().parent().close()

    def delete_mission(self):
        selected_item = self.missions_list.currentItem()
        if selected_item:
            idx = self.missions_list.currentRow()
            if 0 <= idx < len(self.missions_data):
                del self.missions_data[idx]
                self.update_missions_list()

    def edit_mission(self):
        selected_item = self.missions_list.currentItem()
        if selected_item:
            idx = self.missions_list.currentRow()
            if 0 <= idx < len(self.missions_data):
                mission_data = self.missions_data[idx]
                waypoint = mission_data["waypoint"]

                dialog = QDialog(self)
                dialog.setWindowTitle("Edit Mission Parameters")
                dialog_layout = QVBoxLayout()

                latitude_label = QLabel("Latitude:")
                self.latitude_input = QLineEdit(str(waypoint[0]))
                dialog_layout.addWidget(latitude_label)
                dialog_layout.addWidget(self.latitude_input)

                longitude_label = QLabel("Longitude:")
                self.longitude_input = QLineEdit(str(waypoint[1]))
                dialog_layout.addWidget(longitude_label)
                dialog_layout.addWidget(self.longitude_input)

                altitude_label = QLabel("Altitude:")
                self.altitude_input = QLineEdit(str(waypoint[2]))
                dialog_layout.addWidget(altitude_label)
                dialog_layout.addWidget(self.altitude_input)

                # Mission type selection
                mission_type_label = QLabel("Mission Type:")
                self.takeoff_radio = QRadioButton("Takeoff")
                self.flight_radio = QRadioButton("Flight")
                self.land_radio = QRadioButton("Land")

                mission_type_layout = QHBoxLayout()
                mission_type_layout.addWidget(mission_type_label)
                mission_type_layout.addWidget(self.takeoff_radio)
                mission_type_layout.addWidget(self.flight_radio)
                mission_type_layout.addWidget(self.land_radio)

                dialog_layout.addLayout(mission_type_layout)

                # Set the selected mission type based on the existing mission data
                mission_type = mission_data["mission_type"]
                if mission_type == "Takeoff":
                    self.takeoff_radio.setChecked(True)
                elif mission_type == "Flight":
                    self.flight_radio.setChecked(True)
                elif mission_type == "Land":
                    self.land_radio.setChecked(True)

                confirm_button = QPushButton("Confirm")
                confirm_button.clicked.connect(lambda: self.confirm_edit_mission(dialog, idx))
                dialog_layout.addWidget(confirm_button)

                dialog.setLayout(dialog_layout)
                dialog.exec()

    def confirm_edit_mission(self, dialog, idx):
        mission_data = self.missions_data[idx]

        # Check if a mission type is selected
        if not self.takeoff_radio.isChecked() and not self.flight_radio.isChecked() and not self.land_radio.isChecked():
            QMessageBox.warning(self, "Error", "Please select a mission type.")
            return

        try:
            new_latitude = float(self.latitude_input.text())
            new_longitude = float(self.longitude_input.text())
            new_altitude = float(self.altitude_input.text())

            # Determine the selected mission type
            mission_type = None
            if self.takeoff_radio.isChecked():
                mission_type = "Takeoff"
            elif self.flight_radio.isChecked():
                mission_type = "Flight"
            elif self.land_radio.isChecked():
                mission_type = "Land"
            
            mission_data["waypoint"] = (new_latitude, new_longitude, new_altitude)
            mission_data["mission_type"] = mission_type
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid input. Please enter valid numbers for latitude, longitude, and altitude.")
            return

        self.update_missions_list()
        dialog.close()

    def upload_mission(self):
        if self.vehicle is None:
            QMessageBox.warning(self, "Error", "No vehicle connected.")
            return
        if len(self.missions_data) == 0 :
            QMessageBox.warning(self, "Error", "No mission added.")
            return
        
        cmds = []
        for mission in self.missions_data:
            # Retrieve latitude, longitude, and altitude from the mission dictionary
            latitude, longitude, altitude = mission["waypoint"]
            # Retrieve the mission type from the mission dictionary
            mission_type = mission["mission_type"]

            # Create a command based on the mission type
            cmd = None
            if mission_type == "Takeoff":
                # Handle takeoff mission
                cmd = self.vehicle.message_factory.command_long_encode(
                    0, 0,
                    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                    0, 0, 0, 0, 0, 0, 0, 0, altitude
                )
            elif mission_type == "Flight":
                # Handle flight mission
                cmd = self.vehicle.message_factory.command_long_encode(
                    0, 0,
                    mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                    0, 0, 0, 0, 0, 0, latitude, longitude, altitude
                )
            elif mission_type == "Land":
                # Handle land mission
                cmd = self.vehicle.message_factory.command_long_encode(
                    0, 0,
                    mavutil.mavlink.MAV_CMD_NAV_LAND,
                    0, 0, 0, 0, 0, 0, latitude, longitude, 0
                )

            # Add the command to the list of mission commands
            cmds.append(cmd)
        
        # Upload the mission to the vehicle
        self.vehicle.send_mavlink(cmds)