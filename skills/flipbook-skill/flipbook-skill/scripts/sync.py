# /// script
# dependencies = [
# ]
# ///

import os
import sys
import argparse
import shutil
import subprocess
import json
from pathlib import Path

def run_command(cmd):
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Error executing command: {cmd}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Modular 3D Scroll Pipeline")
    # ... (existing args)
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--prompt", help="Base prompt for generation (Required if generating)")
    parser.add_argument("--video-input", help="Path to an existing MP4 video to use directly")
    parser.add_argument("--background-color", help="Background color")
    parser.add_argument("--quality", choices=["fast", "premium"], default="fast", help="Select the generation quality/cost tier")
    parser.add_argument("--step", choices=["start", "end", "video", "web", "all"], default="all")
    parser.add_argument("--workspace", default=".", help="Workspace base directory")
    
    args = parser.parse_args()

    # Identify the extension root directory relative to this script
    script_dir = Path(__file__).parent.absolute()
    extension_root = script_dir.parent
    
    # Absolute paths for internal assets
    # Root-level layout (e.g. workspace)
    tools_dir = extension_root / "tools"
    blueprint_dir = extension_root / "blueprint"
    
    # Skill-level layout (e.g. installed skill)
    if not tools_dir.exists():
        tools_dir = extension_root / "scripts"
    if not blueprint_dir.exists():
        blueprint_dir = extension_root / "assets" / "blueprint"
    
    if not blueprint_dir.exists():
        print(f"Error: Could not find blueprint directory at {blueprint_dir}")
        sys.exit(1)
    
    # Base directory for output
    workspace_dir = Path(args.workspace).absolute()
    
    # We will create the projects folder in the workspace if it doesn't exist
    project_dir = workspace_dir / "projects" / args.name
    source_dir = project_dir / "source"
    www_dir = project_dir / "www"
    frames_dir = www_dir / "assets" / "frames"
    temp_png_dir = source_dir / "temp_png"
    
    source_dir.mkdir(parents=True, exist_ok=True)
    www_dir.mkdir(parents=True, exist_ok=True)

    # 0. VIDEO INPUT HANDLING
    if args.video_input:
        print(f">> Using direct video input: {args.video_input}")
        input_path = Path(args.video_input)
        if not input_path.exists():
            print(f"Error: Video input file '{args.video_input}' not found.")
            sys.exit(1)
        shutil.copy2(input_path, source_dir / "transition.mp4")
        # If video is provided, we skip directly to web packaging
        args.step = "web"

    if args.step != "web" and not args.prompt:
        print("Error: --prompt is required unless using --video-input.")
        sys.exit(1)

    bg_arg = f'--background_color "{args.background_color}"' if args.background_color else ""
    q_arg = f'--quality "{args.quality}"'

    # 1 & 2. GENERATION
    if args.step in ["start", "all"]:
        run_command(f'python3 {tools_dir}/generate_image.py --prompt "{args.prompt}" --output "{source_dir}/start.png" --aspect_ratio "16:9" {bg_arg} {q_arg}')
    if args.step in ["end", "all"]:
        run_command(f'python3 {tools_dir}/generate_image.py --prompt "{args.prompt}, nighttime neon glow" --output "{source_dir}/end.png" --aspect_ratio "16:9" {bg_arg} {q_arg}')

    # 3. VIDEO
    if args.step in ["video", "all"]:
        run_command(f'python3 {tools_dir}/generate_video.py --prompt "{args.prompt}" --start "{source_dir}/start.png" --end "{source_dir}/end.png" --output "{source_dir}/transition.mp4" {q_arg}')

    # 4. WEB PACKAGE
    if args.step in ["web", "all"]:
        print(">> Packaging Web Component...")
        
        # Fresh copy of blueprint
        for folder in ["js", "css"]:
            if (www_dir / folder).exists(): shutil.rmtree(www_dir / folder)
            shutil.copytree(f"{blueprint_dir}/{folder}", www_dir / folder)
        shutil.copy2(f"{blueprint_dir}/index.html", www_dir / "index.html")

        # Process Frames
        if temp_png_dir.exists(): shutil.rmtree(temp_png_dir)
        temp_png_dir.mkdir(parents=True)
        
        print("Extracting video frames...")
        run_command(f'ffmpeg -y -i "{source_dir}/transition.mp4" -start_number 0 "{temp_png_dir}/frame_%04d.png"')
        
        all_frames = sorted(list(temp_png_dir.glob("frame_*.png")))
        total_count = len(all_frames)

        # Update frameCount in index.html
        index_path = www_dir / "index.html"
        with open(index_path, "r") as f:
            content = f.read()
        import re
        content = re.sub(r"frameCount:\s*\d+", f"frameCount: {total_count}", content)
        with open(index_path, "w") as f:
            f.write(content)

        # Convert to WebP
        if frames_dir.exists(): shutil.rmtree(frames_dir)
        run_command(f'python3 {tools_dir}/convert_to_webp.py --input "{temp_png_dir}" --output "{frames_dir}"')
        
        shutil.rmtree(temp_png_dir)
        print(f"--- Build Complete: projects/{args.name}/www/index.html ---")
        print(f"Total Frames: {total_count}")


if __name__ == "__main__":
    main()
