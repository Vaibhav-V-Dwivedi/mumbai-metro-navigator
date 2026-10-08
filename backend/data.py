from graph import Graph, Node

def build_mumbai_metro_graph() -> Graph:
    g = Graph()
    
    # ----------------
    # 1. Add Nodes
    # ----------------
    # Blue Line 1
    l1_nodes = [
        Node("L1_VERSOVA", "Versova", "#0000FF", "Blue Line 1", False, {"lat": 19.1278, "lng": 72.8170}),
        Node("L1_DNNAGAR", "DN Nagar", "#0000FF", "Blue Line 1", True, {"lat": 19.1238, "lng": 72.8268}),
        Node("L1_AZADNAGAR", "Azad Nagar", "#0000FF", "Blue Line 1", False, {"lat": 19.1215, "lng": 72.8360}),
        Node("L1_ANDHERI", "Andheri", "#0000FF", "Blue Line 1", True, {"lat": 19.1197, "lng": 72.8468}),
        Node("L1_WEH", "WEH", "#0000FF", "Blue Line 1", False, {"lat": 19.1147, "lng": 72.8548}),
        Node("L1_GHATKOPAR", "Ghatkopar", "#0000FF", "Blue Line 1", False, {"lat": 19.0838, "lng": 72.9112})
    ]
    for n in l1_nodes: g.add_node(n)
        
    # Yellow Line 2A
    l2a_nodes = [
        Node("L2A_DAHISAR", "Dahisar East", "#D8C007", "Yellow Line 2A", True, {"lat": 19.2486, "lng": 72.8596}),
        Node("L2A_BORIVALI", "Borivali West", "#D8C007", "Yellow Line 2A", False, {"lat": 19.2274, "lng": 72.8496}),
        Node("L2A_MALAD", "Malad West", "#D8C007", "Yellow Line 2A", False, {"lat": 19.1865, "lng": 72.8427}),
        Node("L2A_GOREGAON", "Goregaon West", "#D8C007", "Yellow Line 2A", False, {"lat": 19.1620, "lng": 72.8402}),
        Node("L2A_ANDHERIW", "Andheri West", "#D8C007", "Yellow Line 2A", True, {"lat": 19.1235, "lng": 72.8300})
    ]
    for n in l2a_nodes: g.add_node(n)
        
    # Red Line 7
    l7_nodes = [
        Node("L7_DAHISAR", "Dahisar East", "#FF0000", "Red Line 7", True, {"lat": 19.2486, "lng": 72.8596}),
        Node("L7_BORIVALI", "Borivali East", "#FF0000", "Red Line 7", False, {"lat": 19.2268, "lng": 72.8594}),
        Node("L7_GOREGAON", "Goregaon East", "#FF0000", "Red Line 7", False, {"lat": 19.1645, "lng": 72.8587}),
        Node("L7_JOGESHWARI", "Jogeshwari East", "#FF0000", "Red Line 7", False, {"lat": 19.1432, "lng": 72.8569}),
        Node("L7_GUNDAVALI", "Gundavali", "#FF0000", "Red Line 7", True, {"lat": 19.1195, "lng": 72.8520})
    ]
    for n in l7_nodes: g.add_node(n)

    # ----------------
    # 2. Add Edges (Tracks)
    # ----------------
    # Assume 1 km takes roughly 100-120 seconds (30-36 km/h)
    
    # Line 1 TRACKS
    g.add_edge("L1_VERSOVA", "L1_DNNAGAR", "TRACK", 1.2, 120)
    g.add_edge("L1_DNNAGAR", "L1_AZADNAGAR", "TRACK", 1.0, 100)
    g.add_edge("L1_AZADNAGAR", "L1_ANDHERI", "TRACK", 1.5, 150)
    g.add_edge("L1_ANDHERI", "L1_WEH", "TRACK", 1.0, 100)
    g.add_edge("L1_WEH", "L1_GHATKOPAR", "TRACK", 6.0, 600)
    
    # Line 2A TRACKS
    g.add_edge("L2A_DAHISAR", "L2A_BORIVALI", "TRACK", 2.5, 250)
    g.add_edge("L2A_BORIVALI", "L2A_MALAD", "TRACK", 3.0, 300)
    g.add_edge("L2A_MALAD", "L2A_GOREGAON", "TRACK", 2.0, 200)
    g.add_edge("L2A_GOREGAON", "L2A_ANDHERIW", "TRACK", 4.0, 400)
    
    # Line 7 TRACKS
    g.add_edge("L7_DAHISAR", "L7_BORIVALI", "TRACK", 2.5, 250)
    g.add_edge("L7_BORIVALI", "L7_GOREGAON", "TRACK", 5.0, 500)
    g.add_edge("L7_GOREGAON", "L7_JOGESHWARI", "TRACK", 2.5, 250)
    g.add_edge("L7_JOGESHWARI", "L7_GUNDAVALI", "TRACK", 1.5, 150)
    
    # ----------------
    # 3. Add Edges (Interchanges)
    # ----------------
    # High artificial time penalty (e.g., 500 seconds walk/wait time) to discourage switching
    
    # Andheri (Blue L1) <-> Gundavali (Red L7)
    g.add_edge("L1_ANDHERI", "L7_GUNDAVALI", "INTERCHANGE", 0.2, 500)
    
    # DN Nagar (Blue L1) <-> Andheri West (Yellow L2A)
    g.add_edge("L1_DNNAGAR", "L2A_ANDHERIW", "INTERCHANGE", 0.3, 500)
    
    # Dahisar East (Yellow L2A) <-> Dahisar East (Red L7)
    g.add_edge("L2A_DAHISAR", "L7_DAHISAR", "INTERCHANGE", 0.1, 300)

    return g

