# 3D Scroll Narrative Generator (Modular Pipeline)

A robust, persistent, and step-based pipeline for generating 3D scroll-driven landing pages.

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

---

## 🤖 Gemini CLI Skill (Automated Workflow)

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

### 3. View the Project
```bash
python3 tools/serve.py --name "my-project"
```
Access at: **http://localhost:8000**

---

## 🎨 Pre-generated Examples

The project includes two distinct architectural patterns for 3D scroll narratives:

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

Access both at: **http://localhost:8000**

## 📦 Integration
For instructions on how to copy these assets into an existing external project, see [docs/integration.md](docs/integration.md).

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
