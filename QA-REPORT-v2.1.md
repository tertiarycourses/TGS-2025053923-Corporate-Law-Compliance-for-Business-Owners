# Courseware QA Report — v2.1

Course: Corporate Law Compliance for Business Owners  
Course code: TGS-2025053923  
TSC: ACC-BLR-5001-1.1 Corporate and Business Law  
QA date: 12 August 2026

## Result

PASS — the package is aligned to the approved course proposal, visually reviewed, structurally valid and ready for controlled publication.

## A. Approved course and competency alignment

| Component | Approved evidence | Courseware evidence | Result |
|---|---|---|---|
| Duration | 7 hours training + 1 hour assessment | Lesson Plan totals 480 non-break minutes; WA 30 min + CS 30 min | Pass |
| K1 | Global developments and legal/regulatory framework | Topics 1–2; Activities 1–4; WA Q1–Q2 | Pass |
| K2 | Organisation, environment and industry | Topics 2–4; Activities 3–8; WA Q3–Q4 | Pass |
| A1 | Assess impact of legal/regulatory changes | Activities 1–5; CS Task 1 | Pass |
| A2 | Drive decision-making | Activities 5–6; CS Task 2 | Pass |
| A3 | Influence business units | Activities 7–8; CS Task 2 | Pass |

No stale K3 reference from the old learner paper remains.

## B. PowerPoint QA

- 103 slides in 16:9 format; all text uses Arial.
- All 103 rendered slides were reviewed via five contact sheets; selected dense/scenario/debrief slides were reviewed at higher resolution.
- Fresh-eyes review identified the trainer placeholder, long citation footers and two title-wrap problems. These were corrected and re-rendered.
- Independent shape-geometry check found zero objects outside the slide canvas.
- The bundled pixel-padding checker reports every slide because its enlarged test canvas conflicts with the deck's explicit full-bleed white background. This is a tool false-positive: the shape-geometry check and rendered visual review both show no overflow.
- No detailed procedural steps, screenshots, buttons, menus or click instructions appear in the PPT. Conceptual process maps remain as learning content.
- Eight activities use overview, real-case evidence and debrief/success-check slides only.

## C. Learner Guide and Lesson Plan QA

- Learner Guide: 40 pages, visually inspected page-by-page through four complete contact sheets.
- Lesson Plan: 7 pages, visually inspected page-by-page.
- Detailed steps, real-case scenarios, questions, worksheets, acceptance checks and linked official sources are present for all eight activities.
- Each Markdown activity has a matching two-page branded PDF; all 16 activity pages were rendered and visually inspected.
- Lesson Plan slide ranges are generated from `courseware/slide_map.json`; mappings cover slides 1–103.
- DOCX ZIP integrity passed; generated PDFs open and report the expected page counts.

## D. Assessment QA

- WA Candidate Paper: 6 pages; 30 minutes; four SAQ questions; K1–K2; 40 marks.
- WA Answer Key: 6 pages; model evidence and mark allocation for all four questions.
- Case Study Candidate Paper: 4 pages; 30 minutes; two tasks; A1–A3; 40 marks.
- Case Study Answer Key: 4 pages; task rubrics, model evidence and acceptable decision variation.
- Candidate papers follow the required structure: page 1 cover, page 2 candidate data/instructions/grading, page 3 onward assessment content.
- Every page of all four instruments was rendered and inspected. No clipping, broken tables or orphaned assessor boxes were found.
- Assessment files remain confidential and are excluded from GitHub.

## E. Source QA

- Singapore propositions and the eight activity cases are tied to ACRA, IRAS, MOM and PDPC sources in the slide footers, Learner Guide, activity worksheets and `SOURCES.md`.
- Case status is stated precisely. Charges are not described as convictions, published findings are separated from learner assumptions, and missing incident facts are not invented.
- Secondary sources are used only for comparative compliance-programme concepts; foreign law is not presented as Singapore law.
- The supplied ACRA announcement 872 page was inaccessible at build time and is explicitly marked as not relied upon.
- Educational/legal-advice boundary and currency warnings are prominent.

## F. Publication verification

- Google Drive dry-run passed, then the full package was uploaded. Superseded v1/v2 artifacts were moved to archive folders; no destructive deletion was used.
- TMS authenticated dry-run passed after upload. The production write returned HTTP 200 and all seven courseware fields were read back and fetched successfully.
- TMS links only the WA and Case Study candidate papers; answer keys remain in the controlled Drive assessment folder and are not linked to learners.
- GitHub was replaced with explicit-file staging after a secret scan. Remote and local commit SHAs were verified equal; `.env`, assessments, references, generated build tooling and QA render outputs are excluded.
