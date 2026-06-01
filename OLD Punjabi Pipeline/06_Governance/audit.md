# 🕵️ Punjabi Guftar: Pipeline Audit & Optimization

**Date**: 2026-05-13
**Status**: Post-Test System Audit

---

## 🔄 Current Pipeline Mapping
1.  **Scripting**: Manual/Agent research -> Markdown Script (`test_02_alphabets.md`).
2.  **VO Generation**: Attempted `edge-tts` (Missing Punjabi) -> Shifted to manual/browser TTS.
3.  **Visuals**: Automated Thumbnail Generator (Python/Pillow) using Ancient Manuscript background.
4.  **Assembly**: FFmpeg scripts (`assemble_video.py`) handling image/audio stitching.
5.  **Distribution**: Automated YouTube Uploader (`upload_to_youtube.py`) via OAuth 2.0.

---

## 📉 Loopholes & Inefficiencies
*   **Metadata Language**: Titles and descriptions are currently defaulting to English or Mixed. Should be 100% Punjabi for channel authority.
*   **Thumbnail Permissions**: Channel needs phone verification to allow automated custom thumbnail uploads.
*   **Font Scarcity**: Only one Punjabi font (`nirmala.ttf`) is active. Limits the "Academic" aesthetic.
*   **Branding Manuality**: Logo and intros/outros are not yet part of the automated assembly script.

---

## 🍒 Low Hanging Fruits (Optimization)
1.  **Asset Centralization**: Create a `00_Standard_Assets` folder for Logo, Opener, and Closer.
2.  **Metadata Injection**: Update script to pull Punjabi Titles/Descriptions directly from the Markdown script's frontmatter.
3.  **Visual Watermarking**: Add a standard FFmpeg filter to overlay the Logo on the top-right corner of every video.
4.  **Version Control**: Initialize Git to track changes and prevent "hallucinated" asset loss.

---

## 🛠️ Scoped Implementation Plan
- [ ] **Task 1**: Initialize Git Repository.
- [ ] **Task 2**: Create `00_Standard_Assets` and structure sub-folders for `Logo`, `Intros`, and `Fonts`.
- [ ] **Task 3**: Update `assemble_video.py` to include `Opener -> Video + Logo -> Closer` logic.
- [ ] **Task 4**: Source 3-5 additional high-quality Gurmukhi fonts.
- [ ] **Task 5**: Refine `upload_to_youtube.py` for Punjabi metadata priority.
