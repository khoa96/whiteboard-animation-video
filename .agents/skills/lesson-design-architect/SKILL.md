---
name: lesson-design-architect
description: Architects the deep instructional foundation and pedagogical design of an English language whiteboard lesson, establishing learning objectives, concept structure, misconceptions, sequence, examples/non-examples, and boundaries in an approval-ready Lesson Design Brief (LDB01).
---
# Lesson Design Architect — S02

## Mission

Bridge the gap between strategic video intent (Creative Brief) and structural script planning (Script Blueprint). S02 embodies the **Senior English Pedagogy Council (Hội đồng sư phạm tiếng Anh cao cấp)**. It establishes *how* knowledge is scientifically acquired, structured, contrasted, and verified, ensuring that downstream writers and visual artists never produce superficial explanations, pedagogically unsound examples, or uncalibrated teaching sequences.

## Why This Intermediate Artifact Is Indispensable

A Creative Brief specifies *what* to make and for whom; however, it lacks the detailed instructional architecture needed for scriptwriting. Without a Lesson Design Brief (LDB), scripts inevitably suffer from:
- Vagueness in rule definitions.
- Failure to address the root cognitive misunderstandings of learners.
- Weak or non-contrastive examples.
- Lack of formative checks.
- Scope creep where advanced exceptions disrupt fundamental understanding.

## Required Input Contract

To execute S02, the following must be verified:
1. `projects/<project_id>/01_creative_brief/CB01.json` with status `approved`.
2. Reference sources identified in `intake_report.json` (authoritative grammars, dictionaries, CEFR standards).

*Precondition Guard:* If `CB01` status is not `approved`, HALT immediately and report `ERROR: S02 requires an approved Creative Brief (Gate G01).`

## Core Information Architecture (10 Pedagogical Pillars)

The Lesson Design Brief MUST rigorously define the following 10 informational dimensions:

### 1. Learning Objectives (Mục tiêu học tập)
- Must be framed as measurable, observable "Can-Do" statements aligned with Bloom's Revised Taxonomy and CEFR guidelines.
- Format: *"By the end of this video, the learner will be able to: [Action Verb] + [Specific Task] + [Context/Standard]"*.
- Avoid unmeasurable phrases like "understand grammar" or "know about verbs".
- **Cognitive Load Cap:** Strict ceiling of maximum 1 Primary Learning Objective and at most 2 Supporting Micro-Objectives per 3-5 minute video. Videos exceeding 3 LOs must be flagged for curriculum splitting.

### 2. Knowledge Scope (Kiến thức bắt buộc phải dạy)
- The exact grammatical rules, phonological features, or lexical sets that constitute the core syllabus of this lesson.
- Explicit definition of core terms (e.g., mass noun vs count noun; aspect vs tense).

### 3. Prerequisite Knowledge (Kiến thức tiên quyết)
- Foundational concepts the learner must already possess (e.g., recognizing nouns and verbs, basic singular/plural concepts).
- Explicit diagnostics for what to do if a prerequisite is shaky (brief 5-second anchor vs assume known).

### 4. Concept Structure (Cấu trúc khái niệm & Bản đồ quan hệ)
- The relational anatomy of concepts (hierarchical, taxonomy, contrastive matrix, or sequential process).
- How the central target concept branches into sub-rules or operational criteria.

### 5. Common Misconceptions (Hiểu lầm phổ biến & L1 Interference)
- Identify 2 to 4 documented errors typical of the target learner profile (specifically analyzing Vietnamese L1 interference where applicable, such as zero-marking for plurals, absence of articles, or rigid translation).
- The root cause of each misconception and the antidote strategy.

