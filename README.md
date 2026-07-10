# 🌲🔥 Forest Fire Alert Agent

A simple AI-powered forest fire alert assistant using **OpenAI GPT-4o-mini** and a clean **Gradio UI**.  
Reads simulated forest heat-sensor data in real time and gives clear, friendly safety advice.

---

## 📁 Project Structure

```
forest-fire-alert-agent/
│
├── app.py                  ← Gradio UI  (run this to start)
├── agent.py                ← Core AI agent (OpenAI GPT-4o-mini)
├── sensor_simulator.py     ← Simulates heat sensor readings
├── test_agent.py           ← Quick test before launching UI
│
├── .env.template           ← Copy this → rename to .env → add API key
├── .env                    ← ⚠️  Your real key goes here (never commit!)
├── requirements.txt        ← Python dependencies
├── .gitignore              ← Keeps .env out of git
└── README.md               ← This file
```

---

## ⚡ Quick Start (5 steps)

### 1. Clone or download the project
```bash
cd forest-fire-alert-agent
```

### 2. Create a virtual environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
```bash
# Copy the template and open it
copy .env.template .env       # Windows
# OR
cp .env.template .env         # macOS / Linux
```
Open `.env` and replace the placeholder:
```env
OPENAI_API_KEY=sk-your-real-api-key-here
```
> Get your API key at: https://platform.openai.com/api-keys

### 5. Run the app
```bash
python app.py
```
Your browser will open automatically at **http://127.0.0.1:7860** 🚀

---

## 🧪 Test Without the UI

```bash
python test_agent.py
```
This tests the sensor simulator (no API key needed) and the full AI agent (API key required).

---

## 🌡️ How It Works

```
User Question
     │
     ▼
Sensor Simulator ──────► Live Heat Readings (5 forest zones)
     │
     ▼
AI Agent (GPT-4o-mini) ── reads sensor data + user question
     │
     ▼
Friendly Safety Response ──► Gradio UI
```

### Forest Zones Monitored
| Zone | Location |
|------|----------|
| ZONE-A | North Ridge Forest |
| ZONE-B | Valley Stream Area |
| ZONE-C | East Slope Woodland |
| ZONE-D | South Pine Cluster |
| ZONE-E | Central Grove Station |

### Alert Levels
| Level | Temp (°C) | Meaning |
|-------|-----------|---------|
| 🟢 NORMAL | < 45 | All clear — safe conditions |
| 🟡 WARNING | 45–59 | Elevated heat — monitor closely |
| 🟠 DANGER | 60–79 | High risk — prepare response |
| 🔴 CRITICAL | ≥ 80 | **FIRE DETECTED — act immediately!** |

### Scenario Selector (UI)
| Scenario | Simulates |
|----------|-----------|
| 🟢 Normal | Typical forest temperatures |
| 🟡 Elevated | One zone heating up (early warning) |
| 🔴 Active Fire | One zone at critical temperature |

---

## 🔒 Security Notes

- ✅ API key stored in `.env` — **never hardcoded**
- ✅ `.env` is in `.gitignore` — **never committed**
- ✅ Only reads from OpenAI — no data sent to third parties

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Model | OpenAI GPT-4o-mini |
| UI Framework | Gradio |
| API Client | openai Python SDK |
| Env Management | python-dotenv |
| Sensor Data | Simulated (Python) |

---

## 🌱 Future Enhancements

- Connect to real IoT heat sensors via MQTT or REST API
- Add SMS/email alerts using Twilio or SendGrid
- Display sensor data on a live forest map (Leaflet.js)
- Store alert history in a SQLite database
- Deploy to the cloud (Google Cloud Run / AWS Lambda)
