import heapq
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any

@dataclass
class Node:
    node_id: str
    station_name: str
    line_color: str
    line_name: str
    is_interchange_hub: bool = False
    geo_location: Dict[str, float] = field(default_factory=dict)

@dataclass
class Edge:
    target_node_id: str
    edge_type: str  # "TRACK" or "INTERCHANGE"
    distance_km: float
    weight_time_sec: float

class Graph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, List[Edge]] = {}

    def add_node(self, node: Node):
        self.nodes[node.node_id] = node
        if node.node_id not in self.edges:
            self.edges[node.node_id] = []

    def add_edge(self, source_id: str, target_id: str, edge_type: str, distance_km: float, weight_time_sec: float):
        if source_id in self.nodes and target_id in self.nodes:
            self.edges[source_id].append(Edge(target_id, edge_type, distance_km, weight_time_sec))
            self.edges[target_id].append(Edge(source_id, edge_type, distance_km, weight_time_sec))

    def bfs_shortest_path(self, start_id: str, end_id: str) -> Optional[List[str]]:
        """Min stops (unweighted edges, BFS algorithm)."""
        if start_id not in self.nodes or end_id not in self.nodes:
            return None
        
        queue = deque([(start_id, [start_id])])
        visited = {start_id}

        while queue:
            current, path = queue.popleft()
            
            if current == end_id:
                return path
            
            for edge in self.edges.get(current, []):
                if edge.target_node_id not in visited:
                    visited.add(edge.target_node_id)
                    queue.append((edge.target_node_id, path + [edge.target_node_id]))
                    
        return None

    def dijkstra_shortest_path(self, start_id: str, end_id: str, weight_key: str = 'weight_time_sec') -> Optional[Tuple[List[str], float]]:
        """Min distance or time (Dijkstra's algorithm)."""
        if start_id not in self.nodes or end_id not in self.nodes:
            return None
            
        distances = {node: float('infinity') for node in self.nodes}
        distances[start_id] = 0
        previous_nodes = {node: None for node in self.nodes}
        
        # Priority queue: (weight, node_id)
        pq = [(0, start_id)]
        
        while pq:
            current_weight, current_node = heapq.heappop(pq)
            
            if current_weight > distances[current_node]:
                continue
                
            if current_node == end_id:
                break
                
            for edge in self.edges.get(current_node, []):
                weight = getattr(edge, weight_key)
                distance = current_weight + weight
                
                if distance < distances[edge.target_node_id]:
                    distances[edge.target_node_id] = distance
                    previous_nodes[edge.target_node_id] = current_node
                    heapq.heappush(pq, (distance, edge.target_node_id))
                    
        if distances[end_id] == float('infinity'):
            return None
            
        path = []
        curr = end_id
        while curr is not None:
            path.append(curr)
            curr = previous_nodes[curr]
            
        return path[::-1], distances[end_id]

    def calculate_metadata(self, path: List[str]) -> Dict[str, Any]:
        """Calculates distance, stops, and time for a given path."""
        if not path or len(path) == 1:
            return {"total_distance_km": 0.0, "total_stops_count": 0, "estimated_transit_time_min": 0.0}
            
        dist = 0.0
        time_sec = 0.0
        stops = len(path) - 1
        
        for i in range(1, len(path)):
            u = path[i-1]
            v = path[i]
            for e in self.edges[u]:
                if e.target_node_id == v:
                    dist += e.distance_km
                    time_sec += e.weight_time_sec
                    break
                    
        return {
            "total_distance_km": round(dist, 2),
            "total_stops_count": stops,
            "estimated_transit_time_min": round(time_sec / 60.0, 1)
        }

    def build_path_execution(self, path: List[str]) -> List[Dict[str, Any]]:
        """Transforms a path array of IDs into a detailed step-by-step instruction sequence."""
        if not path:
            return []
            
        execution = []
        start_node = self.nodes[path[0]]
        
        execution.append({
            "step": 1,
            "action": "DEPART",
            "station": start_node.station_name,
            "line": start_node.line_name,
            "color_hex": start_node.line_color,
            "coordinates": start_node.geo_location
        })
        
        step_counter = 2
        
        for i in range(1, len(path)):
            prev_id = path[i-1]
            curr_id = path[i]
            
            prev_node = self.nodes[prev_id]
            curr_node = self.nodes[curr_id]
            
            edge_type = "TRACK"
            for e in self.edges[prev_id]:
                if e.target_node_id == curr_id:
                    edge_type = e.edge_type
                    break
                    
            if edge_type == "INTERCHANGE":
                execution.append({
                    "step": step_counter,
                    "action": "INTERCHANGE",
                    "station": prev_node.station_name,
                    "instruction": f"Disembark {prev_node.line_name}. Walk to board {curr_node.line_name}.",
                    "from_color": prev_node.line_color,
                    "to_color": curr_node.line_color,
                    "coordinates": prev_node.geo_location
                })
                step_counter += 1
                
                # If this is the last node in the path, we need to explicitly ARRIVE
                if i == len(path) - 1:
                    execution.append({
                        "step": step_counter,
                        "action": "ARRIVE",
                        "station": curr_node.station_name,
                        "line": curr_node.line_name,
                        "color_hex": curr_node.line_color,
                        "coordinates": curr_node.geo_location
                    })
                    step_counter += 1
            else:
                action = "ARRIVE" if i == len(path) - 1 else "TRANSIT"
                execution.append({
                    "step": step_counter,
                    "action": action,
                    "station": curr_node.station_name,
                    "line": curr_node.line_name,
                    "color_hex": curr_node.line_color,
                    "coordinates": curr_node.geo_location
                })
                step_counter += 1
                
        return execution
