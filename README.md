# 3D Scroll Narrative Generator (Modular Pipeline)

A robust, persistent, and step-based pipeline for generating 3D scroll-driven landing pages.

## 📁 Project Structure
Every project is isolated and persistent:
- **`projects/{name}/source/`**: Raw generated assets (start/end PNGs, transition MP4).
- **`projects/{name}/www/`**: The final optimized website (index.html, WebP frames).

## 🚀 The Modular Workflow

The pipeline supports incremental steps. If you rerun a command, it will skip already completed steps unless specified.

### 1. Run the Full Pipeline
```bash
python3 pipeline/sync.py --name "my-project" --prompt "A vibrant 8-bit futuristic city" --background-color "black"
```

### 2. Run Individual Steps
- **Start Image only:** `--step start --background-color "#000000"`
- **End Image only:** `--step end --background-color "#000000"`
- **Video Morph only:** `--step video`
- **Web Package only:** `--step web`

Example (Generate only the web component from existing assets):
```bash
python3 pipeline/sync.py --name "my-project" --prompt "..." --step web
```

### 3. View the Project
```bash
python3 tools/serve.py --name "my-project"
```
Access at: **http://localhost:8000**

---

## 🎨 Pre-generated Examples

The project includes pre-built examples showcasing different styles and narratives. These are self-contained in the `example/` directory:

- **Cyber City**: A vibrant, high-contrast futuristic urban environment.
- **Industrial Evolution**: A transition from raw machinery to a polished mechanical future.
- **Space Ascent**: An atmospheric journey from orbit into deep space.

To view these examples, you can serve the `example/` directory directly or navigate to it in your local development environment.

## 📦 Integration
For instructions on how to copy these assets into an existing external project, see [docs/integration.md](docs/integration.md).

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
