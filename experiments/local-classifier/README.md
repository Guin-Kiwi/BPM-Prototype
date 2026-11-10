# Contained local classifier experiment

The first CPU-only feasibility run completed on 10 November 2026. See
[results and limits](RESULTS.md) and [selected measurements](evidence/first-run.json).
The experiment has its own runtime; it installs nothing into the application environment.
[UC-002](../../docs/specs/UC-002-ASSESSMENT-HANDOFF.md) remains in SPECIFY, with provider
selection and application integration open.

## Requirements and boundaries

The [security review](../../docs/reference/LOCAL-MODEL-SECURITY.md) owns containment
conditions. [model-manifest.json](model-manifest.json) owns the pinned repository
revision, allowed artifact names, sizes, hashes and seven-class order.
[requirements.lock](requirements.lock) pins the complete tested Linux x86_64 / CPython
3.12 wheel set, including hashes. [Dependency review](evidence/dependency-review.json)
records official sources and the exact-version advisory lookup.

Only image tensors reach the classifier. No reports, histories, identities, earlier
findings, source labels, farmer notes or weather are model inputs. Existing
[event-weather decisions](../../docs/reference/EVENT-WEATHER.md) are preserved;
weather acquisition is a separate next check. No second model, routing or application
integration runs here.

| Ignored location from repository root | Purpose | Inference container access |
| --- | --- | --- |
| `data/local-classifier/model/` | Verified config and Safetensors weights only | Read-only `/model` |
| `data/local-classifier/inputs/` | Three verified neutral-name JPEG copies only | Read-only `/inputs` |
| `data/local-classifier/wheels/` | Hash-verified build dependencies | None |
| `runs/local-classifier/` | Local measurements and runtime inspection | Writable `/results` |

Do not mount the repository, home, credentials, Docker socket, application database
or source-label manifest. [Existing BRACOL examples](../../docs/reference/EXAMPLE-IMAGES.md)
are technical inputs with recorded hashes, not an accuracy evaluation set. Do not
import another dataset. Blank and geometric non-coffee controls are generated in memory.

## Acquire and build separately from inference

Acquire only the two manifest-listed model files using its pinned-revision URL pattern.
Verify before parsing, and again inside the inference container:

```bash
python3 experiments/local-classifier/verify_artifacts.py data/local-classifier/model
```

Stage byte-identical copies of the three existing JPEGs; compare both source and staged
SHA-256 hashes with the example-image reference. Keep model/input files and directories
read-only on the host. The verifier rejects absent/extra files, symlinks, mismatched
sizes/hashes, class-order changes and custom-loading configuration. Integrity proves
correspondence to the recorded artifact, not trust or absence of poisoning.

Use the official PyTorch CPU index and PyPI to acquire the locked wheels in a disposable
acquisition environment. Require hashes and binary wheels; never install into `.venv`:

```text
python -m pip download --only-binary=:all: --require-hashes \
  --index-url https://pypi.org/simple \
  --extra-index-url https://download.pytorch.org/whl/cpu \
  -r requirements.lock --dest /wheels
```

The initial resolution used torch 2.14.1+cpu, torchvision 0.29.1+cpu, timm 1.0.31,
Safetensors 0.8.0 and Pillow 13.0.0. Every resolved wheel was independently compared to
its official index digest; all transitive versions are captured in the lockfile.
Recheck advisories when acquiring again. The Dockerfile pins the official Python base
digest and installs from these wheels with networking disabled:

```bash
docker build --network none \
  --build-context wheels=./data/local-classifier/wheels \
  -t coffee-classifier-experiment:2026-11-10 experiments/local-classifier

docker image inspect coffee-classifier-experiment:2026-11-10
```

The allowlisted build context contains only runtime files. No weights, images or
credentials enter the image. Inspect and record the actual local immutable image ID;
a rebuild can have a different ID.

## Run deliberately

Docker access and internet acquisition require execution access outside some agent
sandboxes. A successful host terminal check does not establish that agent access works.
No Docker permissions need to change when reviewed execution already provides access.

Use `id -u` / `id -g` for `COFFEE_RUN_UID` / `COFFEE_RUN_GID`, and the inspected full
`sha256:…` image ID for `COFFEE_MODEL_IMAGE`, to resolve Compose configuration and run a
smoke command before inference:

```bash
export COFFEE_RUN_UID="$(id -u)"
export COFFEE_RUN_GID="$(id -g)"
export COFFEE_MODEL_IMAGE=sha256:REPLACE_WITH_INSPECTED_IMAGE_ID
docker compose -f experiments/local-classifier/compose.yaml config --format json
docker compose -f experiments/local-classifier/compose.yaml run --rm --no-deps \
  --pull never classifier python --version
python3 experiments/local-classifier/launch.py sha256:REPLACE_WITH_INSPECTED_IMAGE_ID
```

[launch.py](launch.py) supplies its own UID/GID and sanitizes the environment, refuses
existing service containers/results, creates without pulling, then validates actual
Docker inspection against the expected image, resources, privileges and exact three
bind mounts **before starting**. It saves inspection/state/logs locally and removes
its own container on exit. Host supervision kills the container after 210 seconds.

[run.py](run.py) checks effective user, read-only mounts, loopback-only networking,
capabilities, seccomp, privilege-escalation prevention and cgroup limits before loading.
An internal 180-second alarm covers preflight, imports and inference. It re-verifies
artifacts, bounds the tensor header, checks all Safetensors keys/dtypes/shapes against
the standard seven-class architecture, checks finite weights and loads strictly.
There is no Hub loader, custom code, pickle fallback or tool access.

The runner checks both documented preprocessing interpretations, three repeats of
original/rotated/dimmed/blurred examples and blank/geometric controls. It records every
seven-class score vector, timings, memory methods, hashes and installed versions in
`runs/local-classifier/first-run.json`. Failures are recorded as failures. Before a
rerun, deliberately preserve the preceding local outputs separately; never silently
overwrite evidence. New inputs or a changed runtime require their own review and run.

## Validation

Ordinary tests use synthetic metadata and do not load/download model weights:

```bash
.venv/bin/python -m pytest tests/unit/test_classifier_experiment.py tests/unit/test_model_artifact_verification.py -q
bash scripts/test.sh
```

The [results record](RESULTS.md) owns actual run findings and check outcomes. Passing
these gates does not certify diagnostic accuracy, confidence calibration or complete
isolation from all kernel/runtime vulnerabilities.
