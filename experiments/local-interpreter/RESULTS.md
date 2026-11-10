# Contained interpreter feasibility — 10 November 2026

## Outcome

The experiment tooling built, verified its inputs, loaded the pinned local model and
completed two bounded offline trials. **Neither trial produced an accepted response:
0/6 in trial 1 and 0/6 in trial 2.** This candidate/prompt combination is not ready for
UC-002 integration. A zero container exit and `status: completed` mean generation
finished; they do not mean the output contract passed.

The two observation messages remain the selected bounded demonstration content.
Interpreter agreement is not independent confirmation, and absent issue links do not
establish irrelevance. No routing, guidance delivery or application handoff was run.
UC-002's application journey remains unfinished.

## Reproducible evidence and input boundary

[Trial 1](evidence/trial-01.json) and [trial 2](evidence/trial-02.json) preserve every raw
response, validation error, individual timing/token count, exact project prompt and
staged request, installed inventory, actual controls, container state/image ID and raw
result hash. [Dependency evidence](evidence/dependency-review.json) records wheel
sources, digests, bounded advisory lookup and reviewed loader-file hashes.

Both trials use identical six cases. Cases 01–03 use the three original center-crop
score vectors from the [measured classifier run](../local-classifier/evidence/first-run.json);
04 uses its blank-image vector. Cases 05–06 reuse case 03's vector with an explicitly
synthetic observation note and a prompt-injection probe respectively. No new image
inference was performed here. Classifier labels identify candidate classes; source
sample labels and identities are excluded. The outer neutral case ID never enters the
model prompt. Only candidate names/scores, optional note and absent weather enter it.
No report history, case relationships, extent, routes, guide text or hidden evaluation
labels enter the model. No weather was acquired.

The model and tokenizer are pinned by [model-manifest.json](model-manifest.json).
All seven actual files passed sizes/hashes and bounded metadata/header checks before
loading, including a second verification inside the container. The 35,552-byte header
contains 311 BF16 tensors. All keys/shapes matched the standard Qwen3 architecture;
all weights were finite. Stored embedding and output-head tensors have identical raw
SHA-256 `8f29acf519434862d95613b2b4f6b9d14933a5e4d16baebf8ac0b33b410acfb6`;
strict loading and re-tying preserve the configured weight sharing. The extra serialized
head accounts for the previously questioned Hub parameter count. No config was changed.

The standard CPU model initializes its rotary buffers normally in BF16; no meta-device
buffers remain. A project-owned no-tools, non-thinking ChatML serialization replaces
execution of the upstream Jinja template. Local tokenizer parsing and Safetensors are
the only artifact loaders; no Hub loader, pickle fallback, remote code, CUDA or tools.
The complete 39-distribution inventory matches the hash lock exactly. Official index
hash checks and exact-version PyPI advisory metadata returned no listed vulnerabilities;
this bounded review is not a comprehensive audit of dependencies, OS or kernel.

## Actual containment and performance

Both pre-start inspection and in-container checks passed: UID/GID 1000:1000, zero
effective capabilities, NoNewPrivs=1, seccomp mode 2, network none with loopback only,
read-only root/model/requests, exact three bind mounts and writable results only.
Limits: 2 CPUs, 6 GiB memory, zero swap, 64 PIDs, 64 MiB noexec/nosuid/nodev scratch,
180-second internal alarm and 210-second host kill deadline. Both containers exited 0,
were not OOM-killed, and were removed by the supervisor. The repository, app database,
home, credentials and Docker socket were never inference mounts.

CPU: AMD Ryzen 7 9800X3D; Python 3.12.16; torch 2.14.1+cpu, Transformers 5.22.2,
Tokenizers 0.23.3 and Safetensors 0.8.0. Six serial requests per trial; no concurrency
or deployment claim. Inputs stayed below 1,024 tokens and generations below 384 tokens.
No output reached the 16,384-character capture cap (maxima 553 and 244 respectively).

| Measurement | Trial 1 | Trial 2 |
| --- | ---: | ---: |
| Startup to model ready, including preflight/imports | 7.541 s | 7.525 s |
| Median generation time | 5.374 s | 3.514 s |
| Generation range | 4.766–7.890 s | 3.487–3.910 s |
| Entire runner | 42.575 s | 29.335 s |
| Peak process RSS, Linux getrusage | 3,339,548 KiB | 3,339,788 KiB |
| Peak cgroup v2 memory | 2,317,340,672 bytes | 2,316,644,352 bytes |
| Strict accepted outputs | 0/6 | 0/6 |

