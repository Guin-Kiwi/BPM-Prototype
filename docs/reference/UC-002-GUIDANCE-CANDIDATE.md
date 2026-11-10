# UC-002 illustrative guidance candidate

**Status:** one proposed, non-treatment entry for review; not selected policy,
technician-approved advice, a diagnosis, or agronomic validation. It is a static,
attributed example for the proposed human relay in [UC-002](../specs/UC-002-ASSESSMENT-HANDOFF.md).

## Candidate entry

**Proposed entry ID:** `G-RUST-OBSERVE-1`.

**Topic:** observation and field monitoring for *possible coffee leaf rust*
(*Hemileia vastatrix*) in Arabica coffee.

**Prepared farmer message (original paraphrase):**

> To discuss possible coffee leaf rust, please note the plot and date and
> share clear photos of the leaves, including their undersides, with the advisory
> team. A photo alone cannot confirm rust or estimate how much of a plot is affected.
> If a field estimate is appropriate, a technician can use a consistent plot sample
> and record how many sampled leaves show rust signs. This message does not recommend
> treatment.

This message is intended for a communications staff member to relay as an
observation prompt. The optional sample-method detail is for technician follow-up,
not an instruction for the farmer to perform a formal survey: Embrapa's Arabica
method samples about 25 randomly selected plants per plot, with one leaf from the
third or fourth pair on each of the four compass-facing sides in the lower third of
the plant; the technician inspects the lower leaf surface. The technician must
interpret the field result.

## Applicability and facts needed

- **Source context:** Brazilian *Coffea arabica*; the source identifies coffee leaf
  rust as caused by *H. vastatrix*. Its monitoring interval is fruit formation
  through harvest. This is not a generic coffee or all-leaf-disease message.
- **Must be explicitly known before display:** the crop is Arabica coffee and the
  report is being discussed as possible coffee leaf rust. Neither a photo nor an
  AI class score establishes those facts. In the theoretical demo, the staff user
  selects these categorical facts from a clearly labeled synthetic scenario; the
  application does not infer them as confirmed. If either fact is unknown, do not
  show this entry; leave the issue uncertain and route to technician review.
- **Not farm-specific:** cultivar, plot definition, fruit stage, local conditions,
  sampling history and actual field symptoms are unknown. The message does not claim
  that rust is present, establish incidence or severity, set a threshold, or direct
  a treatment. The source's sampling method estimates plot incidence; it does not
  turn a single submitted leaf photo into a plot estimate.
- **Human boundary:** a technician assesses relevance and any follow-up. The relay
  records communication only; it is not evidence of technician approval or case
  resolution. No model may write or alter this guidance text.

## Source and reuse

Primary source: Caixeta et al., *Manejo integrado de pragas e doenças do café
arábica*, Embrapa Café, Circular Técnica 8 (2024), 35 pp. The applicable passage is
“Doenças do café arábica” → “Ferrugem do cafeeiro” → “Métodos de manejo,” printed
pp. 11–12. It describes rust signs on the lower leaf surface, monitoring from fruit
formation through harvest, and a plot sample of about 25 randomly chosen plants with
four leaves per plant selected from the lower third. The paper also discusses
chemical control thresholds in that
section; **this candidate intentionally excludes thresholds and all treatment
content**.

- [Official Embrapa publication record](https://www.infoteca.cnptia.embrapa.br/infoteca/handle/doc/1167902)
- [Full Circular Técnica 8 PDF](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1167902/1/Circular-Tecnica-8-Manejo-integrado-de-pragas.pdf)

Embrapa's record identifies access as open access and lists the repository license
as [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/); the PDF
also states that all rights are reserved to Embrapa. This draft uses an original,
short paraphrase with attribution; it does not reproduce source wording, illustrations
or the manual. Do not redistribute the manual or adapted source material with the
prototype. The repository notice does not establish permission to redistribute an adapted manual.
This proposal includes an independently worded message and a citation, not a manual
adaptation or a claim of legal clearance. Source-material redistribution is outside
the current demonstration.

## Candidate acceptance check

For a synthetic Arabica / possible-rust scenario, staff can select this fixed entry,
relay it, and record that it was relayed. Verify the message contains no diagnosis,
treatment, product, dose, harvest or pickup instruction; does not present model output
as fact; and is unavailable when crop or topic is unknown. This is a planned
specification check, not completed application behavior or validation of the agronomic
content.
