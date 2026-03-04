# /// script
# dependencies = [
# ]
# ///

import os
import sys
import argparse
import shutil
import subprocess
from pathlib import Path

def run_command(cmd):
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Error executing command: {cmd}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Modular 3D Scroll Pipeline")
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--prompt", required=True, help="Base prompt for generation")
    parser.add_argument("--step", choices=["start", "end", "video", "web", "all"], default="all", 
                        help="Specific step to run (default: all)")
    
    args = parser.parse_args()
    
    # Path Setup
    project_dir = Path(f"projects/{args.name}")
    source_dir = project_dir / "source"
    www_dir = project_dir / "www"
    frames_dir = www_dir / "assets" / "frames"
    temp_png_dir = source_dir / "temp_png"
    
    # Ensure project structure
    source_dir.mkdir(parents=True, exist_ok=True)
    www_dir.mkdir(parents=True, exist_ok=True)

    print(f"--- Project: {args.name} | Step: {args.step} ---")

    # 1. STEP: START FRAME
    if args.step in ["start", "all"]:
        start_path = source_dir / "start.png"
        if start_path.exists() and args.step != "start":
            print(">> Skipping Start Frame (Already exists)")
        else:
            print(">> Generating Start Frame...")
            run_command(f'python3 tools/generate_image.py --prompt "{args.prompt}" --output "{start_path}" --aspect_ratio "16:9"')

    # 2. STEP: END FRAME
    if args.step in ["end", "all"]:
        end_path = source_dir / "end.png"
        if end_path.exists() and args.step != "end":
            print(">> Skipping End Frame (Already exists)")
        else:
            print(">> Generating End Frame...")
            run_command(f'python3 tools/generate_image.py --prompt "{args.prompt}, nighttime neon glow" --output "{end_path}" --aspect_ratio "16:9"')

    # 3. STEP: VIDEO
    if args.step in ["video", "all"]:
        video_path = source_dir / "transition.mp4"
        start_path = source_dir / "start.png"
        end_path = source_dir / "end.png"
        
        if video_path.exists() and args.step != "video":
            print(">> Skipping Video Generation (Already exists)")
        else:
            if not start_path.exists() or not end_path.exists():
                print("Error: Video requires start and end frames. Run with --step all or generate them first.")
                sys.exit(1)
            print(">> Generating Interpolated Video...")
            run_command(f'python3 tools/generate_video.py --prompt "A smooth transition for: {args.prompt}" --start "{start_path}" --end "{end_path}" --output "{video_path}"')

    # 4. STEP: WEB PACKAGE
    if args.step in ["web", "all"]:
        video_path = source_dir / "transition.mp4"
        start_path = source_dir / "start.png"
        end_path = source_dir / "end.png"

        if not video_path.exists():
            print("Error: Web packaging requires transition.mp4. Run previous steps first.")
            sys.exit(1)

        print(">> Packaging Web Component...")
        
        # Fresh copy of blueprint
        if (www_dir / "js").exists(): shutil.rmtree(www_dir / "js")
        if (www_dir / "css").exists(): shutil.rmtree(www_dir / "css")
        shutil.copytree("blueprint/js", www_dir / "js")
        shutil.copytree("blueprint/css", www_dir / "css")
        shutil.copy2("blueprint/index.html", www_dir / "index.html")

        # Process Frames
        temp_png_dir.mkdir(exist_ok=True)
        # We start with the high-res generated start frame
        shutil.copy2(start_path, temp_png_dir / "frame_0000.png")
        
        print("Extracting video frames...")
        run_command(f'ffmpeg -y -i "{video_path}" -start_number 1 "{temp_png_dir}/frame_%04d.png"')
        
        # Stitch end frame
        video_frames = [f for f in temp_png_dir.glob("frame_0*.png") if f.name != "frame_0000.png"]
        last_num = len(video_frames)
        shutil.copy2(end_path, temp_png_dir / f"frame_{str(last_num + 1).zfill(4)}.png")
        
        total_count = last_num + 2
        
        # Update build config in index.html
        index_path = www_dir / "index.html"
        with open(index_path, "r") as f:
            content = f.read()
        content = content.replace("frameCount: 194", f"frameCount: {total_count}")
        with open(index_path, "w") as f:
            f.write(content)

        # Convert to WebP
        if frames_dir.exists(): shutil.rmtree(frames_dir)
        run_command(f'python3 tools/convert_to_webp.py --input "{temp_png_dir}" --output "{frames_dir}"')
        
        # Cleanup temp
        shutil.rmtree(temp_png_dir)
        
        print(f"--- Build Complete: projects/{args.name}/www/index.html ---")
        print(f"Total Frames: {total_count}")

if __name__ == "__main__":
    main()
