# ![logo](assets\bbuav.jpg) BBUAV GCS Support

BBUAV GCS Support is a ground control station application designed to provide comprehensive support and control for unmanned aerial vehicles (UAVs) or drones. The project aims to offer a user-friendly interface that facilitates mission planning, monitoring, and weather information retrieval for drone operations.

## Features
* **Drone Connection:** Connect to UAVs through UDP or TCP communication protocols, enabling real-time communication with the drone.
* **Mission Planning:** Create, edit, and delete waypoints to design custom missions for the drone, specifying takeoff, flight, and landing points.
* **Live Drone Tracking:** Visualize the real-time location of the drone on a map with a custom drone icon, allowing users to monitor the drone's position during missions.
* **Camera Visualization:** Display, adjust and save a video stream of the provided camera's url for ease of reference and navigation.
* **Data Visualization:** Retrieve information of the connected vehicle, providing crucial information for mission debugging.

## Getting Started
### Prerequisites
* Python
* PyQt6
* PyMavlink
* PyQtWebEngine
* Folium
* Geocoder

### Installation
1. Clone the repository: 
`git clone https://github.com/meyiwa123/bbuav-gcs-support.git`
2. Activate the virtual environment 
`venv\Scripts\activate`
3. Run the application: 
`python main.py`

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
This project is provided "as is," and the developers make no warranties regarding its functionality. The use of BBUAV GCS Support is at the user's own risk.