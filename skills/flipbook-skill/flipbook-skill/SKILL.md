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
python3 pipeline/sync.py --name "project-name" --prompt "Your 8-bit ANSI prompt"
```

### 2. Step-by-Step Refinement
You can refine individual components without regenerating the entire project:
- **`--step start`**: Regenerate the beginning anchor frame.
- **`--step end`**: Regenerate the ending anchor frame.
- **`--step video`**: Morph the anchor frames into a transition video.
- **`--step web`**: Package the video frames into an optimized WebP website.

## Directory Structure
- **`projects/{name}/source/`**: Raw anchor frames and transition video.
- **`projects/{name}/www/`**: Final vanilla HTML/JS website.
- **`blueprint/`**: The master template for all new sites.

## Setup Requirements
Ensure `.env` at the root contains:
- `GEMINI_API_KEY`: For Nano Banana 2 and Veo 3.1.
- `GCP_PROJECT_ID`: For Vertex AI services.

## Performance Standards
- **Format**: All web frames are automatically converted to **WebP**.
- **Renderer**: Uses `flipbook.js` (Canvas + requestAnimationFrame).
- **Aspect Ratio**: Defaults to **16:9** for a cinematic experience.
