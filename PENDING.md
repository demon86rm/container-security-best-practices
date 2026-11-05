# Pending points

Open items that need something from outside this repository (a cluster, an account, a decision). Everything else in the workshop has been run and verified on ROSA 4.22; the summary of what was verified is at the bottom of this file.

## Needs an environment or account

| # | Item | What is needed | How to close it |
|---|---|---|---|
| 1 | Step 4: run the real gate | A cluster with RHACS Central (the owner has one) | See the runbook below. Then replace the "no Central" wording in `04-shift-left.adoc` with captured output |
| 2 | Step 5: AWS Secrets Manager store | An AWS account, an IAM role trusted by the cluster's OIDC provider with `secretsmanager:GetSecretValue` on one secret, a ServiceAccount annotated with the role | Apply `05-secrets/secretstore-aws.yaml` (set role ARN annotation and region), point `externalsecret.yaml` at the store, confirm `SecretSynced`; update the status line in Step 5 |
| 3 | Step 5: Azure Key Vault store | A Key Vault, a secret, and a service principal with `get` on secrets (or workload identity federation) | Create the `azure-sp-credentials` Secret, apply `05-secrets/secretstore-azurekv.yaml`, confirm `SecretSynced` |
| 3b | Step 5: HashiCorp Vault store | A Vault server with KV v2, Kubernetes auth enabled, a role `demo-app` bound to ServiceAccount `vault-reader` and the project, a read policy on one path | Edit `server` in `05-secrets/secretstore-vault.yaml`, apply, point `externalsecret.yaml` at store `vault`, confirm `SecretSynced` |
| 4 | Link check | A browser or network path that docs.redhat.com does not block (it returns 403 to `curl`) | Open every `link:` URL once; page paths were confirmed by search only |
| 5 | Red Hat Hardened Images names | The current catalog (registry path and image names) | Add one verified example image to Step 2, section 6 |
| 10 | Validate on OpenShift 5.0 | The owner's 5.0 cluster (single control-plane node plus one worker, ACS installed) and a kube context | Rename it to `workshop`, check the registry `managementState` and node arch, run the page commands, record SCC and External Secrets differences in the pages, then update `ocp-version-tested` |

## Needs a decision

| # | Item | Notes |
|---|---|---|
| 6 | DORA mapping validation | No compliance team available. The mapping is built from the Regulation text; check each row against the Regulation (EUR-Lex 2022/2554) and Delegated Regulation 2024/1774, or the supervisor's guidance, before citing it to an auditor |
| 7 | Out-of-scope extras | Instructor run-sheet, image signing/verification (cosign or Red Hat Trusted Artifact Signer), runnable local scanner (syft/grype or trivy), "what to do Monday" page. Declined for now |
| 8 | Local `npm run dev` | Hangs on Node 26 with Antora 2.3.4. Use the container build; fix needs a Node 18/20 toolchain or an Antora upgrade |
| 9 | Publishing | Nothing is pushed. The GitHub Pages site builds in CI after the owner pushes |

## Runbook: close item 1 (Step 4 against your Central)

1. In Central, create an API token with the **Continuous Integration** role. Keep it out of Git.
2. Export `ROX_ENDPOINT` (host:port of Central) and `ROX_API_TOKEN`.
3. Image to scan: the image built in Step 2, for example the internal registry reference
   `image-registry.openshift-image-registry.svc:5000/$PROJECT/demo-secure:latest`.
   RHACS scans it if the cluster's internal registry integration is enabled; otherwise add a registry integration in Central or use an externally reachable reference.
4. `export IMAGE=...` and `export MANIFESTS=03-scc-rbac/deployment.yaml`, then `./04-shift-left/rox-ci-gate.sh`.
5. Expected: reports in `rhacs-reports/` (`image-scan.csv`, `sbom.spdx.json`, `*.junit.xml`); exit 0 when no enforced policy is violated.
6. Try to break it: set the insecure image as `IMAGE` and a `deployment-root.yaml` manifest, confirm exit 1, then paste the real console output into Step 4.

## What was verified (so nobody redoes it)

- Antora container build: one benign warning (`home` layout); all internal links and anchors resolve.
- ROSA 4.22.19, end-to-end run of the page commands in zsh: 303 s total. SCC refusal, UID assignment, pod kill under traffic (30/30 `200` once the Route is warm), RBAC 403, External Secrets (fake provider) sync and rotation (about 70 s to the running pod), NetworkPolicy matrix.
- Containerfiles build for `linux/amd64`: secure 29.5 MB, insecure 1.02 GB.
- `rox-ci-gate.sh` logic with a stand-in `roxctl`: exit 0 on pass, exit 1 when the image check or the deployment check fails, reports always written. Not yet run against a real Central.
