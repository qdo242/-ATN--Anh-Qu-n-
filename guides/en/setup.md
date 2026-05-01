# Setup and Testing Guide

This document provides a step-by-step procedure to deploy and verify the IoT data encryption system after cloning the repository.

## 1. Environment Preparation
Requirement: Python 3.9+ installed.

### Step 1: Install Dependencies
Open your terminal in the project directory and run the following command to install cryptographic and UI libraries:
```powershell
pip install pycryptodomex flask streamlit pandas plotly requests python-dotenv
```

### Step 2: Configure Security Settings (.env)
Secret keys are excluded from version control. You must create a new file named `.env` in the project root with the following content:
```text
NODE_KEY=1234567890123456
GATEWAY_KEY=gateway_secret_k
```

## 2. Testing Procedure
To verify that the system is functioning correctly, follow these 4 steps in order (each in a separate terminal window):

### Step 1: Initialize the Database
This command creates the `iot_security.db` file to store device info and logs.
```powershell
python server/init_db.py
```

### Step 2: Start the Backend Server
The server listens for JSON requests on port 5000.
```powershell
python server/app.py
```

### Step 3: Launch the Monitoring Dashboard
This starts the Web interface. You can view the analytics at `http://localhost:8501`.
```powershell
streamlit run server/dashboard.py
```

### Step 4: Run Simulation and Security Tests
Execute this script to send simulated data and attack scenarios (Invalid HMAC, Replay Attacks).
```powershell
python server/main_test.py
```
*Expected Outcome:* Observe the Dashboard for "Safe" messages (green) and "Security Alerts" (red).
