# Container Security Best Practices for Developers on OpenShift

A 90-minute, developer-focused workshop on building, running, and gating secure
container images on Red Hat OpenShift (reference platform: ROSA), with a Digital Operational
Resilience Act (DORA) compliance angle. Built as a Red Hat Scholars courseware
site with AsciiDoc and Antora.

The course is 70% container best practices (12-Factor applications, `podman`
local tooling, Red Hat UBI and Hardened Base Images, multi-stage Containerfiles)
and 30% security introspection (rootless execution, SCC v2, RBAC, shift-left
CVE scanning and policy gates with `roxctl`), plus secrets with the External Secrets Operator and network isolation of internal versus external applications.

## View the Course

The full course is published at: https://demon86rm.github.io/container-security-best-practices

## Local Development

To preview the course site locally:

The reliable way (the local Node-based build can hang on very new Node versions) is the Antora container image:

```bash
podman run --rm -v "$PWD":/antora:Z -w /antora docker.io/antora/antora antora generate --stacktrace site.yml
```

The generated site is output to `gh-pages/`. With a compatible Node version, `npm install && npm run dev` starts a live-reload server at http://localhost:3000.

## Repository Structure

| Directory | Purpose |
|---|---|
| `documentation/` | Antora courseware source (AsciiDoc pages, navigation, attributes) |
| `01-12factor-platform/` | Go demo application (Step 1) |
| `02-secure-images/` | Insecure and secure Containerfile (Step 2) |
| `03-scc-rbac/` | Deployment, service, route, PDB, and RBAC manifests (Step 3) |
| `04-shift-left/` | CI gate script and pipeline example (Step 4) |
| `05-secrets/` | External Secrets Operator install, SecretStore and ExternalSecret manifests (Step 5) |
| `06-network/` | NetworkPolicy manifests for internal and external applications (Step 6) |
| `myenv.sh.example` | Workshop variables template |
| `supplemental-ui/` | Custom UI overrides for the Antora site |

## Prerequisites for the Hands-On

- An OpenShift cluster (tested on ROSA) and `oc` CLI access to it (see [Cluster Setup](https://demon86rm.github.io/container-security-best-practices/00-setup.html))
- `podman`, `oc`, `curl` and `envsubst` on the workstation (no Go needed)