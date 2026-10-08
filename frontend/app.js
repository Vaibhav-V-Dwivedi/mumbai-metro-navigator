const API_BASE = "http://127.0.0.1:8000/api";

// Initialize Map
const map = L.map('map').setView([19.0760, 72.8777], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

document.addEventListener('DOMContentLoaded', () => {
    fetchStations();
    
    document.getElementById('find-route-btn').addEventListener('click', findRoute);
});

async function fetchStations() {
    try {
        const res = await fetch(`${API_BASE}/stations`);
        if (!res.ok) throw new Error("Failed to fetch stations");
        
        const payload = await res.json();
        const categories = payload.data;
        
        const startSelect = document.getElementById('start-station');
        const endSelect = document.getElementById('end-station');
        
        categories.forEach(category => {
            const optgroup1 = document.createElement('optgroup');
            optgroup1.label = category.line_name;
            optgroup1.style.color = category.color_hex;
            
            const optgroup2 = document.createElement('optgroup');
            optgroup2.label = category.line_name;
            optgroup2.style.color = category.color_hex;
            
            category.stations.forEach(station => {
                const text = station.is_interchange_hub ? `${station.station_name} (Interchange)` : station.station_name;
                
                const option1 = document.createElement('option');
                option1.value = station.node_id;
                option1.textContent = text;
                optgroup1.appendChild(option1);
                
                const option2 = document.createElement('option');
                option2.value = station.node_id;
                option2.textContent = text;
                optgroup2.appendChild(option2);
            });
            
            startSelect.appendChild(optgroup1);
            endSelect.appendChild(optgroup2);
        });
    } catch (err) {
        console.error("Error loading stations:", err);
    }
}

async function findRoute() {
    const sourceId = document.getElementById('start-station').value;
    const destId = document.getElementById('end-station').value;
    const pref = document.getElementById('preference').value;
    
    if (!sourceId || !destId) {
        alert("Please select both a start and destination station.");
        return;
    }
    if (sourceId === destId) {
        alert("Start and destination must be different.");
        return;
    }
    
    try {
        const res = await fetch(`${API_BASE}/route`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                source_id: sourceId,
                destination_id: destId,
                preference: pref
            })
        });
        
        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.detail || "Routing failed");
        }
        
        const data = await res.json();
        renderResults(data);
    } catch (err) {
        console.error(err);
        alert(err.message);
    }
}

let routeLayerGroup = L.layerGroup().addTo(map);

function renderResults(data) {
    document.getElementById('results-panel').style.display = 'block';
    
    // Update metadata statistics
    document.getElementById('meta-time').textContent = data.metadata.estimated_transit_time_min;
    document.getElementById('meta-stops').textContent = data.metadata.total_stops_count;
    document.getElementById('meta-dist').textContent = data.metadata.total_distance_km;
    
    // Render Itinerary Timeline
    const container = document.getElementById('itinerary-container');
    container.innerHTML = ''; // Clear previous route
    routeLayerGroup.clearLayers(); // Clear previous map layers
    
    let currentPolyline = [];
    let currentColor = data.path_execution.length > 0 ? data.path_execution[0].color_hex : "#333";
    
    data.path_execution.forEach(step => {
        const stepDiv = document.createElement('div');
        stepDiv.className = 'timeline-step';
        
        let titleColor = "#333";
        if (step.color_hex) {
            titleColor = step.color_hex;
        } else if (step.action === "INTERCHANGE") {
            titleColor = "#d35400"; // Orange highlight for interchange step
        }
        
        let content = `<h4 style="color: ${titleColor};">${step.action}: ${step.station}</h4>`;
        
        if (step.action === "DEPART") {
            content += `<p>Board ${step.line}</p>`;
        } else if (step.action === "TRANSIT" || step.action === "ARRIVE") {
            content += `<p>${step.line}</p>`;
        }
        
        if (step.action === "INTERCHANGE") {
            content += `<div class="interchange-alert">
                <strong>Change Lines:</strong><br/>
                ${step.instruction}
            </div>`;
        }
        
        stepDiv.innerHTML = content;
        container.appendChild(stepDiv);
        
        // Map plotting logic
        if (step.coordinates && step.coordinates.lat && step.coordinates.lng) {
            const latlng = [step.coordinates.lat, step.coordinates.lng];
            
            if (step.action === "INTERCHANGE") {
                // Plot interchange marker
                L.circleMarker(latlng, { radius: 8, color: '#d35400', fillColor: 'white', fillOpacity: 1, weight: 3 })
                    .addTo(routeLayerGroup)
                    .bindPopup(`<b>${step.station}</b><br>Interchange: ${step.instruction}`);
                    
                // Draw existing path before interchange
                if (currentPolyline.length > 0) {
                    L.polyline(currentPolyline, { color: currentColor, weight: 6, opacity: 0.8 }).addTo(routeLayerGroup);
                }
                
                // Start new path for new line
                currentPolyline = [latlng];
                currentColor = step.to_color;
            } else {
                currentPolyline.push(latlng);
                
                if (step.action === "DEPART") {
                    L.marker(latlng).addTo(routeLayerGroup).bindPopup(`<b>Start:</b> ${step.station}`);
                } else if (step.action === "ARRIVE") {
                    L.marker(latlng).addTo(routeLayerGroup).bindPopup(`<b>Destination:</b> ${step.station}`);
                } else {
                    L.circleMarker(latlng, { radius: 5, color: currentColor, fillColor: 'white', fillOpacity: 1, weight: 2 })
                        .addTo(routeLayerGroup)
                        .bindPopup(`<b>${step.station}</b><br>${step.line}`);
                }
            }
        }
    });
    
    // Draw the final polyline segment
    if (currentPolyline.length > 1) {
        L.polyline(currentPolyline, { color: currentColor, weight: 6, opacity: 0.8 }).addTo(routeLayerGroup);
    }
    
    // Auto-fit bounds
    if (routeLayerGroup.getLayers().length > 0) {
        const bounds = L.latLngBounds([]);
        routeLayerGroup.eachLayer(layer => {
            if (layer.getLatLng) {
                bounds.extend(layer.getLatLng());
            }
        });
        map.fitBounds(bounds, { padding: [40, 40] });
    }
}

