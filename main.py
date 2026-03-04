import subprocess
import sys
import os
from pathlib import Path
from mcp.server.fastmcp import Fastmcp

# Initialize FastMCP server
mcp = Fastmcp("Flipbook Engine")

# Helper to find the project root (where this script lives)
ROOT_DIR = Path(__file__).parent.absolute()

@mcp.tool()
def generate_flipbook(
    name: str,
    prompt: str = None,
    background_color: str = "black",
    quality: str = "fast",
    video_input: str = None
) -> str:
    """
    Generates a high-performance 3D scroll-driven flipbook website.
    
    Args:
        name: Unique name for the project.
        prompt: Text prompt describing the 3D transition (required if not using video_input).
        background_color: Solid background color for the scene (e.g., 'black', 'white').
        quality: Generation tier ('fast' or 'premium'). Defaults to 'fast'.
        video_input: Optional path to an existing MP4 to use instead of generating AI frames.
    """
    sync_script = ROOT_DIR / "pipeline" / "sync.py"
    
    # Use the current Python executable (which will be the venv one)
    cmd = [sys.executable, str(sync_script), "--name", name, "--quality", quality]
    
    if prompt:
        cmd.extend(["--prompt", prompt])
    if background_color:
        cmd.extend(["--background-color", background_color])
    if video_input:
        cmd.extend(["--video-input", video_input])

    try:
        # We run the sync.py logic within the current venv
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return f"Successfully generated flipbook project '{name}'.\nOutput: {result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Error generating flipbook: {e.stderr or str(e)}"

if __name__ == "__main__":
    mcp.run()
