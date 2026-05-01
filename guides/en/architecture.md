# System Architecture Documentation

## 1. Multi-layered Security Model
The system implements application-layer security mechanisms independent of underlying transport protocols. The model integrates Authenticated Encryption with Associated Data (AEAD) and Hash-based Message Authentication Code (HMAC).

### 1.1. Node Entity Layer (End-to-End Encryption)
- **Algorithm:** AES-128-GCM.
- **Function:** Ensures data confidentiality and integrity from Node to Server.
- **Parameters:** Utilizes a random 96-bit Nonce per session to mitigate cryptographic analysis attacks.

### 1.2. Gateway Layer (Authentication Overlay)
- **Algorithm:** HMAC-SHA256.
- **Function:** Authenticates the Gateway entity and ensures packet integrity over the Internet.
- **Mechanism:** The Gateway signs the encrypted Node packet, enabling the Server to verify the data source accurately.

## 2. Data Processing Workflow
1. **Initialization:** The Node encapsulates sensor data with a monotonic Sequence Number.
2. **Layer 1 Encryption:** The Node executes AES-GCM encryption using the `NODE_KEY`.
3. **Layer 2 Signing:** The Gateway receives the packet, appends the `Gateway ID`, and executes HMAC signing using the `GATEWAY_KEY`.
4. **Verification & Decryption:** The Server validates the HMAC before initiating the internal AES-GCM decryption.
