# Emergency Alert System

**Emergency Alert System** is a Streamlit-based interactive tool designed to simulate real-time emergency detection and alerting.  
It leverages **NLP**, **speech recognition**, and **simulated GPS** to identify potential emergency messages, prioritize alerts, and provide visual dashboards.

---

## Features

- **Text & Voice Input:** Users can type messages or speak using a microphone.
- **Emergency Detection:** Detects emergency keywords such as fire, accident, flood, or earthquake.
- **Priority Levels:** Automatically assigns High, Medium, or Low priority based on message content.
- **Alert Notifications:** Simulates notifying relevant emergency departments.
- **Location Simulation:** Generates a fake GPS location for the alert.
- **Real-Time Dashboard:**
  - Maps the latest alert location.
  - Displays alert frequency by department over time.
  - Provides alert history summaries.
- **Emergency Logs Management:** 
  - Filter by message, department, or priority.
  - Download filtered logs as CSV.
  - Clear all logs.
- **Login/Signup System:** Mock authentication to simulate user management.
- **Responsive Charts:** Uses Altair for real-time line charts of alerts.
- **Session Metrics:** Tracks total alerts triggered per session.

---

## Technology Stack

- **Frontend & Framework:** Streamlit  
- **Speech Recognition:** `speech_recognition` + Google Speech API  
- **Data Handling:** Pandas, Numpy  
- **Visualization:** Altair  
- **Date & Time Management:** datetime  
- **Storage:** CSV-based emergency log (`emergency_log.csv`)  
- **Unique ID Generation:** uuid  
- **Randomized Simulation:** random

---


## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/emergency-alert-system.git
cd emergency-alert-system
Create a virtual environment (recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Running the App
Start the Streamlit server:

bash
Copy code
streamlit run app.py
Open your browser and navigate to:

arduino
Copy code
http://localhost:8501




How to Use
Login or Sign Up

Use mock credentials or sign up with a mock Aadhaar number.

Input a Message

Type a message or use voice input to send alerts.

Emergency Detection & Alerts

The system detects keywords and assigns priority levels.

Sends alerts to selected or matched emergency departments.

Shows simulated GPS location on a map.

View Dashboards & Logs

Track alerts triggered during the session.

View historical logs, filter by message/department/priority.

Download logs or clear them.

Analyze alert frequency by department over time with interactive charts.

Project Structure
perl
Copy code
emergency-alert-system/
│── app.py                  # Main Streamlit app
│── requirements.txt        # Python dependencies
│── README.md               # Project documentation
│── emergency_log.csv       # Generated emergency logs
Roadmap
Add real-time location fetching using mobile GPS (instead of simulated coordinates).

Integrate actual SMS/email alert notifications.

Add AI-based sentiment/emergency severity analysis.

Multi-user support with roles and permissions.

Add mobile-friendly interface with push notifications.

Contribution
Contributions are welcome!

Fork the repository

Create a feature branch

Commit changes

Open a pull request
