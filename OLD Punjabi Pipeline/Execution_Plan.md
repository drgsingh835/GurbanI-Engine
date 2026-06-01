# Execution Plan: Punjabi Guftar YT Workflow

This plan defines the end-to-end process for creating high-fidelity "Academic Punjabi" content for the **Punjabi Guftar** YouTube channel.

## 🏗️ Workspace Architecture (F:\Punjabi_Guftar_Workspace)
- **01_Scripts_and_Research**: Linguistic etymology, Gurmukhi scripts.
- **02_Visual_Assets**: AI-generated calligraphy, thumbnail blueprints, B-roll.
- **03_Audio_Laboratory**: Voiceover recordings and background soundscapes.
- **04_Video_Production**: FFmpeg scripts, rough cuts, and visual overlays.
- **05_Final_Deliverables**: Master files ready for upload.
- **06_Governance**: SEO templates, Style Guide, and Project Logs.

---

## 🔄 Phase 1: Linguistic Research & Scripting (Tier 1)
**Goal**: Establish scholarly authority through precise etymology.
1.  **Etymology Deep-Dive**: Agent researches Persian/Arabic/Sanskrit roots using digital archives.
2.  **Script Drafting**: Draft content in **Gurmukhi** to maintain linguistic precision and cultural focus.
3.  **Tone Check**: Ensure a "High-Register" vocabulary (avoiding casual slang, favoring poetic and formal terms).

## 🎨 Phase 2: Visual & SEO Packaging (Tier 2)
**Goal**: Create premium, "Dark Mode" aesthetic visuals.
1.  **Thumbnail Design**: Generate minimalist, high-contrast thumbnail concepts (e.g., gold calligraphy on charcoal).
2.  **Metadata Mastery**: Generate SEO-optimized titles and descriptions using the channel's "Prestige" keywords.
3.  **Visual Strategy**: Use a **Decoupled Layer Strategy**. Programmatically generate 16:9 horizontal Flashcards using Python/Pillow on reusable premium backgrounds to avoid AI text hallucinations.

## 🎬 Phase 3: Production & Editing (Tier 3)
**Goal**: Efficient, semi-automated assembly.
1.  **Voiceover (Browser Sub-Agent)**: Use automated browser scripts to generate high-quality audio from online free-tier platforms.
2.  **Video Assembly Automation**: Use FFmpeg/Python scripts to:
    *   Sync visual **Flashcards** (Gurmukhi) with audio timestamps.
    *   Burn actual text using `.ttf` fonts over clean, horizontal backgrounds.
    *   Apply Ken Burns zoom effects and background soundscapes.
3.  **Quality Audit**: Final review for linguistic accuracy and audio-visual sync.

## 🚀 Phase 4: Distribution & Engagement
**Goal**: Reach the academic and linguistic enthusiast audience.
1.  **Upload & Chaptering**: Upload to YouTube with auto-generated chapters based on the script.
2.  **Community Hook**: Draft a scholarly community post or poll to drive engagement.
3.  **Archive**: Move all project files to `05_Final_Deliverables` and update the `06_Governance` log.

---

## 🎨 Phase 5: Aesthetic Thumbnail Generation (Native Identity)
**Goal**: Create high-click-through-rate (CTR) thumbnails with "Academic Punjabi" branding.
1.  **Aesthetic Core**: Use the **Gold-on-Charcoal** palette.
2.  **Visual Elements**: 
    *   **Background**: High-texture dark charcoal or ancient parchment.
    *   **Calligraphy**: Large, glowing Gurmukhi text generated via Python/Pillow or AI.
    *   **Branding**: Subtle "Punjabi Guftar" seal in the corner.
3.  **Process**:
    *   Generate base thematic image (AI).
    *   Overlay standardized Gurmukhi title using local premium fonts.
    *   Apply cinematic color grading (high contrast).

## 🚀 Phase 6: Automated Distribution (YouTube Loop)
**Goal**: 100% automated upload and optimization.
1.  **API Integration**: Use YouTube Data API v3 for uploading.
2.  **Metadata Injection**: 
    *   Pull title, description, and tags from `06_Distribution_and_Growth\01_Metadata_Vault`.
    *   Set privacy status (Private -> Review -> Public).
3.  **Algorithm Optimization**: 
    *   Schedule uploads during peak Punjabi-speaking audience hours.
    *   Auto-generate community posts to link to new videos.

---

## 🛠️ Immediate Next Steps
1. [x] Initialize `06_Governance\style_guide.md`.
2. [x] Implement programmatic 16:9 Flashcard Generator.
3. [x] Customize Production Dashboard for "Medium of Exchange" status.
4. [x] Design Brand-Identity Thumbnail Template (Python/Pillow).
5. [x] Populate `06_Governance\credentials.env` with YouTube API Keys.
6. [x] Execute first "Full-Loop" production for `PG-002: ਪੈਂਤੀ ਅੱਖਰ ਦਾ ਵਿਗਿਆਨ`.
7. [x] Implement Animated Flashcards & Branding (Logo/Intro) Integration.
8. [ ] **[CURRENT]** Final Review of PG-002 Master Export and YouTube Upload Verification.
9. [ ] **[NEW]** Test Google Vids Workflow for cinematic scenes (PG-003 prototype).
10. [x] Research & Draft Script for PG-003: ਮਰ ਰਹੀ ਹੈ ਮੇਰੀ ਭਾਸ਼ਾ (The Death of a Language).
11. [x] Generate PG-003 Flashcards (23-Card sequence for Language Death analysis).
12. [ ] **[CURRENT]** Generate PG-003 Voiceover and Audio-Visual Sync (Modular).
