# Contained local interpreter experiment

Two offline Qwen3-0.6B trials completed. **The tooling ran within its controls, but all
12 responses failed the required output contract.** See [results](RESULTS.md) for
measurements, raw evidence, refactor review, validation scope and remaining gaps.
No application integration or agricultural correctness is established.

## Authority and boundary

- [Model manifest](model-manifest.json): official repository revision, seven allowed
  runtime artifacts, exact sizes/SHA-256, standard architecture and classifier classes.
- [Dependency lock](requirements.lock): all 39 tested Linux x86_64 / CPython 3.12
  distributions with official wheel hashes. The Dockerfile pins the Python base digest.
- [Demonstration rules](../../docs/reference/UC-002-DEMO-RULES.md): interpretation
  contract and selected image/note/optional-weather boundary. History remains in code
  and human review; missing issue links do not prove irrelevance. Interpreter agreement
  is not independent confirmation.
- [Local model security](../../docs/reference/LOCAL-MODEL-SECURITY.md): containment
  requirements; its earlier classifier review does not automatically clear this model.

The model is standard Qwen3ForCausalLM with verified local Safetensors and tokenizer
JSON. The loader does not use remote/custom code, pickle, upstream Jinja or tools.
A project-owned no-tools/non-thinking ChatML prompt is data for inference, not authority
to execute commands. Response JSON is strictly checked; structural validation does not
guarantee semantic truth, instruction adherence or safe agronomic interpretation.

## Scoped directories and deliberate execution

| Ignored repository location | Inference mount |
| --- | --- |
| `data/local-interpreter/model/` — seven verified artifacts only | Read-only `/model` |
| `data/local-interpreter/requests/` — allowlisted request JSON | Read-only `/requests` |
| `data/local-interpreter/wheels/` — verified build dependencies | Not mounted at inference |
| `runs/local-interpreter/` — selected run outputs/inspection | Writable `/results` |

No repository, home, app database, credentials, Docker socket or scoring-label manifest
is mounted. Acquire pinned files and dependency wheels separately from inference;
verify before load and again inside the container. Nothing is installed in app `.venv`.

```bash
python3 experiments/local-interpreter/verify_artifacts.py data/local-interpreter/model
docker build --network none \
  --build-context wheels=./data/local-interpreter/wheels \
  -t coffee-interpreter-experiment:2026-11-10 experiments/local-interpreter
docker image inspect coffee-interpreter-experiment:2026-11-10
python3 experiments/local-interpreter/launch.py sha256:REPLACE_WITH_INSPECTED_LOCAL_IMAGE_ID
```

Inspect the image and supply its full immutable ID. The launcher supplies the non-root
host UID/GID, refuses existing services/results and automatic pulls, checks actual
Docker configuration before starting, records state/logs and removes only its container.
The runner verifies effective containment before loading. Controls: 2 CPU, 6 GiB RAM,
no swap, 64 processes, read-only root, zero capabilities, no new privileges, seccomp,
network none, 64 MiB non-executable scratch, 180-second internal/210-second host deadline.

The request file has `cases`, each with a neutral `id` and `request` containing only
`scores`, `farmer_note` and `weather`. The ID is never sent to the model. Prompt input
is limited to 1,024 tokens, generation to 384, greedy decoding and batch size one.
Progress/raw outputs are preserved per case, including invalid outputs and errors.
`completed` is generation completion; read `validation_errors` separately.

Retain a unique image tag for every trial and capture runtime-file hashes at launch;
the retired first image could not be inspected later, as disclosed in the results.
Before another trial, preserve the preceding raw captures, exact prompt and requests
under a new local trial directory, verify their hashes, and deliberately clear only the
active result path. Never silently overwrite evidence or repair generated fields.
The two existing trial directories and selected evidence preserve both prompt versions.

## Checks

```bash
.venv/bin/python -m pytest tests/unit/test_interpreter_protocol.py tests/unit/test_interpreter_guards.py -q
bash scripts/test.sh
```

Ordinary tests use synthetic fixtures without model packages, weights, network or paid
calls. Live generation is deliberate and separate. The [results record](RESULTS.md)
contains actual checks and the independent validation disposition. UC-002's application
journey remains unfinished even when experiment-tooling checks pass.
