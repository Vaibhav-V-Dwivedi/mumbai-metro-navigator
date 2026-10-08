import json
from data import build_mumbai_metro_graph

def run_tests():
    graph = build_mumbai_metro_graph()
    
    print("========================================")
    print("Testing Mumbai Metro Routing Engine")
    print("========================================\n")
    
    # Test 1: L1 Versova to L1 Ghatkopar (Same line)
    print("--- Test 1: Versova to Ghatkopar (Same Line) ---")
    path, time_sec = graph.dijkstra_shortest_path("L1_VERSOVA", "L1_GHATKOPAR")
    metadata = graph.calculate_metadata(path)
    exec_plan = graph.build_path_execution(path)
    
    print(f"Path nodes: {' -> '.join(path)}")
    print(f"Metadata: {metadata}")
    print("Execution Plan:")
    print(json.dumps(exec_plan, indent=2))
    print("\n")
    
    # Test 2: L1 Versova to L7 Gundavali (Interchange at Andheri)
    print("--- Test 2: Versova to Gundavali (Interchange L1 -> L7 at Andheri) ---")
    path, time_sec = graph.dijkstra_shortest_path("L1_VERSOVA", "L7_GUNDAVALI")
    metadata = graph.calculate_metadata(path)
    exec_plan = graph.build_path_execution(path)
    
    print(f"Path nodes: {' -> '.join(path)}")
    print(f"Metadata: {metadata}")
    print("Execution Plan:")
    print(json.dumps(exec_plan, indent=2))
    print("\n")
    
    # Test 3: L2A Andheri West to L7 Borivali East (Complex routing)
    print("--- Test 3: Andheri West (L2A) to Borivali East (L7) ---")
    # Using Min Distance / Time (Dijkstra)
    path, time_sec = graph.dijkstra_shortest_path("L2A_ANDHERIW", "L7_BORIVALI")
    metadata = graph.calculate_metadata(path)
    exec_plan = graph.build_path_execution(path)
    
    print("Dijkstra (Shortest Time) Route:")
    print(f"Path nodes: {' -> '.join(path)}")
    print(f"Metadata: {metadata}")
    print("Execution Plan:")
    print(json.dumps(exec_plan, indent=2))
    print("\n")
    
    # Test 4: BFS vs Dijkstra (Min Stops vs Min Time) for L1_VERSOVA to L7_BORIVALI
    print("--- Test 4: Min Stops (BFS) vs Min Time (Dijkstra) from Versova to Borivali L7 ---")
    
    bfs_path = graph.bfs_shortest_path("L1_VERSOVA", "L7_BORIVALI")
    bfs_metadata = graph.calculate_metadata(bfs_path)
    
    dijkstra_path, _ = graph.dijkstra_shortest_path("L1_VERSOVA", "L7_BORIVALI")
    dijkstra_metadata = graph.calculate_metadata(dijkstra_path)
    
    print(f"BFS (Min Stops) Path Length: {len(bfs_path)} nodes. Metadata: {bfs_metadata}")
    print(f"BFS Path: {' -> '.join(bfs_path)}")
    
    print(f"Dijkstra (Min Time) Path Length: {len(dijkstra_path)} nodes. Metadata: {dijkstra_metadata}")
    print(f"Dijkstra Path: {' -> '.join(dijkstra_path)}")
    print("\n")

if __name__ == "__main__":
    run_tests()

