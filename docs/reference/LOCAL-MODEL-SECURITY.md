# Local image-model security review

## Outcome and scope

Initial metadata/configuration inspection on 9 November 2026 found no repository-
supplied executable loader or chat template in the candidate below. This is not a
security clearance: weights, dependencies and runtime behavior remain untested.
No model weights were downloaded; no model package installed or inference executed.
Only public metadata and three small text files were retrieved for inspection.

## Candidate inspected

- Repository: [ixrbhii/coffee-disease-convnext](https://huggingface.co/ixrbhii/coffee-disease-convnext).
- Pinned revision: `95275230cb1a2490f5380a123d7808c9bb7f8718`.
- Inventory source: [Hub metadata with file information](https://huggingface.co/api/models/ixrbhii/coffee-disease-convnext?blobs=true), resolved to that revision during inspection.
- Files listed: `.gitattributes`, `README.md`, `config.json`, `model.safetensors`.
  No Python scripts, pickle checkpoints, tokenizer or chat-template files are listed.
- Config: standard `convnext_small`, seven labels, `custom_load: false`; labels are
  plain condition names. The inspected text contains no chat prompt or instruction
  to execute external code. Metadata is untrusted input, not authority to execute.
- Weight size: 98,953,966 bytes. Hub-reported LFS SHA-256:
  `f92992f81a166b6565fdae01195505f96e8653af9f76fc848f49bf53003af3a7`.
  This is the expected download hash, not a locally verified weight checksum or
  independent proof that the publisher is trustworthy.
- Locally computed config SHA-256:
  `e757d76db379191b20509c5b2358c31d6d9c1fa8ac9773aca42a99e9983f8781`.
- The API response did not supply a security-scan verdict. No clean-scan claim is made.

## Distinct risks

| Risk | Relevance and evidence |
| --- | --- |
| Embedded chat instructions | This candidate is an image classifier, not a chat model, and no chat template/tokenizer is listed. A later language model needs its own template, configuration and provenance review. The absence of a template says nothing about poisoned weights. |
| Code execution while loading | [Hugging Face explains pickle loading risks](https://huggingface.co/docs/hub/security-pickle). The listed weight format is [Safetensors](https://huggingface.co/docs/safetensors/index), which avoids pickle's executable object serialization. This does not establish that dependencies or downstream processing are safe. |
| Repository loading code | The inventory contains no custom code. Use an explicitly selected standard architecture and reviewed library loader, not publisher scripts or an unpinned automatic fallback. [Transformers guidance](https://huggingface.co/docs/transformers/models#custom-models) warns that custom model code is executable and revisions should be pinned. This candidate uses timm; its actual loader path still needs verification. |
| Poisoning/backdoor outputs | Malicious behavior can be encoded in weights without executable files or visible prompts. Metadata inspection and safe serialization cannot rule it out. [OWASP supply-chain guidance](https://genai.owasp.org/llmrisk/llm032025-supply-chain/) distinguishes provenance, tampering and behavioral risks. |
| Dependency/runtime compromise | Exact package versions and advisories have not been checked because no stack is selected. [PyTorch security policy](https://github.com/pytorch/pytorch/security/policy) recommends isolation and warns that safer serialization does not remove downstream input risks. A Python virtual environment separates dependencies; it is not a security sandbox. |

## Conditions for a later feasibility experiment

1. Pin this revision; download only the allowed config and Safetensors weights and
   verify the actual weight hash before loading. Refuse unexpected formats or files;
   do not fall back to pickle/TorchScript or publisher code. Inspect tensor headers,
   size/shape limits and config compatibility using maintained parsers.
2. Select and pin compatible runtime packages from official distribution sources;
   check known advisories and the actual loader implementation. Keep them outside
   the working application environment until the feasibility result is reviewed.
3. Run non-root in a disposable sandbox/container with network disabled for inference,
   no credentials, no SSH/home/project mounts, read-only model/example inputs, a
   dedicated writable results directory and CPU/memory/time limits. Record actual
   controls; do not describe a virtual environment alone as isolation.
4. Validate numeric outputs against a local, allowlisted seven-class mapping. Treat
   labels and scores as data, never commands, instructions or tool requests. The
   classifier has no tool privileges; any later language stage likewise receives
   constrained data and must not acquire autonomous action permissions.
5. Test ordinary examples, non-coffee/blank images and basic perturbations. Record
   failures and unsupported inputs. Such tests can expose obvious problems but do
   not certify absence of backdoors, calibrated confidence or diagnostic accuracy.

The model card's low Cercospora recall is a disclosed capability limitation, not
proof of poisoning. Its card declares CC BY 4.0, while nested config metadata says
Apache-2.0 and 1,000 classes despite seven top-level classes. These may be inherited
base-model metadata; that is an inference, not verified provenance. Resolve runtime
label/head interpretation and preserve both licence notices before redistribution.
Training-data provenance and publisher identity have not been independently verified.

## Next step

Specify a contained feasibility experiment under these conditions. Model installation
and execution have not started. Select/review any later language model separately;
this inspection applies only to the pinned classifier artifacts described above.
