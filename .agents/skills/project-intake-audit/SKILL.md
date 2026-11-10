---
name: project-intake-audit
description: Audits project source materials, detects missing prerequisites, resolves source conflicts, establishes version baselines, and generates the authoritative Project Intake Manifest before pre-production begins.
---
# Project Intake & Source Audit — S00

## Mission

Serve as the first-line quality and governance gate for any Whiteboard Animation educational video project. Inspect all supplied materials, verify source authorities, resolve conflicting instructions, identify missing information, and establish immutable version baselines. 

This Skill ensures downstream pedagogical and production agents never work with ambiguous, conflicting, incomplete, or obsolete documents.

## Operational Context & Boundaries

- **Role in Pipeline:** Gate 0 (G00). Precedes S01 (Creative Brief Builder).
- **Primary Responsibility:** Source audit, dependency tracking, conflict detection, cold-start handling, and manifest creation.
- **Out of Scope:** This Skill does NOT invent missing lesson content, draft briefs, design lessons, write scripts, or generate image prompts.

## Required Input Contract

The agent executing this Skill must inspect the project workspace and any supplied user inputs:
1. `projects/<project_id>/00_sources/` or root intake directory containing raw reference files (textbooks, grammar notes, guidelines, existing scripts, or curriculum files).
2. Workspace style references: `whiteboard_master_prompt_scene_generator_v2.1.md` and `whiteboard_visual_style_bible_v1.0_accepted.md`.
3. Voice / Audio profiles: `VOICES.md` or `config/tts_voices.json` if available.
4. User request prompt specifying working topic, goals, or constraints (even if only a single prompt sentence).

## Cold-Start & Edge Case Handling Protocol

1. **Cold-Start Mode (Zero External Files):**
   - If the user provides only an initial prompt (e.g., "Create a lesson explaining Present Perfect vs. Past Simple") with no attached files, S00 does NOT fail.
   - S00 flags `INTAKE_MODE: COLD_START`, creates a baseline intake manifest with `SRC_00_USER_PROMPT`, locks the workspace production standards (Master Prompt v2.1, Style Bible v1.0), and marks pedagogical references as `ELICITATION_REQUIRED_IN_S01`.
2. **Corrupted or Unreadable Files:**
   - Detect encoding errors, unreadable formats, or empty files. Flag `CORRUPTED_SOURCE_FLAG`, quarantine the file, and notify the user with file name and required replacement.
3. **Outdated Standards Detection:**
   - Explicitly verify whether legacy prompts (v1.0) or outdated scripts are referenced. If detected, quarantine legacy instructions and enforce Master Prompt v2.1.

## Step-by-Step Audit Protocol

### Step 1: Inventory & Hashing
1. Scan all provided files in the workspace intake directory.
2. Record for each file:
   - File path, size, and last modified date.
   - Content hash or version identifier.
   - Classification: `PEDAGOGICAL_SOURCE`, `PRODUCTION_STANDARD`, `VOICE_SPECIFICATION`, `USER_INSTRUCTION`, `LEGACY_ARTIFACT`.
   - Pedagogical CEFR tag: Check if reference material defines a target CEFR level (A1, A2, B1, B2, C1, C2) or Cambridge/IELTS benchmark.

### Step 2: Source Authority & Precedence Resolution
Establish the precedence hierarchy:
1. **Tier 1 (Explicit User Invariants):** Specific, unambiguous instructions provided in the current session.
2. **Tier 2 (Accepted Workspace Standards):** `whiteboard_production_invariants.md`, `whiteboard_visual_style_bible_v1.0_accepted.md`, `whiteboard_master_prompt_scene_generator_v2.1.md`.
3. **Tier 3 (Authoritative Knowledge Domain Source):** Cambridge/Oxford English grammar references, official curriculum guidelines supplied in `00_sources/`.
4. **Tier 4 (Derived / Draft Artifacts):** Legacy briefs, previous script versions, draft notes.

*Conflict Detection Rule:* If a Tier 4 document contradicts a Tier 2 standard (e.g. legacy script asks for text-free background with post-overlay, while Master Prompt v2.1 requires all typography in single static canvas), flag a `CRITICAL_SOURCE_CONFLICT` and enforce Tier 2 precedence, logging the override.

### Step 3: Completeness & Gap Analysis
Verify the existence of mandatory foundations:
- Is the English grammatical or lexical topic clearly identifiable?
- Is there an authoritative rule reference (e.g., standard definitions, examples, boundary rules)?
- Are visual style and canvas standards pinned?
- Are target delivery constraints indicated (or flagged as needing S01 interview)?

### Step 4: Red-Team Pre-Intake Critique
Before producing the final intake report, evaluate against 4 failure modes:
1. *Ghost Document Risk:* Are there references to unsupplied files?
2. *Pedagogical Drift Risk:* Does the user request ask to teach a rule that is linguistically inaccurate or oversimplified without nuance?
3. *Obsolete Standard Risk:* Is an outdated Master Prompt (v1.0) cited instead of v2.1?
4. *Cadence/Voice Feasibility Risk:* Is the requested video duration realistic for the scope of the topic?

## Output Artifacts & Data Schema

The Skill must generate dual-format artifacts under `projects/<project_id>/00_intake/`:

1. `intake_report.json` (Canonical Machine-Readable Record):
```json
{
  "schema_version": "1.0.0",
  "project_id": "WB-xxxx",
  "intake_mode": "COLD_START | HYBRID | FULL_ASSET",
  "audit_timestamp": "ISO-8601",
  "auditor_role": "S00-project-intake-audit",
  "overall_status": "PASS | CONDITIONAL_PASS | BLOCKED",
  "source_inventory": [
    {
      "source_id": "SRC_01",
      "file_path": "path/to/file",
      "source_type": "PEDAGOGICAL_SOURCE",
      "version_tag": "v1.0",
      "authority_tier": 3,
      "cefr_alignment": "B1 | UNKNOWN",
      "integrity_status": "VALID"
    }
  ],
  "precedence_rules_applied": [],
  "conflicts_detected": [
    {
      "conflict_id": "CONF_01",
      "severity": "CRITICAL | MAJOR | MINOR",
      "conflicting_sources": ["SRC_01", "SRC_02"],
      "description": "string",
      "recommended_resolution": "string",
      "status": "OPEN | RESOLVED"
    }
  ],
  "missing_prerequisites": [],
  "downstream_readiness": {
    "ready_for_s01": true,
    "blocking_issues_count": 0
  }
}
```

2. `INTAKE_REPORT.md` (Human Review Document):
Rendered summary including:
- Executive Summary of Assets & Intake Mode.
- Authority Hierarchy Matrix.
- Identified Conflicts & Proposed Resolutions.
- Ready-for-S01 Checklist.

## Quality Gate G00 Criteria

A project passes Gate G00 if and only if:
- `blocking_issues_count == 0`.
- All conflicting sources have documented resolutions.
- Visual standards are locked (Master Prompt v2.1 & Style Bible v1.0).
- Authoritative pedagogical source is identified or flagged for adaptive elicitation in S01.

If `blocking_issues_count > 0`, the Skill halts execution, marks status `BLOCKED`, and outputs the exact questions required from the user.
