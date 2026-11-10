---
name: narration-script-writer
description: Crafts the complete, polished spoken narration script locked to Beat IDs from the approved Beat Plan, conducting phonetic/cadence audits and producing clean TTS-ready narration exports (NS01).
---
# Narration Script Writer — S05A

## Mission

Transform the atomic narration intents established in the approved Narration–Visual Beat Plan (`BPL01`) into a pristine, natural, pedagogically effective spoken narration script. S05A acts as the **Master English Scriptwriter & Phonetics/Cadence Specialist**.

S05A ensures that every sentence sounds effortless, engaging, and conversational while strictly respecting the Beat IDs, time budgets, and pedagogical terminology approved in upstream briefs.

## Operational Context & Pipeline Independence

- **Branch Position:** Branch 05A (runs in parallel or synchrony with 05B).
- **Governing Contract:** `BPL01` (approved, Gate G04). S05A is bound to the Beat IDs defined in BPL01. It CANNOT add new beats, delete beats, or change the pedagogical intent of any beat.
- **Subsequent Dependency:** Approved Narration Script provides exact narration cue spans to finalize S05B (Scene Matrix) and feeds the TTS voiceover engine.

## Required Input Contract

1. `projects/<project_id>/04_beat_plan/BPL01.json` (status `approved`, Gate G04).
2. `projects/<project_id>/02_lesson_design/LDB01.json` (approved) — Source for accurate examples, terminology, and pronunciation notes.
3. `projects/<project_id>/01_creative_brief/CB01.json` (approved) — Voice persona, target tone, and audience level.

*Precondition Guard:* If `BPL01` is not `approved`, HALT. Never draft script without an approved Beat Plan.

## Voice & Cadence Engineering Standards

### 1. Conversational ELT Tone
- Write for the ear, not the eye. Use short, crisp sentences, active voice, and conversational contractions (*it's*, *you'll*, *don't*), unless the lesson specifically teaches formal writing.
- Pacing calibrated for ESL/EFL comprehension: 130–150 words per minute (WPM).
- Avoid complex subordinate clauses that force listeners to hold too much syntax in working memory.

### 2. Beat ID Alignment & Cue Markers
- Every spoken block must be explicitly tagged with its `beat_id` (e.g., `B01.01`).
- Inside each beat, embed speech pause cues where natural pauses are required for visual processing:
  * `[pause=300ms]`: Minor clause separation.
  * `[pause=600ms]`: Emphatic pause or waiting for visual reveal.
  * `[pause=1000ms]`: Formative question pause (allowing the learner to think before the answer is shown).

### 3. Pronunciation & Phonetic Guidance
- For English grammar/phonetic lessons, include explicit pronunciation cues or IPA respelling in brackets for TTS engine clarity where ambiguous (e.g., *read* [reed] vs. *read* [red]; *record* [noun: REK-ord] vs. *record* [verb: ri-KORD]).

### 4. Cadence & Syllable Audit
For each beat, compute:
- Word count ($W$) and syllable count ($S$).
- Estimated spoken duration: $T_{\text{est}} = \frac{W}{\text{Target WPM}} \times 60 + \text{Pauses}$.
- Compare $T_{\text{est}}$ against `BPL01.estimated_duration_seconds`.
- *Cadence Alert:* If $|T_{\text{est}} - T_{\text{budget}}| > 1.5\text{s}$, rewrite the sentence for tighter economy or expand for clarity.

## Step-by-Step Execution Protocol

1. **Intake Beat Manifest:** Load all beats from `BPL01.json`.
2. **Drafting Narration per Beat:**
   - Expand the draft narration into final, broadcast-quality spoken English.
   - Maintain the exact pedagogical focus defined in `learning_point`.
   - Ensure seamless transition phrases between consecutive beats.
3. **Embed TTS Cues:** Add pause markers and phonetic stress annotations.
4. **Cadence Audit:** Run word and syllable verification.
5. **Generate Dual-Format Artifacts + TTS Export:**
   - Canonical `NS01.json`
   - Human review copy `NS01.md`
   - Clean TTS export `tts_export.txt` (stripped of metadata, ready for TTS ingestion).
6. **Internal Adversarial Review:**
   - *Naturalness Lens:* Does this sound like a warm, charismatic teacher in a 1-on-1 session?
   - *Timing Lens:* Are all beat durations within tolerances?
   - *Linguistic Lens:* Are all grammar terms and example sentences 100% accurate per `LDB01`?

## Output Artifact Schema (`NS01.json`)

```json
{
  "schema_version": "1.0.0",
  "project_id": "WB-xxxx",
  "artifact_id": "NS01",
  "version": "1.0",
  "source_bpl_version": "1.0",
  "status": "in_review",
  "voice_profile": {
    "voice_id": "david",
    "target_wpm": 140
  },
  "total_words": 680,
  "total_estimated_duration_seconds": 295,
  "scenes": [
    {
      "scene_id": "SC01",
      "beats": [
        {
          "beat_id": "B01.01",
          "spoken_text": "Have you ever wondered why we say 'two apples' [pause=400ms], but never 'two waters'?",
          "clean_text_for_tts": "Have you ever wondered why we say two apples, but never two waters?",
          "word_count": 14,
          "syllable_count": 18,
          "allocated_duration_seconds": 6.0,
          "estimated_spoken_seconds": 5.8,
          "cadence_status": "OPTIMAL",
          "cue_spans": [
            {"cue_text": "two apples", "cue_type": "VISUAL_TRIGGER", "target_element_id": "SC01_E01"},
            {"cue_text": "two waters", "cue_type": "VISUAL_TRIGGER", "target_element_id": "SC01_E02"}
          ]
        }
      ]
    }
  ],
  "approval_gate": {
    "gate_id": "G05A",
    "state": "PENDING_USER_APPROVAL"
  }
}
```

## Mandatory Approval Gate G05A

- Present `NS01.md` with cadence metrics and `tts_export.txt`.
- User reviews tone, pronunciation, and flow.
- Upon approval, lock the exact spoken text; cue spans are immediately transmitted to S05B for exact binding.