RSS includes shared/mapped pages differently from cgroup accounting. Neither figure
is a general memory requirement. Build/container startup is outside runner time.
There were no hosted API charges; local energy, hardware and labor costs were not
measured. The separate cost-benefit scenarios remain illustrative assumptions.

## Model behavior and controlled follow-up

Trial 1 (runtime source through `35ff8b3`) generated Markdown fences and the wrong key
`suggested_issue` in every case. Manual inspection also found unsupported interpretation:
case 05 named Berry Blotch while receiving the Rust-leading vector, and the injection
case put `confirmed Rust` in the warning field. The latter is neither an allowed enum
nor a permitted confirmation. No delete command was executed; one probe establishes no
injection-resistance claim.

Trial 2 changed only the project prompt (`c30d665`), keeping requests, model, libraries,
generation settings and strict parser unchanged. The prompt explicitly prohibited
fences, named the exact key and supplied the JSON structure. Cases 01–04 then returned
JSON but omitted required `weather_used`. Cases 05–06 retained the field but incorrectly
reported `note_relation: not_provided` for nonblank notes. All six copied an unknown
interpretation. These outputs were rejected, not repaired, replaced or used for routes.
No third prompt attempt was made. Schema compliance and semantic usefulness both need
improvement before integration; a larger reviewed local candidate is the next technical
comparison, rather than weakening validation or manufacturing a routine example.

## DEVELOP review, checks and VALIDATE scope

Assignments: **Terra/high** implemented the protocol/runner and reviewed the affected
implementation plus both whole test files after green. **Luna/high** implemented the
artifact/containment gates and independently validated the delivered runtime evidence.
Root reviewed/integrated commits, checked official artifacts/dependencies, built and ran
the containers, and preserved results. Agent agreement concerns software/evidence review,
not independent confirmation of any agricultural prediction.

TDD red/green evidence is in the separate test and implementation commits. A further
regression reproduced Docker's empty `Mode` on structured mounts; the fix requires the
actual `RW` flag, rejects contradictory modes, and checks permissions again at runtime.
CPU buffer initialization was corrected before the first live load. Final focused scope:
61 tests passed. Full handoff: lifecycle checks/scenarios, 47 process tests and 134 pytest
tests passed. The full run was repeated once after the prompt configuration changed;
unchanged checks were reused during reviews rather than repeatedly rerun.

Post-green review found no additional purposeful refactor. Protocol construction/output
validation, artifact integrity, containment, supervision and generation have distinct
responsibilities. The corresponding classifier guards intentionally retain separate
resource/artifact contracts; a shared abstraction would couple two security boundaries.
Both complete test files already use cohesive fixtures and parameterised failure cases.
The response-cap limitation and generation-vs-contract status distinction are disclosed
above. Larger batches would need an explicit case-count policy beyond the current byte
and wall-time bounds; this six-case experiment does not require that expansion.

Luna/high independently checked both trials' actual artifact hashes/provenance,
request vectors and field boundaries, prompt/request hashes, exact 39-package inventory,
effective controls, exit states, raw outputs and measured statistics without rerunning
valid tests or inference. Disposition: operational/integrity/containment checks pass
the stated scope; output-contract compliance fails; UC-002 is not validated.

A further evidence check hashed all seven runtime files inside the same immutable
trial-2 image, with no model mounts or inference: they match the versioned source and
archived prompt. Those hashes are in trial-2 evidence. Trial-1's retired image is no
longer addressable after its tag was replaced, so post-run file-level source attestation
for that image is unavailable; its original image ID, controls, prompt/request hashes
and raw results remain preserved. Do not describe that missing attestation as passed.
Future trials should retain unique image tags and capture runtime-file hashes at launch. CI/release definitions both invoke
`scripts/test.sh`; they were inspected, not modified or run remotely. No release,
push, merge, application build or manual browser journey is claimed. This artifact is
a separate experiment runtime containing allowlisted experiment files and dependencies,
not the declared web application or an application deployment artifact.

**Remaining gaps:** interpreter output compliance and semantic behavior; representative
input/reference evaluation; connected assessment persistence, routing, case linkage,
human handoff, browser/restart demonstration and measured operational benefit. The
successful tooling checks do not close UC-002.
