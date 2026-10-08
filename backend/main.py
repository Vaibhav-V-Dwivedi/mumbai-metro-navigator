from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from data import build_mumbai_metro_graph 
from graph import Graph
app = FastAPI(title="Mumbai Metro Routing API", description="API for Mumbai Metro Route Navigation System")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize graph as a singleton for the app
graph = build_mumbai_metro_graph()

class RouteRequest(BaseModel):
    source_id: str
    destination_id: str
    preference: Optional[str] = "MIN_TIME"  # Accepts "MIN_TIME" or "MIN_STOPS"

@app.get("/api/stations")
def get_stations():
    """
    Returns a structured list of all available stations, categorized by their Metro Line.
    Useful for populating frontend dropdowns grouped by line.
    """
    categories = {}
    
    for node_id, node in graph.nodes.items():
        line = node.line_name
        if line not in categories:
            categories[line] = {
                "line_name": line,
                "color_hex": node.line_color,
                "stations": []
            }
        
        categories[line]["stations"].append({
            "node_id": node.node_id,
            "station_name": node.station_name,
            "is_interchange_hub": node.is_interchange_hub
        })
        
    # Return as an array of categories
    return {"data": list(categories.values())}

@app.post("/api/route")
def calculate_route(request: RouteRequest):
    """
    Accepts a starting station and destination station, and returns the calculated route.
    """
    if request.source_id not in graph.nodes:
        raise HTTPException(status_code=404, detail=f"Source station '{request.source_id}' not found.")
    if request.destination_id not in graph.nodes:
        raise HTTPException(status_code=404, detail=f"Destination station '{request.destination_id}' not found.")
        
    # Determine the algorithm based on user preference
    if request.preference == "MIN_STOPS":
        path = graph.bfs_shortest_path(request.source_id, request.destination_id)
    else:
        # Default to MIN_TIME / Distance (Dijkstra)
        res = graph.dijkstra_shortest_path(request.source_id, request.destination_id)
        path = res[0] if res else None
        
    if not path:
        raise HTTPException(status_code=400, detail="No valid route found between these stations.")
        
    metadata = graph.calculate_metadata(path)
    execution_plan = graph.build_path_execution(path)
    
    return {
        "metadata": metadata,
        "path_execution": execution_plan
    }

