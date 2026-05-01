# Usage Guide

Follow this sequence to ensure the system operates correctly:

### Step 1: Initialize Database (First time only)
```powershell
python server/init_db.py
```

### Step 2: Start the Backend Server
Open a new terminal and run:
```powershell
python server/app.py
```

### Step 3: Start the Monitoring Dashboard
Open another terminal and run:
```powershell
streamlit run server/dashboard.py
```

### Step 4: Run Security Tests
Open a final terminal to simulate device data transmissions and security attacks:
```powershell
python server/main_test.py
```
