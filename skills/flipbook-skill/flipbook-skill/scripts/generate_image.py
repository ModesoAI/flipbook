# /// script
# dependencies = [
#   "requests",
#   "python-dotenv",
# ]
# ///

import os
import sys
import argparse
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_image(prompt, output_path, aspect_ratio="1:1"):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY must be set in .env")
        sys.exit(1)

    print(f"Generating image with prompt: {prompt} (Aspect Ratio: {aspect_ratio})")
    
    # Ensure output directory exists
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Using Nano Banana 2 (which is gemini-3.1-flash-image-preview)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            # Note: For multimodal models, some parameters might be top-level or in specific sub-configs
            # Testing the most common valid structure for this specific preview model
        }
    }
    
    # If the model expects it in generationConfig but with a different key name, or as a top-level parameter
    # For now, let's try appending the aspect ratio to the prompt if the API field is failing
    # or use the standard multimodal generation without explicit field if it's strictly beta.
    
    # REVISED: If the API field is unknown, we will embed it in the prompt to ensure consistency 
    # while we wait for official schema stabilization for this preview model.
    modified_prompt = f"{prompt} --aspect_ratio {aspect_ratio}"

    payload["contents"][0]["parts"][0]["text"] = modified_prompt

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        if "candidates" in data and len(data["candidates"]) > 0:
            parts = data["candidates"][0].get("content", {}).get("parts", [])
            for part in parts:
                if "inlineData" in part:
                    image_data_b64 = part["inlineData"].get("data")
                    if image_data_b64:
                        with open(output_file, "wb") as f:
                            f.write(base64.b64decode(image_data_b64))
                        print(f"Successfully generated image: {output_file}")
                        return
                if "text" in part:
                    print(f"API returned text: {part['text']}")
            
            print("Error: No image data found in response parts.")
            sys.exit(1)
        else:
            print("Error: No candidates returned from API.")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an image using Nano Banana 2")
    parser.add_argument("--prompt", required=True, help="The prompt for image generation")
    parser.add_argument("--output", required=True, help="The output file path")
    parser.add_argument("--aspect_ratio", default="1:1", help="Aspect ratio (e.g., 1:1, 16:9)")
    
    args = parser.parse_args()
    generate_image(args.prompt, args.output, args.aspect_ratio)
