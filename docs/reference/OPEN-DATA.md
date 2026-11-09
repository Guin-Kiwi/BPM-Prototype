# Open-data intake plan

## First source

BRACOL version 1, DOI `10.17632/yy2k5y8mxg.1`, Renato A. Krohling,
Guilherme J. M. Esgario and José A. Ventura, published 6 November 2019.
[Dataset and licence](https://data.mendeley.com/datasets/yy2k5y8mxg/1)
(CC BY 4.0; source page checked 9 November 2026).

The source describes 1,747 original Arabica leaf photographs with disease/severity
labels and a separate cropped-symptom dataset. Photos use a white background under
partially controlled conditions. They are not validated farmer submissions or
operational Cooxupé records. Use whole leaves first; do not count crops and their
parent images as independent evaluation samples.

## Proposed synthetic seed and import

Recommend two fictional farms with two fields each, three earlier reports distributed
across them, at least one earlier confirmed finding, and one field with no history.
This gives field isolation, history and empty-state examples with little setup; counts
are a recommendation, not an approved requirement. Observation dates and descriptions
are invented scenario context, explicitly labelled synthetic. A confirmed finding is
also fictional: it represents a prior confirmation within the scenario, not a claim
that an actual technician confirmed that farm's diagnosis.

If images are used, recommend selecting about 6–10 original leaves spanning healthy
and diseased examples after inspecting the download structure. Counts and selection
remain open. Keep raw downloads in ignored `data/`; do not invent sample IDs or claim
a balanced evaluation set before inspecting labels. Dataset images can populate
synthetic history, but cannot establish real farm history, location, treatment success
or field incidence. Identify image reuse; it is not independent field evidence.

For each selected sample record dataset DOI/version, original sample ID/path, download
URL/date, local neutral filename, SHA-256, original disease/severity label,
licence/attribution and transformations. Keep scenario context separate from source
provenance and evaluation labels. Preserve source severity categories without turning
them into business actions.

## Evidence and evaluation boundaries

Keep submitted observations, fictional earlier confirmed findings, AI inferences and
hidden current-sample ground truth distinct. A prior confirmed finding can be displayed
and later supplied as legitimate history. Do not surface current-sample answers or
label-bearing source filenames in the UI, intake payload, attachment names, prompts
or other diagnosis inputs. Keep original IDs/paths and labels in restricted provenance
and evaluation metadata, accessible for scoring rather than diagnosis.

When preparing a later diagnosis evaluation, prevent history or reused/related images
(including crops of the same parent) from revealing the current sample's answer; omit
or separate conflicting history and record the exclusion. Compare actual model outputs
with hidden labels only after inference. No model call is needed for the intake demo.

## Completion evidence

Three author-hosted whole-leaf examples are downloaded locally for manual upload;
see the [manifest](EXAMPLE-IMAGES.md). They are not seeded into farm history or
selected as an evaluation set. The planned scenario import is complete only when selected files exist,
hashes and provenance are recorded, synthetic scenarios and image reuse are identified,
and the relevant display and evaluation leakage checks pass. A small convenience
sample cannot establish population performance or measured incidence.
