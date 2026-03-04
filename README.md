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

## 🧩 CLI Extension (Recommended for Others)

You can install Flipbook as a formal extension in your Gemini CLI. This allows you to trigger 3D scroll generation through simple natural language prompts without needing to manually run Python scripts.

### 1. Install via GitHub
```bash
gemini extensions install https://github.com/ModesoAI/flipbook
```

### 2. Use via AI Prompt
Once installed, you can simply ask Gemini:
> "Create a high-quality flipbook for a brand called 'Aura' using a transition from light to dark mist. Use a white background."

The extension will automatically handle the pipeline and provide you with the project files.

---

## 🤖 Gemini CLI Skill (Internal Development)

If you are using the **Gemini CLI**, you can automate the entire creative process using the built-in skill.

### 1. Install the Skill
From within the repository, run:
```bash
gemini skills install .gemini/skills/flipbook-skill
```

### 2. Use the Skill
You can now prompt Gemini to create full projects for you:
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
