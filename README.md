# Real Time Threatening Speech Detection

This project is a real-time voice threat detection system built using Django, Django Channels, TensorFlow, and TensorFlow Hub. It uses a pre-trained YAMNet model to extract audio features and a custom-trained TensorFlow model to classify the audio as either "Threat" or "Non-Threat".

## Features

- Real-time audio processing and classification
- WebSocket support for real-time communication
- TensorFlow model for efficient inference
- Docker support for easy deployment

## Project Structure

- `threat_detection/`: The main Django project directory.
  - `asgi.py`: ASGI configuration for Django Channels.
  - `settings.py`: Django settings.
  - `urls.py`: URL routing for the Django project.
  - `wsgi.py`: WSGI configuration for Django.
  - `routing.py`: ASGI routing configuration for Django Channels.
- `detector/`: The Django app for threat detection.
  - `consumers.py`: WebSocket consumer for processing audio data.
  - `models.py`: Django models (empty in this case).
  - `views.py`: Django views.
  - `templates/detector/index.html`: The main HTML template.
  - `static/detector/js/audio-processor.js`: JavaScript for audio processing.
  - `YAMNet Threatening Voice Classification.keras`: The custom-trained TensorFlow model.
- `manage.py`: Django's command-line utility.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Docker configuration.
- `start.sh`: Script to start the application.

## How It Works

### Frontend (index.html)

- The user interface allows the user to start and stop monitoring.
- When monitoring starts, the browser requests access to the microphone.
- Audio data is captured and processed using the Web Audio API and Audio Worklets.
- The audio data is encoded as WAV and sent to the server via WebSocket.

### WebSocket Consumer (consumers.py)

- The `AudioConsumer` class handles WebSocket connections.
- When audio data is received, it is processed in chunks.
- The audio data is converted to a NumPy array and normalized.
- Features are extracted using the YAMNet model from TensorFlow Hub.
- The features are padded or truncated to a fixed length.
- The padded features are passed to the custom-trained TensorFlow model for classification.
- The classification result ("Threat" or "Non-Threat") is sent back to the client via WebSocket.

### Backend (Django)

- Django serves the HTML template and static files.
- Django Channels handles WebSocket connections and routes them to the `AudioConsumer`.

## Setup and Installation

### Prerequisites

- Docker
- Python 3.10

### Installation

1. **Clone the repository**:

 ```bash
 git clone https://github.com/yourusername/threat_detection.git
 cd threat_detection
 ```
2. **Install dependencies**:

  ```bash
  pip install -r requirements.txt
  ```
3. **Run migrations and collect static files**:

  ```bash
  python manage.py migrate
  python manage.py collectstatic
  ```
4. **Start the application**:

  ```bash
  sh start.sh
  ```
### Docker
1. **Build the Docker image**:

  ```bash
  docker build -t threat_detection .
  ```
2. **Run the Docker container**:

  ```bash
  docker run -p 8000:8000 threat_detection
  ```
### Usage
1. **Access the application**: Open your browser and navigate to http://localhost:8000.
2. **Start Monitoring**: Click the "Start Monitoring" button to begin capturing and processing audio.
3. **View Results**: The application will display the classification result ("Threat" or "Non-Threat") in real-time.
  
