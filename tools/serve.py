# /// script
# dependencies = [
# ]
# ///

import http.server
import socketserver
import argparse
import os
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Serve a project or directory locally")
    parser.add_argument("--name", help="Name of the project to serve (from projects/)")
    parser.add_argument("--path", help="Direct path to a directory to serve")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve on")
    
    args = parser.parse_args()
    
    if args.path:
        serve_dir = Path(args.path)
    elif args.name:
        serve_dir = Path(f"projects/{args.name}/www")
    else:
        print("Error: Either --name or --path must be provided.")
        return

    if not serve_dir.exists():
        print(f"Error: Directory '{serve_dir}' not found.")
        return

    print(f"Serving from: {serve_dir.absolute()}")
    os.chdir(serve_dir)
    
    Handler = http.server.SimpleHTTPRequestHandler
    Handler.extensions_map.update({
        '.webp': 'image/webp',
        '.js': 'application/javascript',
    })

    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", args.port), Handler) as httpd:
        print(f"--- Local Server active at: http://localhost:{args.port} ---")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server.")

if __name__ == "__main__":
    main()
