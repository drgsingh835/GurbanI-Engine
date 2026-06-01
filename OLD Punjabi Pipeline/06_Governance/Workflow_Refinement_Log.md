# Workflow Refinement Log: The Production Loop

This document tracks the evolution of the Punjabi Guftar automated production pipeline, moving towards 100% in-house automation.

## 🎯 The Target Workflow (Skeleton)
1. **Scripting (Tier 1)**: Agent creates scripts with specific **Visual Prompts** &rarr; Notifies User.
2. **Human Review**: User reviews/edits Markdown scripts and provides **Browser Credentials** in `.env`.
3. **Voiceover (Tier 2)**: Agent uses **Browser Sub-Agent** to generate/download audio from premium online TTS (ElevenLabs, etc.) while tracking free credits.
4. **Visuals & Assembly (Tier 3)**: Agent generates **Programmatic Flashcards** (16:9) and stitches them with audio via local FFmpeg using the **Decoupled Layer Strategy**.
5. **Quality Check**: User reviews the final horizontal video and suggests changes.
6. **Publishing**: Once approved, Agent uploads and publishes to YouTube.

---

## 🔄 Current Pipeline Progress

### 1. Scripting (Tier 1)
- **Current State**: Agent drafts the script in Markdown, translating English concepts into high-register Gurmukhi Punjabi. 
- **Refinement Needed**: Automate the extraction of the spoken text directly from the Markdown file.

### 2. Audio/Voiceover (Tier 2)
- **Current State**: Utilizing **"Browser Sub-Agent Automation"**. User provides web credentials in `.env`, and my internal headless browser agent physically logs in, inputs the text, downloads the audio, and tracks remaining free credits across a pool of accounts.
- **Refinement Needed**: Execute the first Browser Sub-Agent run for `test_02_alphabets.md` once credentials are provided. Develop a credit tracking log to monitor free-tier exhaustion.

### 3. Visual Assets & Assembly (Tier 3)
- **Current State**: Visual Directive Mapping fails because AI image generators hallucinate Gurmukhi text (outputting religious iconography instead of alphabets) and generating unique images per scene exhausts API credits.
- **Refinement Needed**: Implement a **"Decoupled Layer Strategy"**. 
  - **Base Layer**: Maintain a local library of reusable, premium abstract backgrounds (parchment, dark academia). Zero credit cost per video.
  - **Text/Context Layer**: Use Python (Pillow) or FFmpeg to dynamically burn *actual* Gurmukhi text (using .ttf fonts) over the background. 
  - **Result**: The script generator only needs to command *which* text to display over *which* reusable background, completely eliminating AI image hallucinations and saving 100% of image generation credits.

### 4. Distribution & SEO (Tier 4)
- **Current State**: Agent generates the SEO Metadata template.
- **Refinement Needed**: Build the YouTube automation script.

---
## 📝 Change Log
- **[2026-05-12]**:
    - Installed Python 3.11 and FFmpeg locally on F: Drive.
    - Switched to **Decoupled Layer Strategy** for visuals (Python-generated 16:9 Flashcards + .ttf fonts) to avoid AI hallucinations and credit burn.
    - Adopted **Browser Sub-Agent** strategy for VO to leverage free-tier credits across multiple platforms (ElevenLabs/NotebookLM) via a local `credentials.env` vault.
    - Successfully generated first 16:9 Flashcard set for `test_02_alphabets.md`.
- **[2026-05-14]**:
    - **Sync Correction**: Identified a ~2-second drift where visuals were "running behind" speech.
    - **Resolution**: Analyzed `PG002_MX_VO.mp3` files using `ffmpeg silencedetect` to find precise semantic transition points.
    - **Update**: Refined `Video_Stitcher.py` with specific durations (e.g., Mukh Varg reduced from 1.8s to 1.44s per letter).
    - **Future-Proofing**: Added `SYNC_OFFSET` to `Video_Stitcher.py` for global calibration.

## 📌 Next Session Starting Point
1. **VO Integration**: Confirm `PG002_M1_VO.mp3`, `M2`, and `M3` are in the `01_Raw_VO` folder.
2. **Movement 1 Assembly**: Trigger the stitching script for the first 1-minute segment using the new Visual IDs.
3. **Template Scaling**: Apply the "Visual Style Header" to the draft of PG-003.

---

## 📓 Learning Archives
- [Learning Log](file:///f:/Punjabi_Guftar_Workspace/06_Governance/Learning_Log.md): Lessons on Scale Disconnect and Semantic Partitioning.
- [Visual Style Header](file:///f:/Punjabi_Guftar_Workspace/01_Scripts_and_Research/test_02_alphabets.md): The new standard for project-specific visual DNA.
