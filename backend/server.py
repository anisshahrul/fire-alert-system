from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import random
import time
import asyncio

# Create a FastAPI application instance
app = FastAPI()

# Configure CORS (Cross-Origin Resource Sharing)
# This is crucial to allow our frontend running on a different port to access this backend.
# The wildcard "*" allows all origins for a robust local development environment.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for active fire alerts
# We'll use a dictionary where the key is the location name.
active_fire_alerts = {}

# A list of predefined locations for our simulation.
locations = [
    "Warehouse A", "Office Block B", "Data Center C",
    "Production Line D", "Storage Unit E", "Main Lobby F",
    "Loading Dock G", "Server Room H", "R&D Lab I", "Cafeteria J",
    "Security Hub K", "Ventilation Room L", "Emergency Exit M",
    "Parking Level N", "IT Server Room O"
]

# This asynchronous function simulates fire sensor events.
async def simulate_fire_events():
    """Generates random fire events and updates the in-memory store."""
    print("Fire event simulation started...")
    while True:
        # Generate a random fire event every 3 seconds
        location = random.choice(locations)
        event_id = f"fire-{int(time.time() * 1000)}"  # Unique ID
        intensity = random.randint(1, 10)
        status = "active" if random.random() < 0.7 else "cleared"  # 70% chance of 'active'
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        event = {
            "id": event_id,
            "location": location,
            "intensity": intensity,
            "status": status,
            "timestamp": timestamp
        }

        print(f"Simulated Event: {event}")

        if status == "active":
            active_fire_alerts[location] = event
        else:
            if location in active_fire_alerts:
                del active_fire_alerts[location]

        await asyncio.sleep(5) # Wait for 5 seconds before the next event

# Define the API endpoint that our frontend will call.
# This function will be triggered when a GET request is made to '/api/fire-alerts'.
@app.get("/api/fire-alerts")
async def get_fire_alerts():
    """Returns a list of all currently active fire alerts."""
    # We convert the dictionary values to a list of alerts.
    return list(active_fire_alerts.values())

# This startup event handler runs when the server first starts.
@app.on_event("startup")
async def startup_event():
    """Start the background task for simulating fire events."""
    # We run the simulation task in the background without blocking the server.
    asyncio.create_task(simulate_fire_events())

# Main entry point to run the application with uvicorn.
if __name__ == "__main__":
    # We tell uvicorn to run our 'app' on a host that is accessible
    # from the browser (0.0.0.0) at port 3001.
    uvicorn.run(app, host="0.0.0.0", port=3001)
