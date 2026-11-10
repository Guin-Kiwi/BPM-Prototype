# First contained classifier run — 10 November 2026

## Outcome

The pinned classifier loads and runs within the selected local CPU/memory limits.
This establishes technical feasibility on this machine. It does **not** select a
provider for UC-002 or establish diagnostic accuracy, calibrated confidence or security
clearance. A blank white image received a Rust score of 78.11%; simple perturbations
changed one leaf's leading class. Do not use these scores to authorize routine advice.

[Selected run evidence](evidence/first-run.json) contains every score vector, individual
timing, installed version, input/artifact hash and effective containment measurement.
[Dependency evidence](evidence/dependency-review.json) records official wheel sources,
digest checks, advisory results and hashes of reviewed loader files. Raw local captures
remain in ignored `runs/local-classifier/`; the selected evidence names the raw run hash.
No model weights or images are committed or redistributed.

## Execution and integrity

Baseline: merged main `c1b0162`; experiment tooling: `81a94cf`. The model's pinned
revision/files/class order remain governed by [the manifest](model-manifest.json).
The actual configuration and 98,953,966-byte weight file passed the standard-library
verifier before loading and again inside the offline container.

A 33,816-byte bounded header and the maintained Safetensors parser identified 344 F16
tensors. Every key and shape matched the explicitly instantiated standard ConvNeXt-Small.
The head is `[7, 768]` plus `[7]` bias, matching the top-level seven-class configuration;
the nested 1,000-class metadata did not set the runtime head. All weights were finite,
and strict loading into the FP32 CPU architecture succeeded without key remapping.

Only local `safetensors.torch.load_file(..., device="cpu")` loads weights. Review of the
locked timm architecture/builder confirmed `pretrained=False` bypasses pretrained
acquisition. No `hf-hub:` name, publisher loader, `torch.load`, remote/custom code,
pickle, TorchScript or fallback format is used.

The model card attributes the classifier to “Multi-crop disease models, IXR
(agritechixr)” under CC BY 4.0. Preserve that attribution and the nested Apache-2.0
notice; training-data provenance and licence reconciliation before redistribution
remain unresolved. BRACOL image attribution and source hashes remain in
[the existing example reference](../../docs/reference/EXAMPLE-IMAGES.md).

## Dependencies and containment

