# Flipbook // 3D Scroll Narrative Engine

**High-performance, 3D scroll-driven narrative engine. Orchestrate AI-generated or cinematic video sequences into butter-smooth, frame-by-frame landing pages.**

Flipbook is a lightweight, zero-dependency engine designed to transform video sequences and AI-generated morphs into immersive scroll-driven experiences. Built with a "performance-first" philosophy, it prioritizes hardware-accelerated rendering and temporal coherence to eliminate the stutter common in traditional scroll animations.

## 🛠 Prerequisites

Before running the pipeline or the skill, ensure you have a `.env` file in the root directory with your API key:

```env
GEMINI_API_KEY=your_api_key_here
```

This key is required for both image and video generation via the Google AI (Generative Language) API. No Google Cloud Project ID is required for the default setup.

## 📁 Project Structure
Every project is isolated and persistent:
- **`projects/{name}/source/`**: Raw generated assets (start/end PNGs, transition MP4).
- **`projects/{name}/www/`**: The final optimized website (index.html, WebP frames).

## 🚀 The Modular Workflow

The pipeline supports incremental steps. If you rerun a command, it will skip already completed steps unless specified.

### 1. Run the Full Pipeline
```bash
python3 pipeline/sync.py --name "my-project" --prompt "A vibrant city" --background-color "black" --quality "fast"
```

### 2. Run Individual Steps
- **Start Image only:** `--step start --quality "premium"`
- **End Image only:** `--step end --quality "premium"`
- **Video Morph only:** `--step video --quality "fast"`
- **Web Package only:** `--step web`

Example (Generate only the web component from existing assets):
```bash
python3 pipeline/sync.py --name "my-project" --prompt "..." --step web
```

### 3. Direct Video Input (Skip Generation)
If you already have a video, you can create a flipbook directly:
```bash
python3 pipeline/sync.py --name "my-project" --video-input "/path/to/my-video.mp4"
```

---

## 🧩 CLI Extension (Recommended)

You can install Flipbook as a formal extension in your Gemini CLI. This allows you to orchestrate 3D scroll experiences through natural language and manage them with specialized MCP tools.

### 1. Install
From the project root:
```bash
gemini extensions install .
```

### 2. Available MCP Tools
Once installed, the following tools are available to the AI (and you via `/mcp call`):
- **`generate_flipbook(name, prompt)`**: Trigger the full generation pipeline.
- **`list_items()`**: List all generated projects and built-in examples.
- **`preview_item(name, is_example)`**: Start a background server to preview a project or example.

---

## 🤖 Gemini CLI Skill (Agent Expertise)

If you are using the **Gemini CLI**, you can activate the **flipbook-skill** to give the AI expert knowledge of the pipeline.

### 1. Activate the Skill
```bash
/activate_skill flipbook-skill
```

### 2. Use the Skill
Ask the AI to design and build for you:
> "Use the flipbook-skill to create a new project called 'cyber-neon'. The theme is 'A futuristic city' and use a black background."

---

## 🎨 Pre-generated Examples

The project includes three distinct architectural patterns for 3D scroll narratives:

### Example 0: Direct Video Input (Drone Flight)
Showcases how to create a high-performance flipbook directly from an existing MP4 file without AI generation.
```bash
python3 tools/serve.py --path "example-0"
```

### Example 1: Orchestrated Cross-Fade
A sophisticated layout where multiple modules (Cyber City, Industrial, Space) cross-fade into each other on a single fixed canvas.
```bash
python3 tools/serve.py --path "example-1"
```

### Example 2: Spatial Sliding (Void Pro)
A premium "Void Pro" landing page where sections physically slide and overlap, pushing the previous scene out of the viewport.
```bash
python3 tools/serve.py --path "example-2"
```

Access all at: **http://localhost:8000**

## 📦 Integration
For instructions on how to copy these assets into an existing external project, see [docs/integration.md](docs/integration.md).

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
