🎬 The Stickverse Engine

**A Poor Man's Pixar built with Python, Gemini, and OpenCV.**

The Stickverse is an open-source, text-to-animation pipeline. It takes a raw text story, uses AI to break it down into a screenplay, forces you to record the voice lines (because AI voices have no soul), and procedurally animates the result into a lip-synced MP4.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Gemini](https://img.shields.io/badge/AI-Gemini-orange)
![OpenCV](https://img.shields.io/badge/Render-OpenCV-green)

## ⚡ How it Works

1.  **The Writer (`parser.py`):** Uses Google Gemini to convert raw text into a structured JSON animation plan.
2.  **The Director (`director.py`):** A CLI teleprompter that records your voice lines for each character.
3.  **The Animator (`animator.py`):** Analyzes audio volume for lip-flap animation and renders the video using OpenCV and MoviePy.

---

## 🛠️ Installation

### 1. Clone the Repo
```bash
git clone [https://github.com/YOUR_USERNAME/stickverse.git](https://github.com/YOUR_USERNAME/stickverse.git)
cd stickverse
2. Install Dependencies
You need a few heavy hitters for audio processing and video rendering.

Bash

pip install google-generativeai sounddevice numpy scipy opencv-python moviepy
Note: You may need to install FFmpeg on your system if MoviePy complains.

3. Get an API Key
You need a Google Gemini API Key (it's free for reasonable usage).

Go to Google AI Studio.

Create an API Key.

Open parser.py and paste it here:

Python

API_KEY = "PASTE_YOUR_KEY_HERE"
🚀 Usage
Step 1: Write the Story
Create a file named story.txt. Write your dialogue. Use standard screenplay format or just paragraphs.

Example story.txt:

Plaintext

The scene is a vast desert.
Walter: "Jesse, we have to cook. The code isn't going to write itself."
Jesse: "I don't know Mr. White, I think I missed a semicolon."
Step 2: Parse the Script
Run the parser. This sends your story to Gemini and creates script_plan.json.

Bash

python parser.py
Step 3: Record Lines
Run the director. It will guide you through the lines one by one.

Bash

python director.py
Pro Tip: Wait for the countdown, or press Ctrl+C to skip the timer and record immediately.

The audio files will be saved in the ./audio folder.

Step 4: Render
Run the animator. This stitches the audio and the vector graphics together.

Bash

python animator.py
Your video will be saved as final_movie.mp4.

🎨 Customizing the Stickverse
This is an Open Universe. You are encouraged to modify animator.py to add your own characters, props, and backgrounds.

Adding New Characters
Open animator.py and look for the draw_frame function. Add your characters to the dictionary:

Python

chars = {
    "Steve": (400, BLUE),    # Name: (X-Position, Color)
    "Bob": (880, GREEN),
    "Walter": (400, (255, 0, 0)), # Blue (BGR format)
    "Jesse": (880, (0, 255, 255)) # Yellow
}
Note: The system tries to match the character name from the script to this dictionary. It is case-insensitive.

Adding Backgrounds
In the same draw_frame function, look for the background logic:

Python

if "space" in background_type.lower():
    img[:] = (20, 20, 20) # Dark Grey Background
elif "desert" in background_type.lower():
    img[:] = (180, 230, 255) # Sky Color
    cv2.rectangle(img, (0, 500), (1280, 720), (100, 200, 240), -1) # Sand
🤝 Contributing
Want to add a function that draws hats? Want to implement camera shake when characters yell?

Fork the Project.

Create your Feature Branch (git checkout -b feature/AmazingHats).

Commit your Changes (git commit -m 'Added Heisenberg Hat').

Push to the Branch (git push origin feature/AmazingHats).

Open a Pull Request.

📄 License
Distributed under the MIT License. See LICENSE for more information.


***

### One last thing for you (The User)
Don't forget to create a `requirements.txt` file in your folder so people can install everything at once. You can just run this command in your terminal to generate it:

`pip freeze > requirements.txt` 

Or just paste this into a file named `requirements.txt`:
```text
google-generativeai
sounddevice
numpy
scipy
opencv-python
moviepy
