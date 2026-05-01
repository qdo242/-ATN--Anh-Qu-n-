# System Architecture

### 1. Secure Data Flow
- **At the Node:** Sensor data is encrypted using AES-128-GCM, generating a Ciphertext and an Authentication Tag.
- **At the Gateway:** The Gateway appends its Identifier (ID) and signs the entire packet with an HMAC-SHA256 digital signature.
- **At the Server:** The Server verifies the HMAC to authenticate the Gateway, then decrypts the AES layer to retrieve the Node data.

### 2. Protection Layers
- **Layer 1 (HMAC):** Authenticates the Gateway origin and prevents packet tampering over the Internet.
- **Layer 2 (AES-GCM):** End-to-end encryption for sensor data, ensuring confidentiality even if the Gateway is compromised.
- **Layer 3 (Sequence Number):** Prevents Replay Attacks by verifying the message sequence number.