### 6. Teaching Sequence (Trình tự giải thích sư phạm)
- Pedagogical progression designed to manage Cognitive Load (Sweller's CLT):
  * Step 1: Cognitive Hook / Problem Activation (Notice the gap).
  * Step 2: Concrete Demonstration / Contextualized Encounter.
  * Step 3: Rule Deconstruction / Visual Mechanism Isolation.
  * Step 4: Guided Comparison / Formative Practice.
  * Step 5: Consolidation & Mental Anchor Rule.

### 7. Examples & Non-examples (Ví dụ chuẩn & Ví dụ đối lập)
- High-potency examples illustrating the regular application.
- Crucial **Non-examples (Counter-examples / Minimal Pairs)** that delineate the boundary of the rule (e.g., *"a chair"* [Valid Countable] vs. *"a furniture"* [Invalid Uncountable Counter-example]).
- Contextual integrity: Examples must use authentic, high-frequency, natural English vocabulary calibrated to the learner's CEFR level.

### 8. Teaching Strategy (Chiến lược sư phạm)
- Selection and justification of didactic techniques:
  * Visual Analogy (e.g., counting individual blocks vs pouring liquid).
  * Direct Contrasting (Side-by-side comparative table).
  * The "Test/Heuristic Method" (e.g., Can you put a number '2' in front of it? Can you add -s?).
  * Concrete-Representational-Abstract (CRA) instructional flow.

### 9. Knowledge Check (Kiểm tra nhận thức / Formative Assessment)
- 1 to 2 micro-assessment moments embedded before the conclusion.
- Formative challenge format (e.g., *"Spot the error in 3 seconds"*, *"Choose A or B"*).
- Pedagogical rationale for how the answer is revealed and reinforced with positive feedback.

### 10. Content Boundaries (Ranh giới nội dung bất biến)
- Hard pedagogical guardrails: Specific exceptions, advanced edge cases, or peripheral nuances that are STRICTLY FORBIDDEN in this lesson to protect learner clarity.

## Step-by-Step Execution Protocol

1. **Intake & Curricular Alignment:** Extract audience CEFR level, primary purpose, and constraints from `CB01.json`.
2. **Grammar & Linguistics Verification:** Cross-reference authoritative English reference materials to confirm linguistic precision (e.g., Cambridge Grammar of the English Language, Swan's Practical English Usage).
3. **Misconception & L1 Mapping:** Analyze typical Vietnamese EFL learner stumbling blocks for the target topic.
4. **Draft Canonical JSON (`LDB01.json`):** Construct the structured lesson design object.
5. **Generate Human-Readable Review Copy (`LDB01.md`):** Render clear, beautifully structured markdown with analytical commentary and callout boxes.
6. **Internal Adversarial Audit:** Execute 3-lens review:
   - *Applied Linguist Lens:* Are grammar definitions pristine and free from oversimplifications that lead to fossilized errors?
   - *ELT Pedagogy Lens:* Are the non-examples clear? Is cognitive load properly stepped?
   - *Whiteboard Visualizer Lens:* Are the concept structure and analogies easily translatable to 2D whiteboard drawings?

## Output Artifact Schema (`LDB01.json`)

```json
{
  "schema_version": "1.0.0",
  "project_id": "WB-xxxx",
  "artifact_id": "LDB01",
  "version": "1.0",
  "source_cb_version": "1.0",
  "status": "in_review",
  "learning_objectives": [
    {
      "lo_id": "LO_01",
      "statement": "string (measurable can-do)",
      "bloom_level": "Understand | Apply | Analyze",
      "cefr_level": "A2"
    }
  ],
  "knowledge_scope": {
    "core_concepts": ["string"],
    "target_linguistic_structures": ["string"],
    "key_terminology": [
      {"term": "string", "definition_for_learner": "string"}
    ]
  },
  "prerequisite_knowledge": [
    {"concept": "string", "remediation_if_missing": "string"}
  ],
  "concept_structure": {
    "relationship_type": "HIERARCHICAL | CONTRASTIVE_PAIR | SEQUENTIAL_PIPELINE",
    "nodes": [{"node_id": "string", "concept_name": "string", "parent_id": "string | null"}],
    "explanation": "string"
  },
  "common_misconceptions": [
    {
      "misconception_id": "MISC_01",
      "erroneous_belief": "string",
      "l1_interference_factor": "string",
      "pedagogical_antidote": "string"
    }
  ],
  "teaching_sequence": [
    {
      "stage_order": 1,
      "stage_name": "HOOK_AND_DISCOVERY | DECONSTRUCTION | CONTRAST | PRACTICE | ANCHOR",
      "instructional_focus": "string",
      "pedagogical_intent": "string"
    }
  ],
  "examples_and_non_examples": [
    {
      "concept_ref": "string",
      "positive_examples": ["string"],
      "negative_counter_examples": ["string"],
      "boundary_distinction_note": "string"
    }
  ],
  "teaching_strategy": {
    "primary_method": "string",
    "visual_analogies": ["string"],
    "decision_rules_for_learner": ["string"]
  },
  "knowledge_check": {
    "assessment_type": "BINARY_CHOICE | ERROR_HUNT | FILL_BLANK",
    "sample_questions": [
      {
        "prompt": "string",
        "options": ["string"],
        "correct_answer": "string",
        "feedback_explanation": "string"
      }
    ]
  },
  "content_boundaries": {
    "forbidden_extensions": ["string"],
    "deferred_to_future_lessons": ["string"]
  },
  "approval_gate": {
    "gate_id": "G02",
    "state": "PENDING_USER_APPROVAL"
  }
}
```

## Mandatory Approval Gate G02

- Present `LDB01.md` highlighting the 10 pedagogical pillars.
- Request user evaluation and sign-off.
- **HARD STOP:** Script Blueprint (S03) MUST NOT begin until Gate G02 is formally approved.
