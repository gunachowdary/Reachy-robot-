import json
import requests
import websocket  # pip install websocket-client
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  

# ✅ WebSocket Forwarding Function
def forward_to_unity(action_json_str):
    try:
        ws = websocket.create_connection("ws://localhost:8765/")
        ws.send(action_json_str)
        ws.close()
        print("✅ Sent to Unity via WebSocket")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")

@csrf_exempt
def parse_command(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_command = data.get("command", "")

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            # ✅ Limited to only known Reachy gesture presets
            prompt = (
                "You are a robot controller. Convert the user's command into one of the following JSON presets only:\n\n"
                "Valid presets: \"wave\", \"nod\", \"shake\", \"raise_left\", \"lower_left\", "
                "\"raise_right\", \"lower_right\", \"reset\"\n\n"
                "Example: {\"preset\": \"wave\"}\n\n"
                "Respond ONLY with the JSON object. Do NOT include explanations, markdown, or extra text."
            )

            payload = {
                "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_command}
                ],
                "temperature": 0.2,
                "max_tokens": 512
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )

            raw_output = response.json()["choices"][0]["message"]["content"].strip()
            print(f"📤 Raw LLM Output: {raw_output}")

            # ✅ Clean markdown formatting if LLM returns ```json
            if raw_output.startswith("```"):
                raw_output = raw_output.strip("`").split("\n", 1)[-1].rsplit("\n", 1)[0].strip()

            try:
                json_obj = json.loads(raw_output)

                # ✅ Check that "preset" key exists
                if "preset" not in json_obj:
                    return JsonResponse({"error": "Missing 'preset' key in response", "raw": raw_output}, status=400)

                clean_json = json.dumps(json_obj)
                forward_to_unity(clean_json)

                return JsonResponse({"action": json_obj})
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON returned by LLM", "raw": raw_output}, status=400)

        except Exception as e:
            return JsonResponse(
                {"error": str(e), "raw_response": response.json() if 'response' in locals() else {}},
                status=500
            )

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
