<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import './styles/style.scss';

// Reactive state variables. The ref() function makes these variables "reactive,"
// meaning Vue will automatically update the page whenever their values change.
const fireAlerts = ref([]); // An array to store all active fire alerts from the backend.
const selectedAlert = ref(null); // Stores the details of the alert the user clicks on.
const showSimulatedAlert = ref(false); // Controls the visibility of the simulated alert modal.
const simulatedAlertMessage = ref(''); // Stores the message text for the simulated alert.
let intervalId = null; // A variable to hold the ID of our polling timer.

// A static list of locations for our simulated system.
const locations = [
    "Warehouse A", "Office Block B", "Data Center C",
    "Production Line D", "Storage Unit E", "Main Lobby F",
    "Loading Dock G", "Server Room H", "R&D Lab I", "Cafeteria J",
    "Security Hub K", "Ventilation Room L", "Emergency Exit M",
    "Parking Level N", "IT Server Room O"
];

// This asynchronous function fetches the latest fire alert data from our backend API.
const fetchAlerts = async () => {
    try {
        // Attempt to connect to the backend server running on localhost:3001
        const response = await fetch('http://localhost:3001/api/fire-alerts');

        // Check if the server's response was successful (status code 200-299).
        if (!response.ok) {
            // If not, throw an error to be caught by the catch block.
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON data from the response body.
        const data = await response.json();

        // Update the reactive fireAlerts variable with the new data.
        fireAlerts.value = data;
    } catch (error) {
        // Log any errors that occur during the fetch operation.
        console.error("Failed to fetch fire alerts:", error);
    }
};

// This function determines which CSS classes to apply to a location's grid box,
// now based on both the presence of an alert and its intensity level.
const getGridClass = (location) => {
    // Find the alert object for the current location.
    const alert = fireAlerts.value.find(a => a.location === location);

    // If there is an active alert, return the appropriate intensity class.
    if (alert) {
        const intensity = alert.intensity;
        const status = alert.status;
        
        if (status === 'cleared') {
            return { 'fire-zone': true, 'cleared': true };
        } else if (intensity >= 8) {
            return { 'fire-zone': true, 'active': true, 'high-intensity': true };
        } else if (intensity >= 5) {
            return { 'fire-zone': true, 'active': true, 'medium-intensity': true };
        } else {
            return { 'fire-zone': true, 'active': true, 'low-intensity': true };
        }
    }

    // If there is no active alert, return the default class.
    return { 'fire-zone': true };
};

// This function handles the click event on a grid box.
// It finds the details for the clicked location's alert and stores them.
const handleZoneClick = (location) => {
    // Find the specific alert object that matches the clicked location.
    const alert = fireAlerts.value.find(alert => alert.location === location);

    if (alert) {
        // Update the reactive selectedAlert variable. This will make the details section visible.
        selectedAlert.value = alert;
    } else {
        // If no alert, show a cleared status
        selectedAlert.value = {
            location,
            intensity: 0,
            status: "cleared",
            timestamp: Date.now()
        };
        // Optionally, show a modal or message
        simulatedAlertMessage.value = `Status for ${location} has been cleared.\nNo active fire alert.`;
        showSimulatedAlert.value = true;
    }
};

// This new function simulates sending an SMS or email alert.
const sendSimulatedAlert = () => {
    if (selectedAlert.value) {
        // Construct the alert message using details from the selected alert.
        const isCleared = selectedAlert.value.status === 'cleared';
        const alertTitle = isCleared ? '*** ALERT UPDATE ***' : '*** URGENT ALERT ***';
        const alertMessage = isCleared 
            ? `Fire at ${selectedAlert.value.location} has been cleared`
            : `Fire reported at: ${selectedAlert.value.location}`;
            
        simulatedAlertMessage.value = `${alertTitle}\n${alertMessage}\nIntensity: ${selectedAlert.value.intensity}/10\nStatus: ${selectedAlert.value.status}\nTime: ${new Date(selectedAlert.value.timestamp).toLocaleString()}`;
        // Show the simulated alert modal.
        showSimulatedAlert.value = true;
    }
};

// The onMounted hook runs once, immediately after the component is added to the page.
onMounted(() => {
    fetchAlerts(); // Perform an initial data fetch right away.
    // Set up a timer to call fetchAlerts() every 5 seconds (5000 milliseconds),
    // which simulates real-time data updates.
    intervalId = setInterval(fetchAlerts, 5000);
});

// The onUnmounted hook runs just before the component is removed from the page.
// This is important for cleaning up resources to prevent memory leaks.
onUnmounted(() => {
    clearInterval(intervalId); // Stop the polling timer.
});
</script>

<template>
    <!-- The HTML structure for our dashboard. -->
    <div class="app-container">
        <h1>Fire Monitoring Dashboard</h1>

        <!-- The grid layout for our locations. -->
        <div class="fire-grid">
            <!-- The v-for directive loops through the 'locations' array to create a box for each location. -->
            <div
                v-for="(location, index) in locations"
                :key="index"
                :class="getGridClass(location)"
                @click="handleZoneClick(location)"
            >
                <h3>{{ location }}</h3>
                <!-- The v-if directive conditionally renders the appropriate alert message
                     based on the alert status for this location. -->
                <template v-if="fireAlerts.some(alert => alert.location === location)">
                    <p v-if="fireAlerts.find(alert => alert.location === location).status === 'active'" class="alert-text">
                        FIRE ALERT!
                    </p>
                    <p v-else class="cleared-text">
                        CLEARED
                    </p>
                </template>
            </div>
        </div>

        <!-- The details panel for a selected alert.
             The v-if directive ensures this section is only displayed when an alert is selected. -->
        <div v-if="selectedAlert" :class="['alert-details', selectedAlert.status === 'cleared' ? 'cleared-details' : '']">
            <h2>Alert Details: {{ selectedAlert.location }}</h2>
            <p><strong>Intensity:</strong> {{ selectedAlert.intensity }} / 10</p>
            <p><strong>Status:</strong> <span :class="selectedAlert.status === 'cleared' ? 'status-cleared' : 'status-active'">{{ selectedAlert.status }}</span></p>
            <p><strong>Timestamp:</strong> {{ new Date(selectedAlert.timestamp).toLocaleString() }}</p>
            <div class="button-group">
                <button @click="sendSimulatedAlert">Send Alert</button>
                <button @click="selectedAlert = null">Close</button>
            </div>
        </div>

        <!-- The new simulated alert modal.
             The v-if directive makes this visible only when showSimulatedAlert is true. -->
        <div v-if="showSimulatedAlert" class="modal-overlay">
            <div :class="['modal-content', selectedAlert && selectedAlert.status === 'cleared' ? 'modal-cleared' : '']">
                <h3>Simulated Alert Sent!</h3>
                <pre :class="['alert-message', selectedAlert && selectedAlert.status === 'cleared' ? 'alert-message-cleared' : '']">{{ simulatedAlertMessage }}</pre>
                <button @click="showSimulatedAlert = false" :class="selectedAlert && selectedAlert.status === 'cleared' ? 'button-cleared' : ''">OK</button>
            </div>
        </div>
    </div>
</template>

