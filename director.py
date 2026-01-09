import json
import time
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os

# --- CONFIG ---
INPUT_JSON_FILE = "script_plan.json"
OUTPUT_JSON_FILE = "script_ready.json"
AUDIO_FOLDER = "./audio"
SAMPLE_RATE = 44100

os.makedirs(AUDIO_FOLDER, exist_ok=True)

def record_line(filename):
    print(f"   🎤 RECORDING... (Press Ctrl+C to STOP)")
    recording = []
    try:
        def callback(indata, frames, time, status):
            recording.append(indata.copy())
        
        # Stream starts here
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback):
            while True:
                sd.sleep(100)
    except KeyboardInterrupt:
        print("\n   ✅ Saved.")
    
    if recording:
        my_recording = np.concatenate(recording, axis=0)
        write(filename, SAMPLE_RATE, my_recording)

def run_director():
    if not os.path.exists(INPUT_JSON_FILE):
        print(f"❌ Error: Could not find '{INPUT_JSON_FILE}'. Run parser.py first!")
        return

    with open(INPUT_JSON_FILE, 'r') as f:
        script = json.load(f)

    print("\n🎬 DIRECTOR MODE: 15s Countdown. Ctrl+C to skip wait & Record.\n")

    for index, event in enumerate(script):
        # We only record for "speak" events
        if event['type'] != 'speak':
            continue

        char = event['character']
        text = event['text']
        filename = f"line_{index}_{char}.wav"
        filepath = os.path.join(AUDIO_FOLDER, filename)
        
        # VISUAL INTERFACE
        print("\n" + "="*50)
        print(f"🗣️  CHARACTER: {char.upper()}")
        print(f"📝 LINE: \"{text}\"")
        print("="*50)

        # COUNTDOWN
        try:
            for i in range(15, 0, -1):
                print(f"Time to prepare: {i}  (Ctrl+C to Record NOW)", end='\r')
                time.sleep(1)
        except KeyboardInterrupt:
            pass # Skip timer
        
        # RECORDING
        # We need a tiny pause so the Ctrl+C from the timer doesn't cancel the recording immediately
        time.sleep(0.5) 
        record_line(filepath)
        
        # Update the script data with the file location
        event['audio_file'] = filename

    # Save final build script
    with open(OUTPUT_JSON_FILE, 'w') as f:
        json.dump(script, f, indent=4)
    
    print("\n🎉 That's a wrap! Run 'animator.py' to generate the video.")

if __name__ == "__main__":
    run_director()
