# 🛠️ Punjabi Guftar: Production Loop & System Status

We are pausing all work on PG-003 to perfect the **PG-002 (First Test Video)**. This document outlines our current automation status and the roadmap for recalibrating flashcards and thumbnails.

## 🏗️ Production Flow Chart (Automation vs. Manual)

![Production Loop Flowchart](file:///f:/Punjabi_Guftar_Workspace/06_Governance/Production_Loop_Flowchart.png)

```mermaid
graph TD
    subgraph "Phase 1: Research & Scripting"
        A[Manual: Idea & Research] --> B[Automated: Script Drafting]
        B --> C{User Approval}
    end

    subgraph "Phase 2: Asset Preparation"
        C -- Approved --> D[Automated: VO Generation]
        D --> E[Option A: Python/Pillow Flashcards]
        D --> E2[Option B: Google Vids AI Scenes]
        E --> F[Standard Assets]
        E2 --> F
    end

    subgraph "Phase 3: Assembly & Polish"
        F --> G[Manual/Audit: Spelling Check]
        G --> H[Automated: Text Animation & Sync]
        H --> I[Automated: Final Rendering]
    end

    subgraph "Phase 4: Distribution"
        I --> J[Automated: YouTube Upload]
        J --> K[Automated: Custom Thumbnail Set]
    end

    style C fill:#f9f,stroke:#333,stroke-width:2px
    style G fill:#f9f,stroke:#333,stroke-width:2px
```

### 📊 Automation Audit
| Stage | Status | Tool | Intervention Required |
| :--- | :--- | :--- | :--- |
| **Scripting** | 🤖 80% | GPT-4o / Gemini | Research validation & Tone check |
| **Voiceover** | 🤖 100% | Edge-TTS | None (unless quality needs change) |
| **Flashcards** | 🤖 60% | Python/Pillow | **Spelling Audit** & **Animation Sync** |
| **Thumbnail** | 🤖 90% | Python/API | Phone verification (DONE) |
| **Assembly** | 🤖 40% | FFmpeg | Timing sync with VO chunks |

---

## 📜 Git Status (Workspace Integrity)

The repository is currently tracking the core logic. Your newly added assets (Intro/Logo) are currently **Untracked**.

- **Last Commit**: `4beb2c7` - Initial commit: Pipeline established.
- **Current Branch**: `master`
- **Pending Actions**:
    - [ ] Stage and commit standard assets (Intro/Logo/Fonts).
    - [ ] Stage and commit automation script updates.

---

## 🎯 Immediate Recalibration Goals (PG-002)

1.  **Spelling Audit**: I will compare `test_02_alphabets.md` with the existing flashcards to catch discrepancies.
2.  **Text Animation**: I will modify the assembly script to use FFmpeg's `drawtext` for per-character or per-word appearing effects (synchronized with VO timestamps).
3.  **Thumbnail Test**: I will run a dedicated test to set a custom thumbnail for the PG-002 upload to verify the phone activation.

---
