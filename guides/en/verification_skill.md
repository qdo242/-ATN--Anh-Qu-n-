# Verification and Validation Methodology

This document outlines the technical procedures to ensure system stability, security, and accuracy before real-world deployment.

## 1. Multi-point Verification Workflow

### 1.1. Unit Testing
- **Objective:** Verify the correctness of individual encryption and decryption functions.
- **Execution:** Check AES-GCM output against sample vectors to ensure alignment with theoretical cryptographic results.

### 1.2. Integration Testing
- **Objective:** Ensure seamless coordination between Node, Gateway, and Server.
- **Execution:** Utilize `main_test.py` to simulate the full data flow from encryption at the Node to storage in the Server database.

### 1.3. Empirical Security Testing
- **Objective:** Demonstrate defensive capabilities against target attack models.
- **Execution Scenarios:**
    - **Gateway Impersonation:** Modify Gateway ID or HMAC signature to confirm Server rejection.
    - **Replay Attack:** Resend captured valid packets to confirm the Sequence Number mechanism.
    - **Data Tampering:** Flip bits in the Ciphertext to confirm that the AES-GCM layer detects integrity violations (MAC check failure).

## 2. Performance Evaluation Criteria
- **Processing Latency:** Measure execution time at the Server from reception to decryption completion. Target: < 50ms per packet.
- **Database Stability:** Test continuous data logging and Telemetry data consistency.

## 3. Environment Cleanup Procedure
Every test run must start from a "clean state":
1. Terminate old processes occupying the Database file.
2. Reset device status to `active`.
3. Reset `last_seq` to -1.
