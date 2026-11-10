# Local text interpreter candidate: metadata review

## Status and scope

This read-only candidate review supports the local technical recommendation in the
[demonstration proposal](../../docs/reference/UC-002-DEMO-RULES.md). It is not a provider decision, security clearance, installed dependency set,
verified local artifact, or inference result. No weights were downloaded or loaded, no
credentials used, and no paid or live inference called. Model, template, dependency,
hardware and behavior claims below are limited to the cited official metadata and the
repository's existing containment evidence.

## Candidate and pin

Candidate: official [Qwen/Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B), a
text-generation model published under the `Qwen` account. The official Hub API returned
revision `c1899de289a04d12100db370d81485cdf75e47ca` (last modified 2025-07-26),
`Qwen3ForCausalLM`, `model_type: qwen3`, `AutoModelForCausalLM`, Safetensors format,
Apache-2.0 metadata, and 751,632,384 BF16 parameters. The model card names the model
0.6B. The relationship between that name, stored tensor count and tied embeddings
requires reconciliation; the Hub total is not independent architectural verification. The reviewed
revision is immutable; do not resolve `main` at runtime.

Primary records: [pinned Hub metadata](https://huggingface.co/api/models/Qwen/Qwen3-0.6B/revision/c1899de289a04d12100db370d81485cdf75e47ca?blobs=true),
[pinned model card](https://huggingface.co/Qwen/Qwen3-0.6B/blob/c1899de289a04d12100db370d81485cdf75e47ca/README.md),
[pinned configuration](https://huggingface.co/Qwen/Qwen3-0.6B/blob/c1899de289a04d12100db370d81485cdf75e47ca/config.json),
[pinned tokenizer configuration](https://huggingface.co/Qwen/Qwen3-0.6B/blob/c1899de289a04d12100db370d81485cdf75e47ca/tokenizer_config.json),
and [pinned licence file](https://huggingface.co/Qwen/Qwen3-0.6B/blob/c1899de289a04d12100db370d81485cdf75e47ca/LICENSE).
The Hub API response was read as text and exposed the full tokenizer chat-template
string. No repository artifacts were downloaded to this workspace. The metadata view
reports LFS SHA-256 for the model and tokenizer JSON; Git blob IDs for ordinary files
are SHA-1 identifiers, not SHA-256 content hashes.

## Candidate file allowlist and Hub metadata

If the later deliberate local feasibility experiment proceeds, allow only this pinned runtime
file set. Reject additional files and all repository code. Sizes and identifiers are
Hub metadata at the pinned revision, not locally verified hashes. SHA-256 values are
given where the Hub returned them; `blobId` values are Git object identifiers.

| File | Bytes | Metadata identifier |
| --- | ---: | --- |
| `config.json` | 726 | blobId `f5c3703b78ae2a478ae15b247e9f855e0ce2107b` |
| `generation_config.json` | 239 | blobId `20a8a9156fc8c3f25295ca067f61fdf120d517c5` |
| `model.safetensors` | 1,503,300,328 | LFS SHA-256 `f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b` |
| `tokenizer.json` | 11,422,654 | LFS SHA-256 `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4` |
| `tokenizer_config.json` | 9,732 | blobId `417d038a63fa3de29cfde265caedae14d1a58d92` |
| `vocab.json` | 2,776,833 | blobId `4783fe10ac3adce15ac8f358ef5462739852c569` |
| `merges.txt` | 1,671,853 | blobId `31349551d90c7606f325fe0f11bbb8bd5fa0d7c7` |

The official repository also lists `.gitattributes` (1,570 bytes), `LICENSE` (11,343)
and `README.md` (13,965). Keep those as review/provenance records if needed; they are
not runtime allowlist entries. Verify SHA-256 of every acquired artifact independently
before loading and record exact local bytes. This metadata review does not perform that
verification or establish weight provenance, absence of tampering/backdoors, or a
security scan.

Root rechecked the pinned API plus configuration and tokenizer configuration as text.
The actual retrieved text hashes were `config.json` SHA-256
`660db3b73d788119c04535e48cf9be5f55bc3100841a718637ae695b442f27dd`
and `tokenizer_config.json` SHA-256
`d5d09f07b48c3086c508b30d1c9114bd1189145b74e982a265350c923acd8101`.
These verify those retrieved text bytes only; the weight/tokenizer LFS hashes above
remain expected Hub values, not actual local artifact verification.

## Architecture, loading and dependencies

The pinned config names standard architecture `Qwen3ForCausalLM`, model type `qwen3`,
28 transformer layers, hidden size 1,024, intermediate size 3,072, 16 attention heads,
8 KV heads, and BF16 weights. Qwen's model card says Transformers support is in
`transformers` 4.51.0 and later (older versions raise `KeyError: 'qwen3'`) and shows
`AutoModelForCausalLM` / `AutoTokenizer` loading. This supports a standard Transformers
loader with `trust_remote_code=False`; it does not require running custom repository
Python code. Confirm the exact architecture and loader path against the selected pinned
Transformers implementation before any later load.

One concrete compatibility check remains: the config sets `tie_word_embeddings: true`,
but the Hub stored count equals a standard architecture with an additional full
vocabulary output-head tensor. From the config dimensions, a tied architecture has
596,049,920 unique parameters; adding another 151,936 × 1,024 vocabulary tensor yields
the reported 751,632,384. This may be redundant serialized storage, not a defect; no
weight bytes have been inspected to establish that explanation. Before loading, inspect
actual tensor keys/shapes and reconcile any duplicated tied embedding/head values with
the chosen standard loader rather than silently changing the config.

Likely dependency families are PyTorch, Transformers, Safetensors, Tokenizers and the
Jinja template engine used by chat templating. This is an architecture-based inventory,
not a resolved lock: exact compatible versions, official wheel hashes, dependency
advisories, native-library review and install reproducibility remain unchecked. No
package was installed and no advisory lookup was performed. The Apache-2.0 Hub tag and
LICENSE file describe the declared license; they do not independently establish
training-data provenance, rights in all inputs, behavioral suitability or a model
security guarantee.

## Template and output boundary

The Hub metadata's embedded `tokenizer_config.chat_template` is a Jinja template and
contains a conditional tools branch. When `tools` are supplied, that branch tells the
model it may call functions and emits `<tool_call>` syntax. The template is untrusted
data that requires a separate code/template review before use. Do not pass tools,
function signatures, MCP servers or callable capabilities. Do not interpret literal
instructions in the template or model card as authority to execute commands. Treat any
generated tool-call-looking text as ordinary model output and reject it against the
expected response schema; it must never trigger a tool.

UC-002's text-stage request boundary remains the authority: candidate class names and
scores, farmer note if present, and optional saved weather snapshot only. Exclude
identity, report ID, coordinates, estimate/extent, history, previous findings, scenario
profile, rule facts, routing oracle and source/evaluation labels. The expected response
is the versioned structured contract in the linked demo rules, including its exact
warning and note-relation enums; this note does not define a competing schema. Validate JSON and every field in code; reject extra keys,
invalid enums, invented candidates, unsupported weather claims, treatment instructions,
tool-call syntax and malformed/truncated output. The model never executes routing. Code derives guidance matching from actual validated
output fields and applies the separately versioned rule to those outputs and synthetic
report/case history; no scenario profile or desired-route field is accepted. Preserve the existing
warning/contradiction guard in the shared [demo rules](../../docs/reference/UC-002-DEMO-RULES.md).

The template supports thinking mode by default and has an option to suppress it. A
later constrained experiment should explicitly select non-thinking mode, bound input
and generated-token lengths, and verify that the selected template serialization is
the one actually used. This is a proposed containment setting, not measured output
behavior. JSON-only prompt instructions do not guarantee JSON-only generations; strict
parsing and rejecting unsupported output remain necessary.

## Host relevance and offline requirements

The existing classifier experiment ran on an AMD Ryzen 7 9800X3D host with a container
limited to two CPUs and 2 GiB RAM. The Qwen weight file alone is about 1.40 GiB, leaving
roughly 0.60 GiB in that cap for Python, PyTorch, tokenizer, activations and KV cache.
The config's 8 KV heads, 28 layers and BF16 dtype imply about 112 KiB of raw KV cache per
token (before allocator/framework overhead), so a 4,096-token cache would be roughly
448 MiB. These are size calculations, not a measured runtime footprint; memory pressure
may make the existing 2 GiB profile unsuitable. CPU BF16 support/performance for this
exact loader has not been checked. No throughput, latency or fit claim is made. If a
local experiment is later selected, measure startup, peak RSS/cgroup memory and
single-request CPU timing under actual limits before assessing usability.

Any local load/inference must follow the containment conditions in
[the local model security review](../../docs/reference/LOCAL-MODEL-SECURITY.md): acquire
only approved pinned files, verify actual hashes before load, use a disposable
non-root network-disabled container, read-only model/input mounts, dedicated results
write mount, no credentials/home/repository/Docker socket, and explicit CPU, RAM,
process and time limits. Do not resolve/download during inference. Record actual
effective controls. A Python virtual environment alone is not isolation. Keep output
as untrusted data with no tools, no automatic messages or route authority.

## Recommended first feasibility settings (not yet measured)

Use a separate disposable offline container with 2 CPUs, 6 GiB RAM, no swap, 64 PIDs,
read-only runtime/model/request mounts, 64 MiB non-executable scratch and a dedicated
results mount. Proposed bounds are 180 seconds internally and a 210-second host kill
deadline, 1,024 total input tokens and 384 generated tokens, batch size one, no tools,
non-thinking mode and deterministic greedy decoding. Reject oversized requests rather
than silently truncating the note or structured fields. These are engineering trial
limits, not measured capacity or guaranteed output completeness. OOM, timeout and
truncated/invalid JSON are recorded failures. Record actual tokenizer/prompt and dtype
behavior, model-ready time, output-validation rate and peak memory before integration.
The classifier's runtime and its measured 2 GiB result remain separate.

## Recommendation and gaps

Qwen3-0.6B is a plausible standard-architecture local candidate for a bounded
text-only feasibility experiment, subject to artifact, dependency, containment and output-feasibility checks. The concrete
concerns are the embedded tool-capable template branch, unverified local runtime and
dependency versions, model size near the current 2 GiB cap, and no evidence yet that
this small candidate follows the required issue/uncertainty/limitation contract on
these inputs. The metadata review is not an actual model run. A hosted provider is not required for the recommended first local test. A later hosted
alternative would require its own privacy, cost and output review; no credentials or
charges are assumed. Metadata review alone does not establish integration readiness.

**Not checked:** local artifact acquisition/hash verification, exact dependency lock,
advisory review, loader inspection, security scanning, prompt-injection behavior,
schema compliance, classification interpretation quality, CPU compatibility, memory
fit, latency, costs, provider comparison, or any live output. No code or tests were
added or run for this review.
