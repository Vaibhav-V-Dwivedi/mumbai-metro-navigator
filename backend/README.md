# Mumbai Metro Navigation API

This is the backend API for the Mumbai Metro Route Navigation System. It uses FastAPI to expose routing logic based on Graph Theory (BFS/Dijkstra).

## How to Run

1. Make sure your virtual environment `.venv` is activated.
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Endpoints

* **GET `/api/stations`**: Returns a list of all stations grouped by Metro Line.
* **POST `/api/route`**: Calculates a route.
  * Body: `{"source_id": "L1_VERSOVA", "destination_id": "L7_GUNDAVALI", "preference": "MIN_TIME"}`
  * `preference` can be `"MIN_TIME"` (default) or `"MIN_STOPS"`.

## Interactive API Docs
Once the server is running, you can test the API interactively by visiting:
http://localhost:8000/docs

