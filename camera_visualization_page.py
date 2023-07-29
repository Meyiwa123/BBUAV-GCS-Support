import os, cv2
from logger import logger
from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QSlider, QFileDialog, QHBoxLayout, QLineEdit, QPushButton

class CameraVisualizationPage(QWidget):
    def __init__(self):
        super().__init__()

        self.capture = None  # OpenCV capture object to access the camera feed
        self.brightness = 50  # Default brightness value
        self.contrast = 50  # Default contrast value
        self.is_recording = False  # Flag to indicate if video recording is in progress

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Camera Visualization")
        layout = QVBoxLayout()

        self.camera_label = QLabel("Camera Feed")
        layout.addWidget(self.camera_label)
        self.video_path_input = QLineEdit()
        layout.addWidget(self.video_path_input)

        # Create a horizontal layout for the connection input and button
        connection_layout = QHBoxLayout()
        self.camera_url_input = QLineEdit()
        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.connect_to_camera)
        connection_layout.addWidget(self.camera_url_input)
        connection_layout.addWidget(connect_button)

        layout.addLayout(connection_layout)

        # Create sliders for adjusting camera parameters
        brightness_label = QLabel("Brightness:")
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.brightness_slider.setRange(0, 100)
        self.brightness_slider.setValue(self.brightness)
        self.brightness_slider.valueChanged.connect(self.update_brightness)

        contrast_label = QLabel("Contrast:")
        self.contrast_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.contrast_slider.setRange(0, 100)
        self.contrast_slider.setValue(self.contrast)
        self.contrast_slider.valueChanged.connect(self.update_contrast)

        layout.addWidget(brightness_label)
        layout.addWidget(self.brightness_slider)
        layout.addWidget(contrast_label)
        layout.addWidget(self.contrast_slider)

        # Create buttons for starting and stopping recording
        self.start_record_button = QPushButton("Start Recording")
        self.stop_record_button = QPushButton("Stop Recording")
        self.configure_save_path_button = QPushButton("Configure Save Path")
        self.start_record_button.setEnabled(False)  # Disable start button initially
        self.stop_record_button.setEnabled(False)  # Disable stop button initially
        self.start_record_button.clicked.connect(self.start_recording)
        self.stop_record_button.clicked.connect(self.stop_recording)
        self.configure_save_path_button.clicked.connect(self.configure_save_path)

        # Create a horizontal layout for the recording buttons
        record_buttons_layout = QHBoxLayout()
        record_buttons_layout.addWidget(self.start_record_button)
        record_buttons_layout.addWidget(self.stop_record_button)
        record_buttons_layout.addWidget(self.configure_save_path_button)
        layout.addLayout(record_buttons_layout)

        self.setLayout(layout)

    def configure_save_path(self):
        logger.info("Configure save path button clicked.")
        selected_directory = QFileDialog.getExistingDirectory(self, "Select Directory")

        # Update the video path input with the selected directory
        if selected_directory:
            self.video_path_input.setText(str(selected_directory))

    def start_recording(self):
        logger.info("Start recording button clicked.")
        if self.capture is not None and not self.is_recording:
            # Get the user-defined video path from the input field
            video_path = self.video_path_input.text()

            # If the video path is empty, use the default path (current working directory)
            if not video_path:
                video_path = os.getcwd()

            # Create the directory if it doesn't exist
            os.makedirs(video_path, exist_ok=True)

            # Get the current time and set it as the default filename
            current_time = QTime.currentTime().toString("hh-mm-ss")
            video_filename = f"{current_time}.avi"

            # Get the resolution of the camera feed
            width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            size = (width, height)

            # Create a VideoWriter object to save the video
            video_format = cv2.VideoWriter_fourcc(*"MJPG")
            self.video_writer = cv2.VideoWriter(os.path.join(video_path, video_filename), video_format, 10, size)
            self.is_recording = True

            # Disable the start button and enable the stop button during recording
            self.start_record_button.setEnabled(False)
            self.stop_record_button.setEnabled(True)

    def stop_recording(self):
        logger.info("Stop recording button clicked.")
        if self.capture is not None and self.is_recording:
            self.is_recording = False

            # Release the VideoWriter object
            self.video_writer.release()
            self.video_writer = None

            # Enable the start button and disable the stop button after recording
            self.start_record_button.setEnabled(True)
            self.stop_record_button.setEnabled(False)

    def connect_to_camera(self):
        logger.info("Connect to camera button clicked.")
        # Get the camera URL from the input field
        camera_url = self.camera_url_input.text()

        # Release any existing camera capture
        if self.capture is not None:
            self.capture.release()

        # Check if the input an integer
        if camera_url.isdigit():
            camera_url = int(camera_url)

        try:
            # Try to open the camera using the URL
            self.capture = cv2.VideoCapture(camera_url)

            if self.capture.isOpened():
                # If the camera is opened successfully, start the camera feed update loop
                self.update_camera_feed()
                # Enable the start button after connecting to the camera
                self.start_record_button.setEnabled(True)
            else:
                # If the camera couldn't be opened, display an error message
                self.camera_label.setText("Error: Failed to connect to the camera")
        except Exception as e:
            # Display the error message if there's an exception
            self.camera_label.setText(f"Error: {str(e)}")

    def update_camera_feed(self):
        if self.capture is not None:
            ret, frame = self.capture.read()
            if ret:
                # Apply brightness and contrast adjustments to the camera frame
                adjusted_frame = self.adjust_brightness_contrast(frame)

                # Convert the frame to RGB color space and show it on the QLabel
                rgb_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                q_img = QImage(rgb_frame.data, w, h, ch * w, QImage.Format.Format_RGB888)
                self.camera_label.setPixmap(QPixmap.fromImage(q_img))

                # If recording is in progress, save the frame to the video file
                if self.is_recording and self.video_writer is not None:
                    self.video_writer.write(adjusted_frame)
        # Schedule the next frame update after a delay (e.g., 30ms)
        QTimer.singleShot(30, self.update_camera_feed)

    def adjust_brightness_contrast(self, frame):
        alpha = (self.contrast + 100) / 100.0
        beta = self.brightness - 50

        return cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    def update_brightness(self, value):
        logger.info(f"Updated brightness value: {value}")
        self.brightness = value

    def update_contrast(self, value):
        logger.info(f"Updated contrast value: {value}")
        self.contrast = value

    def closeEvent(self, event):
        logger.info("Closing CameraVisualizationPage.")
        # Release the OpenCV capture object and the video writer if they are active
        if self.capture is not None:
            self.capture.release()

        if self.video_writer is not None:
            self.video_writer.release()

        # Call the base class closeEvent to properly close the widget
        super().closeEvent(event)
