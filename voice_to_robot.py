import sounddevice as sd
import numpy as np
import whisper
import requests
import scipy.io.wavfile as wavfile
import tempfile
import time

# Load Whisper model only once
model = whisper.load_model("base")  # or "tiny" for speed

def record_and_transcribe():
    samplerate = 16000
    duration = 4  # seconds
    print("🎤 Listening... (Speak now)")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()

    # Save temp WAV
    temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wavfile.write(temp.name, samplerate, audio)

    print("🧠 Transcribing...")
    result = model.transcribe(temp.name)
    text = result["text"].strip()
    return text

def send_command_to_robot(command_text):
    print(f"📝 You said: \"{command_text}\"")
    if command_text:
        try:
            response = requests.post(
                "http://localhost:8000/api/parse-command/",
                json={"command": command_text}
            )
            if response.status_code == 200:
                print("✅ Robot responded:", response.json())
            else:
                print("❌ Failed:", response.text)
        except Exception as e:
            print("🚫 Error:", str(e))
    else:
        print("⚠️ No command detected.")

print("🤖 Voice Assistant Ready (press Ctrl+C to stop)")
try:
    while True:
        text = record_and_transcribe()
        send_command_to_robot(text)
        print("\n⏳ Waiting for next command...\n")
        time.sleep(1)
except KeyboardInterrupt:
    print("👋 Exiting. Voice assistant stopped.")
