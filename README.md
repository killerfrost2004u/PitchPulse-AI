# PitchPulse AI

Multimodal Soccer Tactical Analyst with a Hybrid Edge/Cloud Architecture.

## Architecture
- **Edge Vision (Local):** YOLOv8 Nano + OpenCV tracking on constrained hardware.
- **Backend:** Python, Flask, Flask-SocketIO.
- **Frontend:** Next.js, React, Tailwind CSS, HTML5 Canvas.
- **Cloud Intelligence:** Google Gemini API (Tactical Reasoning) & Deepgram/Whisper (Audio).

## Setup
### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
