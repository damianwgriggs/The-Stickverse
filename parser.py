import google.generativeai as genai
import json
import os

# --- CONFIG ---
API_KEY = "YOURAPIPASTEHERE"
INPUT_TEXT_FILE = "story.txt"
OUTPUT_JSON_FILE = "script_plan.json"

genai.configure(api_key=API_KEY)

def parse_screenplay():
    # 1. Read the raw text file
    if not os.path.exists(INPUT_TEXT_FILE):
        print(f"Error: Create a file named '{INPUT_TEXT_FILE}' with your story first!")
        return

    with open(INPUT_TEXT_FILE, 'r') as f:
        raw_text = f.read()

    print(f"📖 Reading '{INPUT_TEXT_FILE}'...")
    print("🤖 Sending to Gemini for breakdown...")

    # 2. The System Prompt (Crucial for getting clean JSON)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    system_prompt = """
    You are a Screenplay parsing engine. Convert the following raw text story into a structured JSON animation script.
    
    RULES:
    1. Identify every character speaking.
    2. Identify scene changes (backgrounds).
    3. Output JSON ONLY. No markdown, no explanations.
    
    JSON STRUCTURE:
    [
      { "type": "background", "description": "A sunny park with a bench" },
      { "type": "speak", "character": "Steve", "text": "Hello world!" },
      { "type": "action", "description": "Steve jumps in the air" },
      { "type": "speak", "character": "Bob", "text": "Hi Steve." }
    ]
    """

    response = model.generate_content(system_prompt + "\n\nSTORY:\n" + raw_text)

    # 3. Clean and Save JSON
    try:
        # Strip markdown if Gemini adds it (e.g. ```json ... ```)
        cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
        script_data = json.loads(cleaned_text)
        
        with open(OUTPUT_JSON_FILE, 'w') as f:
            json.dump(script_data, f, indent=4)
            
        print(f"✅ Success! Parsed script saved to '{OUTPUT_JSON_FILE}'")
        print(f"   Now run 'director.py' to record your lines.")
        
    except json.JSONDecodeError:
        print("❌ Error: Gemini didn't return valid JSON. Here is what it said:")
        print(response.text)

if __name__ == "__main__":
    parse_screenplay()
