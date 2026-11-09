# Local classifier experiment preparation

Prepare a contained CPU-only feasibility experiment, separate from the running
prototype. This folder contains a manifest, sandbox configuration and a standard-library
artifact verifier. There is no runtime image, downloader, inference runner, installed
model dependency or model weight. No model runs today.
The active application remains governed by [UC-002](../../docs/specs/UC-002-ASSESSMENT-HANDOFF.md);
this supporting preparation does not select DEVELOP for that use case.

## Inputs and boundaries

[model-manifest.json](model-manifest.json) is the machine-readable authority for the
pinned repository revision, allowed artifact names, expected hashes and class order.
It records the distinction between inspected configuration and unverified weights.
The [security review](../../docs/reference/LOCAL-MODEL-SECURITY.md) owns the risk
assessment and containment requirements. Do not run the publisher's example loader
unchanged: avoid remote code, automatic downloads or fallback checkpoint formats.

Local directories, all already ignored by Git:

| Location from repository root | Purpose | Container access |
| --- | --- | --- |
| `data/local-classifier/model/` | Only verified config and Safetensors weights | Read-only `/model` |
| `data/local-classifier/inputs/` | Explicitly staged neutral-name image copies only | Read-only `/inputs` |
| `runs/local-classifier/` | Selected experiment's local output | Writable `/results` |

Do not mount the repository, home, credentials, Docker socket, application database
or source-label manifest. [Existing BRACOL examples](../../docs/reference/EXAMPLE-IMAGES.md)
are candidate technical inputs, not an accuracy evaluation set. Match their recorded
hashes when staging; do not generate or import another dataset for this experiment.

## Artifact verification command

After tomorrow's explicitly authorised download, from repository root:

```bash
python3 experiments/local-classifier/verify_artifacts.py data/local-classifier/model
```

This uses the versioned manifest, rejects absent/extra files, symlinks, mismatched
sizes/hashes, class-order changes and custom-loading configuration. It never imports
model libraries or interprets weight bytes as tensors. Keep the folder read-only and
verify again inside the eventual container before loading to reduce file-replacement
risk. A passing hash check proves correspondence to the recorded artifact, not
publisher trust, tensor-parser safety or absence of poisoning.

## Sandbox configuration

[compose.yaml](compose.yaml) disables networking, runs as an explicitly supplied
nonzero host user, drops capabilities, blocks privilege escalation, uses a read-only
root filesystem and limits CPU, RAM/swap, processes and scratch space. Bind mounts
must exist; Compose will not silently create them. No image is pulled automatically.
Use an inspected immutable local image ID (`sha256:…`), not a moving registry tag.
The nonzero UID and immutable image policy need verification at run time; Compose
requires values but does not validate their contents.

The current command prints the Python version only. It is an intended runtime smoke
check, not a model benchmark. Runtime build/runner implementation, an enforced wall-
time limit and isolation verification remain tomorrow's work. A container reduces
exposure but is not proof of complete isolation or harmless model behavior.
[Docker service reference](https://docs.docker.com/reference/compose-file/services/)
documents the configured controls.

## Tomorrow: ordered handoff

1. Re-read the security review and manifest. Check exact CPU-only dependency versions,
   their official sources and known advisories. Resolve label/head config mismatch and
   explicit preprocessing before using results. No complete lockfile is claimed today.
2. Prepare a minimal runtime image with pinned base digest and dependency versions;
   record the installed inventory and final local image ID. Keep acquisition/build
   separate from offline inference; no model weights or credentials in the image.
3. Download only manifest-listed artifacts from URLs formed with the pinned revision.
   Run the artifact verifier before loading. Inspect bounded tensor headers
   and shapes with a maintained parser; refuse unexpected files or pickle fallbacks.
4. Stage the verified image examples and create the three scoped directories. Set
   `COFFEE_RUN_UID` to `id -u` (must not be 0), `COFFEE_RUN_GID` to `id -g`, and
   `COFFEE_MODEL_IMAGE` to the inspected local image ID. Check the resolved Compose
   configuration and run the smoke command with no automatic pull.
5. Add a reviewed runner to the runtime image; explicitly instantiate the standard
   architecture, load only local Safetensors and use the manifest class order.
   Enforce a wall-time limit inside the container and verify the sandbox's effective
   user, mounts and network before loading. Start offline inference only then.
6. Record model/config/image hashes, runtime inventory, preprocessing, actual controls,
   load/inference timing, memory-measurement method, class scores and failures. Include
   blank/non-coffee/perturbed inputs; technical feasibility does not establish diagnostic
   accuracy, calibrated confidence or absence of a backdoor. No routing/weather work.

## Checks completed today

Docker 29.7.2 and Compose v5.4.0 are installed. A read-only daemon query reported
AppArmor, built-in seccomp and cgroup namespaces. Access from the agent's normal
sandbox was denied; the read-only query succeeded with execution approval. No Docker
permissions were changed and no containers/images were created or pulled.

Completed checks: `docker compose ... config --format json` parsed the configuration
using dummy image/user values; inspection of that output confirmed the declared
network, mount, non-root example user, resource and privilege controls. The manifest
matches the previously retrieved Hub metadata and inspected config hash. Eighteen
local document links resolve.

TDD: eight artifact-verifier checks failed before implementation and passed afterwards.
`bash scripts/test.sh` passed lifecycle checks/scenarios, 46 process tests and 40 pytest
tests. `git diff --check` passed. All verifier test artifacts are temporary synthetic
bytes; no actual weights are loaded. The checker verifies integrity only.

The independent configuration review identified nonzero UID/immutable image validation
as run-time prerequisites; they remain explicit in the ordered handoff. Effective
runtime isolation, dependency compatibility, tensor parsing and model loading remain
unverified until that experiment is performed.
