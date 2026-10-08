# Mumbai Metro Route Navigator 

A full-stack web application that helps users find the optimal travel route across the Mumbai Metro network. The application leverages graph theory to calculate the shortest paths and minimum stops while providing an interactive map visualization.

# Features

Optimal Routing: Choose between "Fastest Time" (Dijkstra's Algorithm) or "Minimum Stops" (Breadth-First Search).

Interactive Map: Built with Leaflet.js and OpenStreetMap to visualize the exact route, including stations and track lines.

Smart Interchanges: Automatically calculates when a user needs to change lines and provides explicit interchange instructions.

Color-Coded UI: Metro lines are visually distinct (e.g., Blue Line 1, Yellow Line 2A, Red Line 7) on both the map and the step-by-step itinerary.

# Tech Stack

Frontend:

HTML5, CSS3, Vanilla JavaScript

Leaflet.js (Map Rendering)

Backend:

Python 3.x

FastAPI (RESTful API Gateway)

Uvicorn (ASGI Server)

Custom Graph Data Structure

# Project Structure

mumbai-metro-navigator/
├── backend/
│   ├── main.py        # FastAPI server and endpoints
│   ├── graph.py       # BFS and Dijkstra routing logic
│   └── data.py        # Mumbai Metro adjacency list data
├── frontend/
│   ├── index.html     # Main user interface
│   ├── style.css      # UI styling
│   └── app.js         # API integration and map logic
├── run.py             # Launcher script for the backend
└── requirements.txt   # Python dependencies


# Local Setup & Installation

1. Clone the repository

git clone https://github.com/YOUR-USERNAME/mumbai-metro-navigator.git
cd mumbai-metro-navigator


2. Set up the Python Backend

Create and activate a virtual environment, then install the required dependencies:

Windows:

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic


macOS/Linux:

python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pydantic


3. Run the Backend Server

Use the provided launcher script to start the server from the root directory:

python run.py


(The API will be available at http://127.0.0.1:8000)

4. Run the Frontend

Simply open the frontend/index.html file in any modern web browser to start using the application.

🔗 API Endpoints

GET /api/stations - Returns a list of all available metro stations grouped by line.

POST /api/route - Accepts a start and destination station and returns the optimal path array.
