# Fire Alert System
## Project Description

This is a real-time fire alert system designed to monitor environmental data from sensors and detect potential fire hazards. The system uses a Python backend to process sensor readings and a web-based dashboard to display the status and alert history.

The system's core function is to provide an early warning by monitoring temperature and smoke levels, triggering an alert when predefined thresholds are exceeded.

 --- 
 
## 📁 Features

**Real-time Monitoring**: Continuously simulates and displays sensor data for temperature and smoke.

**Visual Alerts**: A dashboard element visually indicates an alert state.

**Alert History**: Maintains a log of all triggered alerts with timestamps.

**Responsive Design**: The web dashboard is designed to be accessible and readable on various devices.

---

## 🚀 Getting Started
Follow these steps to get a copy of the project running on your local machine for development and testing purposes.

### 📁 1. Clone the Repository
```bash
git clone https://github.com/anisshahrul/fire-alert-system.git
cd fire-alert-system
```

### 🐍 2. Set Up Virtual Environment

1. **Create the virtual environment**  
```venv
python -m venv venv 
OR
py -m venv venv
```

2. **Activate the virtual environment**

 *For Windows (Command Prompt):*  
```activate
venv\Scripts\activate
```

> ⚠️ **Important:** Add `.venv` to your `.gitignore` to avoid committing unnecessary files and folders related to your local Python environment.

### 📦 3. Install Dependencies

```pip
pip install -r requirements.txt
```

### 🚦 4. Run the FastAPI Server

1. Open your terminal and make sure you're in the root project directory:
`/fire-alert-system/backend`
2. Run the development server with: 
```uvicorn
uvicorn server:app --reload --port 3001
``` 
3. Once the server is running, you can access it at:
- API Root: http://127.0.0.1:3001
- Swagger UI (API docs) http://127.0.0.1:3001/docs
4. ⚠️ If you encounter an "address already in use" error, it means port 3001 is occupied.

### 🎈 5. Monitor the fire dashboard
1. In a **new terminal window**, make sure you're in the root project directory:
`/fire-alert-system/frontend`
2. Run the frontend with:
```npm
npm run dev
```
3. Once the server is running, you can access it at:
   - http://localhost:3000
---

✅ This provides a simple interface dashboard to monitor fire in buildings in real-time.

---

## Retrospective: Scaling for Real-World Usage

The initial system is a great proof-of-concept, but a production-grade fire-alert system for real-world usage would require a complete architectural redesign to handle scale, reliability, and security. Here's a look at the key challenges and a proposed solution.

## Key Challenges

**Massive Data Volume**: The system must handle simultaneous data streams from thousands or millions of sensors without bottlenecks.

**Strict Real-Time Processing**: Alerts need to be generated with extremely low latency to be effective.

**High Availability**: The system must be fault-tolerant, with no single point of failure.

**Guaranteed Alert Delivery**: Critical alerts must be delivered reliably through multiple channels with built-in retry logic.

**Data Security**: Robust measures are needed to protect sensitive sensor data and user information.

## Proposed Scalable Architecture

To overcome these challenges, a distributed, microservices-based architecture is essential.

**Message Queue**: Sensors would send data to a high-throughput message queue, which decouples them from the processing services.

**Stream Processing**: A stream processing framework would analyze the data in real-time for immediate threat detection.

**Dedicated Services**: The system would be broken down into specialized microservices for tasks like Data Ingestion, Real-Time Analytics, and Alerting.

**Scalable Storage**: Data would be stored in a time-series database optimized for sensor data.

This distributed approach ensures the system is highly scalable, resilient, and reliable enough for mission-critical use.
