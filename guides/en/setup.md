# System Setup

## 1. System Requirements
- Python version 3.9 or higher.
- pip package manager.

## 2. Library Installation
Run the following command in your terminal to install the required dependencies:
```powershell
pip install pycryptodomex flask streamlit pandas plotly requests python-dotenv
```

## 3. Security Configuration (.env)
The `.env` file containing secret keys is excluded from GitHub for security reasons. You must create a new file named `.env` in the project root directory with the following content:
```text
NODE_KEY=1234567890123456
GATEWAY_KEY=gateway_secret_k
```
