# GurbanI Engine

Welcome to the **GurbanI Engine** monorepo. This codebase hosts active tools, pipeline automations, and assets to generate, render, and publish high-quality media content (such as YouTube shorts/reels) with Gurmukhi typography and voiceovers.

---

## Repository Structure

The monorepo contains the following primary directories:

* **[gurbani-creative-pipeline](file:///f:/GurbanI%20Engine/gurbani-creative-pipeline/)**: The active project orchestration codebase. Contains LLM-based agent definitions, Python runner scripts, audio assets, and render configurations.
* **[koda-stack-source](file:///f:/GurbanI%20Engine/koda-stack-source/)**: Core skills definitions and prompts for Concept, Storyboard, Assemble, and Publish steps.
* **[ai-labs-claude-skills-source](file:///f:/GurbanI%20Engine/ai-labs-claude-skills-source/)**: Reusable packages and code skills for researching, optimizing SEO, and managing assets.
* **[OLD Punjabi Pipeline](file:///f:/GurbanI%20Engine/OLD%20Punjabi%20Pipeline/)**: Historical automation scripts, templates, and video assets.

---

## Setup & Prerequisites

### 1. External Dependencies
This engine uses **FFmpeg** and **ffprobe** to programmatically measure audio durations, trim silence, mix voiceovers with background music, and compile video clips.
* **FFmpeg**: Must be installed on your system and added to your system's PATH. 
  * *Windows (PowerShell)*: Install via winget: `winget install Gyan.FFmpeg` or chocolatey: `choco install ffmpeg`.
  * *Mac/Linux*: Install via brew/apt: `brew install ffmpeg` or `sudo apt install ffmpeg`.

### 2. Python Environment
Navigate to the active pipeline directory and install dependencies:
```bash
cd gurbani-creative-pipeline
pip install -r requirements.txt
```

### 3. Local Configuration & Secrets
Copy the environment template and set up your Hugging Face API token (required for Indic Parler-TTS speech synthesis models):
```bash
cp .env.example .env
```
Open `.env` and configure:
* `HF_TOKEN`: Your Hugging Face user access token.
* `GEMINI_API_KEY`: Your Google Gemini API Key (needed for AI Scriptwriter, Art Director, and Storyboard agents).

### 4. YouTube API Integration (Optional)
If you wish to auto-publish rendered videos directly to YouTube:
1. Obtain an OAuth 2.0 Desktop Application JSON credentials file from the Google Cloud Console.
2. Follow the detailed steps in [gurbani-creative-pipeline/config/youtube/README.md](file:///f:/GurbanI%20Engine/gurbani-creative-pipeline/config/youtube/README.md) to place your `client_secret.json` and generate the authorized `token.pickle` file.

---

## How to Run

The pipeline runs step-by-step or in full sequence using `pipeline_runner.py` inside `gurbani-creative-pipeline`:

* **View Available Steps**:
  ```bash
  python pipeline_runner.py help
  ```
* **Run a Specific Step** (e.g., Step 1: Scriptwriting):
  ```bash
  python pipeline_runner.py 1 --id gurbani_01
  ```
* **Run the Entire Pipeline** (Generates scripts, storyboards, voiceovers, overlays, compiles video, and generates a thumbnail):
  ```bash
  python pipeline_runner.py all --id gurbani_01 --thumbnail
  ```
* **Run the Pipeline & Upload to YouTube**:
  ```bash
  python pipeline_runner.py all --id gurbani_01 --thumbnail --upload --privacy unlisted
  ```
