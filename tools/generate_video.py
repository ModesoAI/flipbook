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
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def generate_video(prompt, start_image_path, end_image_path, output_path, quality="fast"):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY must be set in .env")
        sys.exit(1)

    print(f"Generating transition video with Veo 3.1...")
    
    # Ensure output directory exists
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    model_name = "veo-3.1-generate-preview" if quality == "premium" else "veo-3.1-fast-generate-preview"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:predictLongRunning?key={api_key}"
    
    # Prepare payload with First + Last frame interpolation
    instance = {
        "prompt": prompt
    }
    
    if start_image_path and os.path.exists(start_image_path):
        print(f"Using start image: {start_image_path}")
        instance["image"] = {
            "bytesBase64Encoded": get_base64_image(start_image_path),
            "mimeType": "image/png"
        }
        
    if end_image_path and os.path.exists(end_image_path):
        print(f"Using end image: {end_image_path}")
        instance["lastFrame"] = {
            "bytesBase64Encoded": get_base64_image(end_image_path),
            "mimeType": "image/png"
        }

    payload = {
        "instances": [instance],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9", # Corrected to a supported aspect ratio
            "resolution": "720p"
        }
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        operation = response.json()
        
        operation_name = operation.get("name")
        if not operation_name:
            print("Error: No operation name returned from API.")
            print(f"Response: {operation}")
            sys.exit(1)
            
        print(f"Operation started: {operation_name}")

        while True:
            poll_url = f"https://generativelanguage.googleapis.com/v1beta/{operation_name}?key={api_key}"
            poll_resp = requests.get(poll_url)
            poll_resp.raise_for_status()
            status = poll_resp.json()
            
            if status.get("done"):
                if "error" in status:
                    print(f"Error in video generation: {status['error']}")
                    sys.exit(1)
                
                response_data = status.get("response", {})
                print("Generation complete!")
                
                video_uri = None
                gen_response = response_data.get("generateVideoResponse", {})
                samples = gen_response.get("generatedSamples", [])
                if samples:
                    video_uri = samples[0].get("video", {}).get("uri")

                if video_uri:
                    print(f"Downloading video from: {video_uri}")
                    if "?" in video_uri:
                        download_url = f"{video_uri}&key={api_key}"
                    else:
                        download_url = f"{video_uri}?key={api_key}"
                        
                    dl_resp = requests.get(download_url)
                    dl_resp.raise_for_status()
                    
                    with open(output_file, "wb") as f:
                        f.write(dl_resp.content)
                    print(f"Successfully saved video to: {output_file}")
                    return

                print("Success, but couldn't find video URI in response.")
                print(f"Full response: {status}")
                break
            
            print("Still generating... (polling in 20s)")
            time.sleep(20)

    except requests.exceptions.RequestException as e:
        print(f"Error calling Veo API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a transition video using Veo 3.1")
    parser.add_argument("--prompt", required=True, help="The prompt for video generation")
    parser.add_argument("--start", required=False, help="Path to the starting frame image")
    parser.add_argument("--end", required=False, help="Path to the ending frame image")
    parser.add_argument("--output", required=True, help="The output file path")
    parser.add_argument("--quality", choices=["fast", "premium"], default="fast", help="Select the generation quality/cost tier")
    
    args = parser.parse_args()
    generate_video(args.prompt, args.start, args.end, args.output, args.quality)
