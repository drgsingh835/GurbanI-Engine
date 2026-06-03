# Changelog

All notable changes to the **GurbanI Engine** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-06-04

### Added
* **No-Captions Compilation**: Added the `--no-captions` CLI parameter to `render_reel.py` to allow compiling videos without burning hard subtitles onto image shots.
* **Integrated Voiceover Compilation**: Passed `--no-captions` option during `recompile_voiceover.py` video assembly executions.

### Fixed
* **Windows Git Hook Launcher**: Modified the git pre-commit hook installer in `changelog_enforcer.py` to use the standard `py` launcher instead of `python` for correct execution on Windows systems.

## [1.0.0] - 2026-06-01

### Added
* **Monorepo Consolidation**: Consolidated individual projects (`gurbani-creative-pipeline`, `ai-labs-claude-skills-source`, `koda-stack-source`, and `OLD Punjabi Pipeline`) into a unified parent Git repository for simpler tracking and deployment.
* **Gurmukhi Typography Support**: Added legacy ASCII font mapping (`AmrLipiHeavy.ttf`) and native Unicode support (`Nirmala.ttc`) inside the video renderer and thumbnail generators.
* **Indic Parler-TTS Integration**: Hooked up Gradio-based speech synthesis API fallback using `ai4bharat/indic-parler-tts` on Hugging Face to generate authentic Punjabi voiceovers.
* **Timeline Sync Correction**: Introduced sidecar JSON duration tracking to programmatically scale and align visual timeline clips to exact generated audio lengths before video rendering.
* **YouTube Publishing Automations**: Added helper script (`youtube_uploader.py`) utilizing OAuth 2.0 flow to support automatic video uploads and thumbnail settings.
* **Local Replication Tooling**: Added `.env.example` templates and config folder instructions (`config/youtube/README.md`) to allow new users or AI agents to replicate the setup on their own channels instantly.

### Fixed
* **GitHub Push Protection Violations**: Excluded OAuth secrets (`client_secret.json` and `token.pickle`) from the repository history using updated root `.gitignore` patterns.
* **FFmpeg Image Decode Crashes**: Refactored the asset generator step to output valid black PNG images instead of plain text placeholders, preventing FFmpeg zoompan decode errors.
* **Path Escaping on Windows**: Escaped backslashes and drive letter colons in file paths to avoid rendering failures inside FFmpeg drawtext filters.

### Roadmap
* **Auto-Multiplier**: Create a publishing agent to automatically cut full-length reflections into shorter segments with optimized metadata for multi-platform distribution (TikTok/Instagram Reels).
* **Vocal Quality Upgrades**: Incorporate secondary voice filters to refine synthesized audio using studio equalization profiles.
