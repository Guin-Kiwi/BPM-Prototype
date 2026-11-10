# UC-002 prepared guidance candidates

These are two short, project-worded, non-treatment entries for the proposed
communications relay in [UC-002](../specs/UC-002-ASSESSMENT-HANDOFF.md). They are
selected illustrative content for the first bounded observation demonstration. This
selection is not group policy, a diagnosis, technician approval or agronomic validation.

## Candidate entries

### G-RUST-OBSERVE-1 — possible coffee leaf rust

**Farmer message:**

> The image assessment suggests possible coffee leaf rust, but a photo cannot
> confirm it or estimate how much of a plot is affected. Please note the plot and
> observation date and include a clear view of the underside of an affected leaf.
> A field survey can check sampled leaves across the plot and record the count with
> rust signs.

**Embrapa evidence:** *Manejo integrado de pragas e doenças do café arábica*,
“Doenças do café arábica” → “Ferrugem do cafeeiro” → “Descrição e biologia” and
“Métodos de manejo,” printed pp. 11–12. The source says the disease is caused by
*Hemileia vastatrix* in Brazilian Arabica coffee and describes yellow, powdery
marks on the underside of leaves. For field monitoring it describes sampling about
25 randomly selected plants per plot, four leaves per plant from the lower third,
and inspecting the leaf undersides; incidence is based on leaves with sporulating
pustules over the total sampled.

**Claim boundary:** The disease, visible sign, and sampling/count method above are
source-supported. “The image assessment suggests” is a project-authored wrapper
that may be populated only from the actual model output; it must remain explicitly
suspected. Asking for plot/date and a clear underside view is project-authored
communication wording, not an Embrapa recommendation. The source does not say that
a submitted photo confirms disease, establish image-classifier validity, or prescribe
which staff role receives the report.

### G-LEAF-MINER-OBSERVE-1 — possible coffee leaf miner

**Farmer message:**

> The image assessment suggests possible coffee leaf miner, but this image assessment
> does not establish whether a mine is active or how much of a plot is affected.
> Please note the plot and observation date and share a clear view of the affected
> leaf for review.
> Field monitoring checks sampled leaves for mines and whether live larvae are
> present.

**Embrapa evidence:** The same circular, “Bicho-mineiro-do-café” → “Descrição e
biologia” and “Métodos de manejo,” printed pp. 5–6. It identifies *Leucoptera
coffeella*, describes larvae forming mines inside coffee leaves, and says it occurs
in Arabica-producing regions of Brazil. Its field method samples 25 randomly chosen
plants per plot, taking leaves from specified pairs on the four compass-facing sides
and the middle or upper third; its text distinguishes active mines with live larvae.
The monitoring interval in the source is every 15 days during the dry period.

**Claim boundary:** The species/host, leaf mines, sampling description, and
active-mine distinction are source-supported. “The image assessment suggests” is a
project-authored wrapper that may be populated only from actual model output; it is
not confirmation. The current classifier does not assess live larvae; a submitted image supplies no
representative plot sample. Asking the farmer to note plot/date and share the leaf is project-authored
communication wording, not a quoted or prescribed Embrapa step. The source does not
assign a communications/technician route or urgency to a model label.

## Applicability and system boundary

- Match a candidate only to the corresponding **suspected-issue output from the
  actual model assessment**. Treat that output as inference, not confirmed disease
  or pest. These messages do not tell the model what to predict.
- If model output is unknown or does not match either entry, these entries supply no
  message. Do not have staff hand-enter a desired issue, route, risk, confidence,
  eligibility, or outcome to make a candidate apply.
- Deterministic routing is a separate rule using the recorded actual model outputs
  and synthetic report history. This content file defines no route, risk category,
  threshold, visit decision, escalation priority, or eligibility rule. The Embrapa
  source is agronomy context, not a routing policy.
- The source describes Brazilian *Coffea arabica*. Farm, cultivar, location,
  phenology, plot boundaries and field symptoms are not established by these entries.
  Sampling methods are for field monitoring; one uploaded leaf image is not a
  representative plot sample. Neither message includes treatment, product, dose,
  field severity, harvest, pickup or yield instruction.
- The project-authored message can be revised as product communication. Do not
  reproduce the source manual, its illustrations, or its wording in the application.

## Primary source and access

Eveline Teixeira Caixeta et al., *Manejo integrado de pragas e doenças do café
arábica*, Embrapa Café, Circular Técnica 8 (2024), 35 pp.

- [Official Embrapa publication record](https://www.infoteca.cnptia.embrapa.br/infoteca/handle/doc/1167902)
- [Full Circular Técnica 8 PDF](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1167902/1/Circular-Tecnica-8-Manejo-integrado-de-pragas.pdf)

The repository record identifies the item as open access and lists CC BY-NC-ND 4.0.
This file contains original short paraphrases with source attribution and links; it
does not include the manual or figures. The license metadata is recorded as source
context, without asserting a legal conclusion about these independently worded
messages.

## Demonstration check

Using synthetic report history and an actual run's model output, show each fixed
message only for its matching suspected-issue output, preserve the inference label,
and record that communications relayed the selected message. Separately demonstrate
the deterministic route from actual outputs and synthetic history. Do not use
hand-entered desired route/risk/eligibility to construct the example. The full passages and printed page markers were checked directly, including leaf-miner
methods on p. 6 and rust methods on p. 12. These are
SPECIFY acceptance cues; no app behavior or agronomic validation is claimed here.
