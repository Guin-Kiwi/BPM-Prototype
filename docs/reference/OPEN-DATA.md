# Open-data intake plan

## Outcome

Prepare a small, attributable field-image sample for the farmer-facing report
scenario, with suitability and limits known before any diagnosis evaluation.
Source inspection, sample selection and evaluation are separate steps; no model
call is needed for the intake demo.

## Requirements and boundaries

### Observable selection criteria

- Prefer on-plant images resembling a farmer's view in the field. Inspect actual
  files, annotation coverage and label meanings before selecting a small, bounded
  sample. Include healthy or nonproblem controls for evaluation where supported.
- Verify each selected file's actual format and size against the upload requirements
  in [UC-001](../specs/UC-001-REPORT-INTAKE.md). Assess whether annotations support
  the intended use; leave missing or ambiguous labels unknown. Do not infer an
  image-level disease or severity label from leaf-instance annotations.
- UC-001 owns the accepted synthetic farm/field seed requirements, including counts,
  history and the empty-history case. This plan does not reopen them.

### Provenance

Record for each selected image its dataset DOI/version, original ID and path,
download URL and date, neutral local filename, SHA-256, available label type and
value, licence and attribution, transformations, reuse and related images. Keep raw
files in ignored `data/` and the manifest separate from diagnosis inputs. Check the
actual terms for each source and intended use, including attribution and any CC
licence conditions; do not assume one dataset's licence covers another.

### Evaluation safeguards

Images do not establish real farm history, location, disease incidence, treatment
outcomes or business-action labels. Label fictional dates, descriptions, findings
and actions as synthetic scenario context; a fictional prior confirmation is not a
real technician's confirmation. A convenience sample cannot establish population
performance or measured incidence.

Keep observations, prior confirmed findings, model inferences and hidden current-image
scoring labels distinct. Prior confirmed findings may appear as legitimate history,
including in normal intake when an image repeats. For diagnosis evaluation, exclude
and record history that reveals the current answer, including findings tied to reused
or related images such as crops of one parent. Record reuse and relationships; do not
count crops and their parent as independent samples. Keep current answers and
label-bearing IDs or filenames out of displayed observations, attachment names,
intake payloads, prompts and other diagnosis inputs. Keep provenance and scoring
metadata separate and compare outputs with hidden labels only after inference.

Report controlled BRACOL and field-condition results separately. Preserve each
source's label meanings and severity scale; do not map scales across sources without
an explicit justification or turn labels into business actions without a separate
rule. Where requirements expect uncertainty handling or requests for more evidence,
assess those behaviors explicitly, without making them universal success criteria
or substituting model self-confidence for evidence.

## Open choices

- **Next inspection — recommend BRACOT version 1.** Its [official record](https://data.mendeley.com/datasets/pmkbyjpf6k/1)
  (DOI `10.17632/pmkbyjpf6k.1`) describes 300 Galaxy S8 smartphone images of
  parts of Arabica coffee trees in a Brazilian plantation and 1,662 annotated leaf
  instances, for instance segmentation. This field context better matches the
  intended report than detached leaves. The actual annotations, disease-label
  coverage and terms remain uninspected; final selection and evaluation suitability
  remain open. If disease labels are absent, the images may serve upload/context
  only; diagnosis scoring needs another suitable truth source or expert work.
- **Backup — RoCoLe version 2.** Its [official record](https://data.mendeley.com/datasets/c5yvn32dzg/2)
  (DOI `10.17632/c5yvn32dzg.2`) describes smartphone images of Robusta with
  healthy/unhealthy state and disease severity. Its species differs from BRACOT's
  Arabica; keep its severity labels and scale separate. Suitability and terms need
  inspection before use.
- **Optional — JMuBEN.** The [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC8165403/)
  describes a possible field-acquired Arabica source from Kenya. Inspect its data
  availability, annotations, terms and existing preprocessing before deciding;
  it is not needed to complete BRACOT inspection.
- **Controlled comparator — BRACOL version 1.** The detached whole leaves on plain
  backgrounds support upload examples and a separately reported comparison, not
  evidence of realistic farmer-image performance. Prefer whole leaves before crops.
  The [manifest](EXAMPLE-IMAGES.md) owns source details, IDs, labels, hashes and
  CC BY 4.0 attribution. Current examples are not an evaluation set.

## Steps

1. Inspect BRACOT's archive structure, actual image files, annotations, coverage,
   related-image structure and licence/terms. Record what is available and unknown.
2. Based on that inspection, propose a small field sample with original IDs, paths,
   provenance and available label types/values, including controls if supported.
   Select only after suitability and reuse relationships are understood; a failed
   selection is a finding, not a successful sample. Consider a backup if needed.
3. Verify selected files and complete their manifest. If used in scenarios, label
   synthetic context and record reuse. Apply and record the display and evaluation
   leakage checks before the corresponding use.
4. Before diagnosis scoring, establish suitable truth and its coverage independently
   of model inputs. If it is unavailable, limit use and claims accordingly; obtain
   another truth source or expert work before scoring. Keep any later source-specific
   results separate.

## Completion evidence

**Current evidence:** Three author-hosted BRACOL whole-leaf examples were downloaded
locally for manual upload; their provenance, hashes and attribution are in the
[manifest](EXAMPLE-IMAGES.md). They are not seeded into farm history or selected as
an evaluation set. No BRACOT files have been downloaded or inspected, no new sample
has been selected, and no new experiments have been run.

**Source inspection:** Complete when the archive structure, available annotations and
coverage, related-image information, and applicable licence/terms have been checked
and recorded, including unknowns. Inspection can finish with an unsuitable source;
that does not complete sample selection.

**Small field sample:** Complete only when selected files exist and their actual
format and size have been verified; terms have been checked; the per-image manifest
above is complete; annotation coverage and suitability for each intended use are
known; unknowns restrict claims; and reuse, related images and applicable display
and evaluation leakage are handled and recorded. For scenario import, also identify
synthetic context and image reuse. If these conditions cannot be met, record the gap
and do not claim selection or import complete.

**Diagnosis-evaluation readiness:** Separate from inspection and sample completion.
Require suitable disease truth and known coverage, source-specific label meanings,
hidden scoring metadata, and recorded exclusions for answer-revealing history and
related images. Without suitable truth, retain only supported upload/context use and
obtain another truth source or expert work before scoring diagnosis.
