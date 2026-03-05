---
name: flipbook-skill
description: Generates modular 3D scroll experiences using Nano Banana 2 and Veo 3.1. Supports step-based generation of start/end frames, transition videos, and high-performance WebP flipbook components.
---

# Flipbook Generation Pipeline

## Overview
This skill provides a modular, project-based workflow for creating high-performance 3D scroll "flipbook" websites. It coordinates Google's Nano Banana 2 (for 8-bit ANSI images) and Veo 3.1 (for smooth transition morphs).

## Modular Workflow

### 1. Full Pipeline Run
Generate everything for a new project in one command.
```bash
python3 pipeline/sync.py --name "project-name" --prompt "Your prompt" --background-color "black" --quality "fast"
```

### 3. Direct Video Input
Skip generation and create a flipbook from an existing MP4.
```bash
python3 pipeline/sync.py --name "my-project" --video-input "/path/to/video.mp4"
```

### 4. Step-by-Step Refinement
You can refine individual components without regenerating the entire project:
- **`--video-input`**: Path to an existing MP4 to use as the source.
- **`--quality`**: Choose between 'fast' (budget-friendly) or 'premium' (high-fidelity final render). Defaults to 'fast'.
- **`--step start`**: Regenerate the beginning anchor frame.
- **`--step end`**: Regenerate the ending anchor frame.
- **`--step video`**: Morph the anchor frames into a transition video.
- **`--step web`**: Package the video frames into an optimized WebP website.

## 📁 Skill Assets & Scripts
- **`scripts/sync.py`**: The core orchestrator for the entire generation process.
- **`scripts/generate_image.py`**: Direct interface to Nano Banana 2.
- **`scripts/generate_video.py`**: Direct interface to Veo 3.1.
- **`scripts/convert_to_webp.py`**: High-performance frame optimizer.
- **`scripts/serve.py`**: Local preview server.
- **`assets/blueprint/`**: The master vanilla HTML/CSS/JS template for all new sites.

## Workspace Awareness
All projects are generated and stored in the **`projects/`** directory of the user's workspace, regardless of where the extension is installed. This ensures persistence and easy access.

## Preview & Review
Once a project is built, the user can instantly preview it using the **`preview_item`** MCP tool.
- For local projects: `preview_item(name="my-project")`
- For built-in examples: `preview_item(name="example-0", is_example=True)`

## Setup Requirements
Ensure `.env` at the root contains:
- `GEMINI_API_KEY`: For Nano Banana 2 and Veo 3.1.
- `GCP_PROJECT_ID`: For Vertex AI services.

## Performance & Quality Standards
- **Temporal Coherence**: Automatically extracts frames from video generation for butter-smooth motion without first-frame stutter.
- **Pixel-Perfect Rendering**: Uses Flipbook.js 2.3+ with hardware-accelerated CSS centering (`object-fit: cover`).
- **WebP Optimization**: Automatically converts all frames to optimized WebP for ultra-fast loading.
- **Pinned Hero Layout**: New blueprint ensures the 3D animation stays sticky as a full-screen background by default.
