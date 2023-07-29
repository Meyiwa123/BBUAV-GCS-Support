from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class DataVisualizationPage(QWidget):
    def __init__(self, vehicle):
        super().__init__()

        self.vehicle = vehicle

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Data Visualization")
        layout = QVBoxLayout()

        # Create a Matplotlib figure and axes for the graph
        self.figure, self.axes = plt.subplots(figsize=(8, 6))
        self.axes.set_title("Throttle, Pitch, Roll, and Yaw Over Time")
        self.axes.set_xlabel("Time (seconds)")
        self.axes.set_ylabel("Value")

        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Labels to display pitch, roll, and yaw angles
        self.pitch_label = QLabel("Pitch: N/A")
        layout.addWidget(self.pitch_label)

        self.roll_label = QLabel("Roll: N/A")
        layout.addWidget(self.roll_label)

        self.yaw_label = QLabel("Yaw: N/A")
        layout.addWidget(self.yaw_label)

        self.setLayout(layout)

        # Start receiving data from the vehicle
        if self.vehicle is not None:
            self.start_receiving_data()

    def start_receiving_data(self):
        # Subscribe to the ATTITUDE message to receive pitch, roll, and yaw data
        self.vehicle.add_message_listener("ATTITUDE", self.handle_attitude_message)
        # Subscribe to the RC_CHANNELS message to receive throttle data
        self.vehicle.add_message_listener("RC_CHANNELS", self.handle_rc_channels_message)

    def handle_attitude_message(self, message):
        # Update the pitch, roll, and yaw labels with the received data
        pitch_degrees = round(message.pitch * 180 / 3.14159, 2)
        roll_degrees = round(message.roll * 180 / 3.14159, 2)
        yaw_degrees = round(message.yaw * 180 / 3.14159, 2)

        self.pitch_label.setText(f"Pitch: {pitch_degrees} degrees")
        self.roll_label.setText(f"Roll: {roll_degrees} degrees")
        self.yaw_label.setText(f"Yaw: {yaw_degrees} degrees")

    def handle_rc_channels_message(self, message):
        # Update the throttle value in the graph
        time = message.time_boot_ms * 1e-3
        throttle = message.chan4_raw

        self.axes.plot(time, throttle, 'y.', label="Throttle")

        self.axes.legend()
        self.canvas.draw()
