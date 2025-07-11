# Reachy Robot – Voice-to-Motion AI Assistant

This project demonstrates an end-to-end AI assistant pipeline where natural-language or voice commands control a simulated humanoid robot (Reachy Mini) using Unity, Django, Whisper, and Meta’s LLaMA 4 Scout model via Groq API.

---

## 🛠 Tools Used

- Unity 2021.3.45f1 – Reachy Mini simulation environment  
- Python + Django – Backend server and WebSocket handler  
- Groq API + Meta LLaMA 4 Scout (17B) – Language model for command interpretation  
- Whisper (base) – Speech-to-text transcription  
- websocket-sharp.dll – Unity WebSocket communication  
- grpc.core / protobuf DLLs – Unity dependency resolution  

---

## 🚀 How It Works

### Part A – Simulation Setup

- Reachy Mini model imported into Unity (open-source from Pollen Robotics)  
- Added `KeyboardReachyControl.cs` for 15 gesture animations triggered via keypress (A–Z)  
- Added `ReachyController.cs` for low-level joint motor control  

### Part B – LLM Integration

- Django backend receives user input via API  
- Sends text to Groq-hosted **Meta LLaMA 4 Scout (17B)** model  
- Model returns structured JSON with motor actions (e.g., `{"r_shoulder_pitch": 30}`)  
- JSON is sent via WebSocket to Unity, where `WebSocketReceiver.cs` parses it and triggers joint/gesture movement  

### Part C – Voice Input (Optional)

- Audio captured using `sounddevice`  
- Transcribed using Whisper (base model)  
- Transcription passed to backend → LLM → robot movement, enabling full voice-to-motion control  

---

## 🧪 Example Commands

- "Raise your right hand"  
- "Reset the position"  
- "Wave"  
- "Raise your left hand"

---

## 📂 Project Structure

```plaintext
abide robotics/
├── backend/                 # Django backend
├── robotapi/               # API logic (LLM & WebSocket integration)
├── voice_to_robot.py       # Voice-to-text-to-action script
├── test_post.py            # Sample structured command tester
├── reachy-unity/           # Unity project files (Reachy Mini)
├── README.md


This project uses Groq api key in views.py add your api key 

GROQ_API_KEY – your Groq API access token
