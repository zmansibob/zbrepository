import os
import hashlib
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from TTS.api import TTS

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
PORT = 5559
VOICE_SAMPLE = "zb_voice45.wav"
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
CACHE_DIR = "audio_cache"

# --- THE AUTO-CREATION STAGE ---
# This fixes the missing folder issue you saw in your 'ls' command
if not os.path.exists(CACHE_DIR):
    print(f"📁 Creating storage folder: {CACHE_DIR}")
    os.makedirs(CACHE_DIR)

# --- LOAD MODEL ---
print("🚀 Loading TTS Model (this takes a moment on CPU)...")
device = "cpu"
tts = TTS(MODEL_NAME).to(device)
print("✅ System Ready.")


@app.route('/status', methods=['GET'])
def status():
    # Helps you track how many sentences you've "learned"
    cache_count = len(os.listdir(CACHE_DIR))
    return jsonify({"status": "online", "cache_size": cache_count})


@app.route('/clone', methods=['POST'])
def clone():
    try:
        data = request.json
        text = data.get('text', '').strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Create a unique ID for this specific sentence
        sentence_hash = hashlib.md5(text.encode()).hexdigest()
        cache_path = os.path.join(CACHE_DIR, f"{sentence_hash}.wav")

        # --- THE LIBRARIAN LOGIC ---
        if os.path.exists(cache_path):
            print(f"⚡ CACHE HIT: Found existing audio for: {text[:30]}...")
            return send_file(cache_path, mimetype="audio/wav")

        # --- THE WORKER LOGIC ---
        print(f"🎙️ CACHE MISS: Synthesizing new audio for: {text[:50]}...")

        # We save directly to the disk so we never have to synthesize this text again
        tts.tts_to_file(
            text=text,
            speaker_wav=VOICE_SAMPLE,
            language="en",
            file_path=cache_path,
            enable_text_splitting=True
        )

        return send_file(cache_path, mimetype="audio/wav")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # host='0.0.0.0' allows access from other devices on your local network
    app.run(host='0.0.0.0', port=PORT, debug=False)