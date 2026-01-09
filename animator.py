import json
import os
import numpy as np
import cv2
from scipy.io import wavfile

# --- MOVIEPY 2.0+ IMPORTS ---
from moviepy import VideoFileClip, AudioFileClip, VideoClip, CompositeVideoClip, concatenate_videoclips

# --- CONFIGURATION ---
INPUT_SCRIPT = "script_ready.json"
OUTPUT_FILENAME = "final_movie.mp4"
AUDIO_FOLDER = "./audio"
WIDTH, HEIGHT = 1280, 720
FPS = 24

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (255, 0, 0)
YELLOW = (0, 255, 255)
GREEN = (0, 255, 0)

def get_volume_array(audio_path, fps):
    """
    Analyzes audio file to determine mouth openness per frame.
    """
    try:
        sample_rate, data = wavfile.read(audio_path)
    except Exception as e:
        print(f"⚠️ Could not read audio {audio_path}: {e}")
        return []

    # Convert stereo to mono if needed
    if len(data.shape) > 1:
        data = data.mean(axis=1)

    # Normalize data
    max_val = np.max(np.abs(data))
    if max_val > 0:
        data = np.abs(data) / max_val
    else:
        data = np.zeros_like(data)
    
    samples_per_frame = int(sample_rate / fps)
    volume_per_frame = []
    
    for i in range(0, len(data), samples_per_frame):
        chunk = data[i:i+samples_per_frame]
        if len(chunk) > 0:
            vol = np.mean(chunk) * 100 
            volume_per_frame.append(vol)
            
    return volume_per_frame

def draw_frame(t, character_speaking, mouth_open_amount, background_type="default"):
    # 1. Create Canvas (BGR for OpenCV)
    img = np.full((HEIGHT, WIDTH, 3), 255, dtype=np.uint8)

    # 2. Draw Background
    if "desert" in background_type.lower():
        img[:] = (180, 230, 255) 
        cv2.rectangle(img, (0, 500), (1280, 720), (100, 200, 240), -1)
    elif "space" in background_type.lower():
        img[:] = (20, 20, 20)
    else:
        cv2.rectangle(img, (0, 500), (1280, 720), (200, 200, 200), -1)

    # 3. Define Characters
    # Ensure keys match what comes from the JSON (Case Insensitive Fix)
    chars = {
        "Steve": (400, BLUE),
        "Bob": (880, GREEN)
    }

    # Normalize the speaking character name to Title Case (e.g. "bob" -> "Bob")
    # This prevents the "Left guy always speaks" bug if the JSON has lowercase names
    active_speaker = character_speaking.title() if character_speaking else None

    for name, (x, color) in chars.items():
        # Body
        cv2.line(img, (x, 500), (x-30, 600), BLACK, 5)
        cv2.line(img, (x, 500), (x+30, 600), BLACK, 5)
        cv2.line(img, (x, 500), (x, 350), BLACK, 5)
        cv2.line(img, (x, 380), (x-40, 450), BLACK, 5)
        cv2.line(img, (x, 380), (x+40, 450), BLACK, 5)

        # Head Logic
        head_center = (x, 300)
        gap = 0
        
        # KEY FIX: Compare the Title Cased names
        if name == active_speaker:
             gap = int(mouth_open_amount * 20)
             if gap > 60: gap = 60
        
        # Bottom Jaw (Static)
        cv2.ellipse(img, head_center, (50, 50), 0, 0, 180, color, -1)
        cv2.ellipse(img, head_center, (50, 50), 0, 0, 180, BLACK, 3)
        
        # Top Head (Flapping)
        top_center = (x, 300 - gap)
        cv2.ellipse(img, top_center, (50, 50), 0, 180, 360, color, -1)
        cv2.ellipse(img, top_center, (50, 50), 0, 180, 360, BLACK, 3)
        
        # Eyes
        cv2.circle(img, (x-15, 290 - gap), 5, BLACK, -1)
        cv2.circle(img, (x+15, 290 - gap), 5, BLACK, -1)

    # Convert BGR (OpenCV) to RGB (MoviePy expects RGB)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def build_animation():
    print("🚀 STARTING RENDER ENGINE...")
    
    if not os.path.exists(INPUT_SCRIPT):
        print(f"❌ Error: {INPUT_SCRIPT} not found.")
        return

    with open(INPUT_SCRIPT, 'r') as f:
        script = json.load(f)

    final_clips = []
    current_bg = "default"

    for event in script:
        if event['type'] == 'background':
            current_bg = event.get('description', 'default')
            continue

        if event['type'] == 'speak':
            # FIX: Ensure we read the character name cleanly
            char_name = event['character'] 
            audio_file = event.get('audio_file')
            
            if not audio_file:
                continue
                
            path = os.path.join(AUDIO_FOLDER, audio_file)
            
            # Load Audio
            audioclip = AudioFileClip(path)
            duration = audioclip.duration
            
            # Analyze Volume
            volumes = get_volume_array(path, FPS)
            
            # Use default argument capture to safely pass char_name into the lambda
            def make_frame(t, name=char_name): 
                frame_index = int(t * FPS)
                vol = volumes[frame_index] if frame_index < len(volumes) else 0
                return draw_frame(t, name, vol, current_bg)

            # Creating the clip
            clip = VideoClip(make_frame, duration=duration)
            clip = clip.with_audio(audioclip)
            
            final_clips.append(clip)
            
            # Pause clip (0.2 seconds silence between lines)
            def make_pause(t):
                return draw_frame(t, None, 0, current_bg)
                
            pause = VideoClip(make_pause, duration=0.2)
            final_clips.append(pause)

    if not final_clips:
        print("❌ No clips created.")
        return

    print("🎞️  Stitching video together...")
    final_video = concatenate_videoclips(final_clips)
    
    # Write file
    final_video.write_videofile(OUTPUT_FILENAME, fps=FPS, codec='libx264')
    print(f"✅ DONE! Video saved as: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    build_animation()
