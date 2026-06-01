# Punjabi Guftar: Learning Log (Architectural Evolution)
## Lessons learned during the automation of academic Punjabi content.

---

### 📓 Lesson 1: The "Scale Disconnect" & Thematic Laziness
**Date**: 2026-05-14
**Project Context**: PG-SPEC ("ਮਰ ਰਹੀ ਹੈ ਮੇਰੀ ਭਾਸ਼ਾ")

**The Failure**:
1.  **Auditing**: I miscalculated the project length by 400% (assumed 7 mins, actually ~30 mins). This led to an "ETA" that was physically impossible.
2.  **Visual Over-Reliance**: I suggested a "patch-work" fix using a generic brand default (Gold-on-Charcoal) instead of analyzing the emotional and historical visual depth required for a film about language death.
3.  **Exploration Failure**: I reported the project as "Finalizing" despite dozens of white-frame gaps, because I only looked at the surface of the timeline.

**The Solution (The Pivot)**:
*   Transition to a **Decoupled Layer & Stitching Strategy** where I focus on assembling visuals provided or indexed by the user.
*   Implement a **Visual Style Header** in each script to anchor the project's DNA from the start.

**Future Action**:
*   Whenever a project is handed over, the first step is an **In-Depth Audit** regardless of the dashboard status.
*   Cross-reference source scripts with timeline duration BEFORE giving any ETA.

---

### 📓 Lesson 2: Aesthetic Consistency vs. Brand Defaults
**Date**: 2026-05-14
**Context**: Visual prompt generation for cinematic scenes.

**Insight**: "High-contrast gold" is a branding tool, not a cinematic narrative tool. For deep projects like PG-SPEC, the visuals must evolve with the script (e.g., vibrant to muted to dark).

**Future Action**: For every new project, we will define a **Visual Style Header** individually at the top of the script document. This header will provide guidance for the thematic, lighting, and core stylistic elements (for both AI scenes and programmatic flashcards), while specific scene movements will continue to follow the script's requirements.