The complete [28-distribution lock](requirements.lock) matches the installed inventory
exactly. CPU torch 2.14.1+cpu and torchvision 0.29.1+cpu use the official
[PyTorch CPU distribution](https://pytorch.org/get-started/previous-versions/); other
wheels use PyPI. Each wheel's SHA-256 matched the corresponding official index digest.
Exact-version PyPI vulnerability metadata returned zero advisories for each distribution
on the check date (CPU suffix removed only for advisory lookup). This is a bounded
source check, not a comprehensive vulnerability audit or clean-scan verdict. Base OS,
kernel and native-library vulnerabilities were not independently scanned.

The [upstream timm loader change](https://github.com/huggingface/pytorch-image-models/pull/2679)
reinforces why checkpoint deserialization needs review. The experiment bypasses that
checkpoint path entirely. [Safetensors security information](https://github.com/safetensors/safetensors/security)
does not establish safety of weights, downstream processing or native dependencies.

The runtime was built with networking disabled from hash-locked wheels and the pinned
official Python base digest in the Dockerfile. `pip check` passed. Smoke: Python 3.12.16.
The final inspected local image ID is:

```text
sha256:a54cb8436f88cd39f8b34fd6cdbac38e824518e78f069f5b3a56103dadfab368
```

Before start, Docker inspection matched the immutable image, UID/GID 1000:1000,
`network_mode: none`, read-only root, exact three bind mounts, dropped capabilities,
no added devices/capabilities, private IPC, no host PID namespace and disabled privilege
escalation. Inside the running container, before loading:

| Effective control | Observed evidence |
| --- | --- |
| Identity / privileges | UID/GID 1000:1000; CapEff=0; NoNewPrivs=1; seccomp filter mode 2 |
| Network | Only loopback interface; Docker network mode `none` |
| Mounts | `/`, `/model`, `/inputs` read-only; `/results` writable |
| CPU | cgroup quota/period = 2 CPUs; torch uses two compute threads |
| RAM / swap / processes | 2 GiB memory maximum; zero swap allowance; 64-process limit |
| Scratch | 64 MiB tmpfs; noexec, nosuid, nodev |
| Time | Internal 180-second alarm; host 210-second kill deadline |

The daemon reports AppArmor, built-in seccomp and cgroup namespaces. Container exit
was 0, with no OOM kill; the launcher removed its container. No application database,
repository, home, credentials, Docker socket or source-label metadata was mounted.
These checks reduce exposure; they do not prove complete kernel/runtime isolation.

Initial commands from the restricted agent sandbox could not reach Docker or resolve
package hosts. Host terminal checks and subsequent reviewed execution succeeded.
No Docker permissions or host configuration were changed to obtain access.

## Actual performance

Host: AMD Ryzen 7 9800X3D, x86_64 Linux; container restricted to two CPUs. These are
single-process, warmed CPU timings on this machine, not a load/concurrency benchmark.

| Measurement | Actual result |
| --- | --- |
| Imports + initial preflight | 1.263 s |
| Architecture creation + header validation | 0.216 s |
| Tensor load + finite check + strict assignment | 0.049 s |
| Startup to model ready | 1.528 s |
| One untimed-for-comparison warmup forward | 0.080 s |
| 84 measured forwards, excluding image preprocessing | median 77.07 ms; range 76.62–78.31 ms |
| Entire experiment inside runner | 8.126 s |
| Peak process RSS | 660,028 KiB (644.6 MiB), Linux `getrusage(RUSAGE_SELF).ru_maxrss` |
| Peak cgroup memory | 517,206,016 bytes (493.2 MiB), cgroup v2 `memory.peak` |

RSS and cgroup values use different accounting, including shared/mapped pages; they
are separate observations. No single universally applicable memory requirement is
inferred. Container startup, image build and acquisition are outside the runner timing.

## Inputs, preprocessing and behavior

All three staged JPEGs matched their source hashes. No reports, histories, locations,
identities, prior findings, notes, source-label metadata or weather entered the model.
The callable sees only normalized image tensors. The separate score/provenance record
is experiment output, never an input to another assessment stage.

The pinned [model card](https://huggingface.co/ixrbhii/coffee-disease-convnext/blob/95275230cb1a2490f5380a123d7808c9bb7f8718/README.md)
describes direct 224×224 resizing during training, while its example and config use
resize plus center crop. Both interpretations were tested explicitly because the
512×256 examples are rectangular. Config mode resizes the shorter side to 224 then
center-crops; direct mode resizes both dimensions to 224. Both use RGB, bilinear
interpolation, antialiasing and the config's ImageNet mean/std. Preprocessing remains
a sensitivity to resolve before an application adapter is chosen.

Leading scores for unperturbed images and unsupported-input controls:

| Input | Config center crop | Card direct resize |
| --- | --- | --- |
| `sample-01.jpg` | Healthy 88.17% | Healthy 89.83% |
| `sample-02.jpg` | Rust 43.53% | Rust 76.43% |
| `sample-03.jpg` | Rust 90.77% | Rust 94.28% |
| `blank` | Rust 78.11% | Rust 78.11% |
| `non-coffee` | Phoma 20.83% | Phoma 20.83% |

For each of the three leaves, variants were rotation by 15° with white fill, brightness
multiplied by 0.5, and Gaussian blur radius 2. Each of the 28 image/variant/preprocessing
combinations ran three times after warmup. Every output was finite, seven-dimensional,
in [0,1] and summed to one within tolerance. Repeated score vectors were identical in
this run; that does not establish portability across machines/library versions.

For sample-02 with center crop, the top class changed from Rust (43.53%) to Phoma after
dimming (55.15%) or blur (46.89%). Direct resize retained Rust across those variants,
but its original Rust score was 76.43%. The other two leaves retained their leading
classes under the tested perturbations. Source-label indicators remain separately
inspectable; this tiny, selected set has no established independent reference truth
for scoring diagnostic accuracy or detecting training overlap.

White blank and non-coffee geometric images both produced ordinary class distributions.
The blank's high Rust score demonstrates missing invalid-input/abstention behavior;
a high softmax score is not evidence of a coffee leaf or disease. The geometric control
is synthetic and supplies no coverage of real non-coffee photographs. No threshold,
confidence calibration or backdoor absence is established by this experiment.

## Verification and next action

TDD: the new experiment checks failed collection before the gate module existed, then
33 new cases passed. Combined artifact/runtime checks: 41 passed. `bash scripts/test.sh`
passed lifecycle checks/scenarios, 47 process tests and 73 pytest tests. Tests require
no model installation, network or live inference. Runtime inventory/lock comparison,
actual artifact verification, 41 local document links and `git diff --check` also passed.

The final check exposed a lifecycle-fixture cleanup failure: scenario setup copied
ignored read-only model directories. A separate regression test reproduced the warnings
and retained copies. Excluding root `data/` and `runs/` fixed it; the final full run had
no cleanup warnings, and this session's temporary duplicate artifacts were removed.

Application integration remains deferred. Review provider suitability, preprocessing,
unsupported-input handling and independent evaluation evidence before selecting an
adapter. UC-002 routing/guidance and the second model remain open. Weather acquisition
may now be checked separately under the preserved
[event-weather decisions](../../docs/reference/EVENT-WEATHER.md); none was fetched in
this classifier run. This result changes no weather variables, time window, history
boundary, DMN definitions or application behavior.
