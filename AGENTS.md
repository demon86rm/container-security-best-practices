# Workshop Conventions

## Repository Purpose

A 90-minute, developer-focused workshop on container security best practices for
applications running on ROSA (Red Hat OpenShift on AWS), with a Digital Operational
Resilience Act (DORA) compliance angle. The audience is developers with little
OpenShift background. The course is 70% container best practices (12-Factor
applications, local tooling, UBI image building) and 30% security introspection
(SCC v2, RBAC, shift-left scanning and policy gates).

## Structure

- `documentation/` contains all AsciiDoc courseware content (Antora component)
- `documentation/modules/ROOT/pages/` contains the course pages in `.adoc` format
- YAML manifests live in the root step directories
- Step folders match page numbers (`NN-name/` next to `documentation/.../NN-name.adoc`):
  - `01-12factor-platform/` is the Go demo application (`main.go`, `go.mod`)
  - `02-secure-images/` holds the insecure and the secure Containerfile (build context is the repo root)
  - `03-scc-rbac/` holds the deployment, service, route, PDB, and RBAC manifests
  - `04-shift-left/` holds the CI gate script and the pipeline example
  - `05-secrets/` holds the External Secrets Operator install and SecretStore/ExternalSecret manifests
  - `06-network/` holds the NetworkPolicy manifests
- `myenv.sh.example` is the workshop variables template (copy to the gitignored `myenv.sh`)
- Steps are progressive: each builds on the previous one

## AsciiDoc Formatting

- Every numbered step must have a *What* and *Why* pair in bold
- Every step must have a collapsible verification block
- Use `[.console-input]` before source blocks for commands
- Use `[.console-output]` before source blocks showing expected output
- Reference YAML manifests by file path in `oc apply -f` commands
- Do not use em dashes. Use regular dashes (`-`) instead
- Use `'''` for horizontal rules between steps
- Cross-reference other pages with `xref:page.adoc[Label]`
- External links use `link:URL[Label]`
- Use `NOTE:`, `TIP:`, `IMPORTANT:`, `WARNING:` admonitions
- Product documentation links must point to `docs.redhat.com` or `docs.openshift.com`. Regulation, standards and non-Red Hat tool references (EUR-Lex, 12factor.net, vendor docs) are allowed and must be labelled as external
- Use attributes from `_attributes.adoc` for version numbers

## CLI Conventions

- Every `oc` command must include an explicit `--context rosa` flag and, when it touches a namespace, an explicit `-n $PROJECT` (or `-n $INTERNAL`)
- In bash/zsh snippets write `${var}` when a `:` follows a variable (zsh treats `$var:x` as a modifier)
- Show only real, captured command output; never fabricate output blocks
- Never use `oc login` inside step pages (only in `00-setup.adoc`)
- All workshop variables are exported once in `00-setup.adoc` and `myenv.sh`

## Content Rules

- Never include customer names, user names, or email addresses
- All content must be in English
- Prefer `registry.access.redhat.com` or `registry.redhat.io` images
- Use Red Hat / OpenShift-native components when they cover the use case
- Mention Red Hat products because they fit the solution, not to promote them
- DORA references use the article numbers from the mapping table in `index.adoc`

## YAML Conventions

- Every YAML file starts with a comment block: filename and purpose
- Use `app.kubernetes.io/part-of: demo-app` label consistently
- Include resource requests and limits on Deployments
- Include readiness and liveness probes where applicable