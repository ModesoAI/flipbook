import subprocess
import sys
import os

def bootstrap():
    """Ensure all required dependencies are present before importing MCP."""
    # 'fastmcp' is included in the official 'mcp' package, no need to install separately
    required = ["mcp", "requests", "python-dotenv"]
    try:
        import mcp
        # FIX 1: Capitalized FastMCP correctly
        from mcp.server.fastmcp import FastMCP 
        import requests
        import dotenv
    except ImportError as e:
        print(f"Missing dependency ({e}). Installing: {required}...", file=sys.stderr)
        try:
            # FIX 2: Redirect pip output to stderr to protect the MCP handshake
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install"] + required,
                stdout=sys.stderr,
                stderr=sys.stderr
            )
            print("Dependencies installed successfully. Restarting...", file=sys.stderr)
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as err:
            print(f"FATAL: Could not install dependencies: {err}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    bootstrap()
    
    # NOW we can safely import and run
    from mcp.server.fastmcp import FastMCP # Capitalized correctly
    from pathlib import Path
    
    # Capitalized correctly
    mcp = FastMCP("Flipbook Engine")
    ROOT_DIR = Path(__file__).parent.absolute()

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", default=".", help="Workspace path")
    # Using parse_known_args in case fastmcp passes its own args
    args, unknown = parser.parse_known_args()
    workspace_path = args.workspace

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
        
        # Use the current Python executable
        cmd = [sys.executable, str(sync_script), "--name", name, "--quality", quality, "--workspace", workspace_path]
        
        if prompt:
            cmd.extend(["--prompt", prompt])
        if background_color:
            cmd.extend(["--background-color", background_color])
        if video_input:
            cmd.extend(["--video-input", video_input])

        try:
            # We run the sync.py logic without changing cwd, as sync.py now handles the absolute pathing
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=workspace_path)
            return f"SUCCESS_PROJECT_GENERATED: {name}\nWORKSPACE: {workspace_path}\nOutput: {result.stdout}"
        except subprocess.CalledProcessError as e:
            return f"FAILURE_PROJECT_GENERATED: {name}\nWORKSPACE: {workspace_path}\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}\nSTR_ERROR: {str(e)}"

    mcp.run()