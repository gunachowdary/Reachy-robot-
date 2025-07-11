import websocket
import json
import time

# Only the 5 presets that are implemented in Unity handler
keyboard_presets = [
    "wave",
    "nod",
    "shake",
    "raise_left",
    "lower_left",
    "raise_left",
    "lower_left",
    "raise_right",
    "lower_right",
    "reset"
]

def send_preset_command(preset):
    message = json.dumps({"preset": preset})
    try:
        ws = websocket.create_connection("ws://localhost:8765/")
        ws.send(message)
        ws.close()
        print(f"✅ Sent preset: {preset}")
    except Exception as e:
        print(f"❌ Error sending '{preset}': {e}")

def run_all_presets():
    for preset in keyboard_presets:
        send_preset_command(preset)
        time.sleep(2)  # Give time for each action

if __name__ == "__main__":
    run_all_presets()
