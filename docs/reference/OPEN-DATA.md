# Open-data intake plan

## Selection authority and next inspection

The farmer-facing framing is an on-plant field report: images should resemble a
farmer's view of a plant in the field. BRACOL's detached whole leaves on plain
backgrounds remain useful as upload examples and for a separately reported
controlled-condition comparison. They are not evidence of realistic farmer-image
performance.

Prioritise **BRACOT version 1** for the next data inspection: [official dataset
record](https://data.mendeley.com/datasets/pmkbyjpf6k/1), DOI
`10.17632/pmkbyjpf6k.1`. Its indexed official description reports 300 smartphone
images of parts of Arabica coffee trees photographed with a Galaxy S8 in a Brazilian
plantation, and 1,662 annotated leaf instances. The stated purpose is instance
segmentation. This capture context better matches the intended field-report framing
than detached-leaf images. It does not establish that every image has a usable
disease or severity truth label. Before selecting any evaluation image, inspect the
available annotation files and terms/licence directly; do not infer image-level
truth from instance annotations or the dataset description. No BRACOT files have
been downloaded and no new experiments have been run.

Keep the next step small: inspect the archive structure and annotation coverage, then
propose a small field sample with each original image ID, source path, provenance,
and available label type/value. Include healthy or nonproblem images as evaluation
controls even though a farmer's report trigger is a suspected issue. Do not decide
the final sample until annotations and reuse/related-image structure are understood.

**Backup candidate:** [RoCoLe version 2](https://data.mendeley.com/datasets/c5yvn32dzg/2),
DOI `10.17632/c5yvn32dzg.2`, is a smartphone-image Robusta dataset whose official
record describes healthy/unhealthy state and disease severity. Its species differs
from BRACOT's Arabica. If used, keep its severity labels and scale separate; do not
pool or translate severity across sources without an explicit, justified mapping.

**Optional candidate:** [JMuBEN](https://pmc.ncbi.nlm.nih.gov/articles/PMC8165403/)
is a possible field-acquired Arabica source from Kenya. Inspect the paper, data
availability, annotations, licence/terms, and preprocessing already applied before deciding
whether it is suitable. It is not needed to complete the BRACOT inspection step.

## Existing BRACOL upload examples

[BRACOL version 1](https://data.mendeley.com/datasets/yy2k5y8mxg/1), DOI
`10.17632/yy2k5y8mxg.1`, is the source for the three existing detached-leaf upload
examples documented in the [manifest](EXAMPLE-IMAGES.md). The manifest's source IDs,
URLs, labels, and SHA-256 hashes are historical provenance and remain unchanged.
BRACOL is licensed CC BY 4.0; retain the attribution in that manifest.
These images demonstrate attachment handling and can support a controlled-condition
comparison. Their plain-background setup differs from on-plant farmer reports, so
do not use them alone to claim realistic field performance.

## Scenario, provenance, and evaluation boundaries

UC-001 owns the accepted and implemented synthetic farm/field seed requirements,
including counts, history, and empty-history behavior; see
[UC-001](../specs/UC-001-REPORT-INTAKE.md). This document owns open-data source
selection and evaluation-sample guidance. Do not reopen seed-count decisions here.

For each selected image record dataset DOI/version, original ID/path, download
URL/date, neutral local filename, SHA-256, available labels, licence/attribution
and transformations. Keep raw files in ignored `data/`; verify actual image format
and upload size. Unknown labels stay unknown.

Images alone are not real farm history, disease incidence, treatment outcomes, or
business-action labels. Synthetic histories must remain explicitly labelled
synthetic; any fictional finding or action is scenario context, not source ground
truth. Current-sample scoring labels and label-bearing identifiers stay separate from
displayed observations, attachment names and future diagnosis inputs. Earlier
confirmed findings may be legitimate history; for diagnosis evaluation, exclude and
record history that reveals the current sample answer. Keep scoring/provenance
metadata outside inference inputs. Record image reuse and relationships
(including crops from one parent) and prevent answer leakage through history.

In later experiments, report controlled BRACOL and field-condition results separately.
Where requirements define uncertainty handling or a request for more evidence as an
expected behavior, assess and report those behaviors explicitly. Do not treat them
as universal success criteria or substitute model self-confidence for evidence-based
uncertainty handling. Keep source label meanings and scales intact; do not convert
them into business actions without a separately defined rule.
