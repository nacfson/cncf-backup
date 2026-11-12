# CNCF Graduated Projects Documentation Backup

Consolidated, version-pinned documentation corpus covering **all 26 CNCF Graduated projects** across 7 architectural layers, structured for learning, offline reference, and Retrieval-Augmented Generation (RAG).

## Corpus Summary

- **Last synced (UTC):** `2026-11-12T02:09:55Z`
- **Backup scope:** `text-svg` (prose docs + config/code examples + vector `.svg` architecture diagrams; latest stable version per project)
- **Total projects:** `26` (synced from `31` upstream GitHub repositories)
- **Total files:** `8,759` (`6,453` Markdown/MDX, `831` reStructuredText, `882` YAML/JSON/code examples, `513` SVG diagrams)
- **Uncompressed corpus size:** `85.21 MB`

## Directory Layout

```text
cncf-backup/
├── docs/
│   ├── orchestration-core/   # Kubernetes, etcd, containerd, CoreDNS, KubeVirt, Karmada
│   ├── networking-mesh/      # Cilium, Envoy, Istio, Linkerd
│   ├── observability/        # Prometheus (+ Alertmanager), OpenTelemetry, Jaeger, Fluentd
│   ├── gitops-packaging/     # Helm, Argo (CD, Workflows, Rollouts), Flux
│   ├── security-identity/    # SPIFFE/SPIRE, OPA, Kyverno, cert-manager, Falco, Harbor
│   ├── storage-messaging/    # Rook, NATS
│   └── ai-ml/                # Kubeflow
├── manifest/
│   ├── projects.json         # Declarative source definitions & dynamic version resolvers
│   └── lock.json             # Exact upstream commit SHAs, timestamps, mappings & file counts
└── scripts/
    ├── sync_docs.py          # Repeatable parallel sparse-checkout sync tool (Python 3 stdlib)
    └── export_jsonl.py       # Export prose/code docs + pinned GitHub URLs to JSONL for RAG
```

## Project Inventory

| Layer | Project | Local Path | Upstream Repo & Path | Pin (`SHA`) | Format | Files | Size |
| :--- | :--- | :--- | :--- | :--- | :--- | ---: | ---: |
| Orchestration & Core | **Kubernetes** | [`docs/orchestration-core/kubernetes/`](docs/orchestration-core/kubernetes) | [`kubernetes/website`](https://github.com/kubernetes/website) (`content/en/docs`) | [`18f8e9f`](https://github.com/kubernetes/website/tree/18f8e9f6d2b0bc9d33e82ceac8abcfffdf8c1ca8) | Markdown | 1,799 | 19.45 MB |
| Orchestration & Core | **etcd** | [`docs/orchestration-core/etcd/`](docs/orchestration-core/etcd) | [`etcd-io/website`](https://github.com/etcd-io/website) (`content/en/docs/v3.7`) | [`41e5cd6`](https://github.com/etcd-io/website/tree/41e5cd6ab9efcf67270cea28790f77df8e6c2ed4) | Markdown | 105 | 1.20 MB |
| Orchestration & Core | **containerd** | [`docs/orchestration-core/containerd/`](docs/orchestration-core/containerd) | [`containerd/containerd`](https://github.com/containerd/containerd) (`docs`) | [`bc6efe7`](https://github.com/containerd/containerd/tree/bc6efe74c55e588dded980f941a7b1ddd2f6e24d) | Markdown | 41 | 0.42 MB |
| Orchestration & Core | **CoreDNS** | [`docs/orchestration-core/coredns/`](docs/orchestration-core/coredns) | [`coredns/coredns.io`](https://github.com/coredns/coredns.io) (`content/manual, content/plugins, content/explugins`) | [`ac92d6b`](https://github.com/coredns/coredns.io/tree/ac92d6b4a9ce165b15dca3f52da29fc5dd903881) | Markdown | 111 | 0.42 MB |
| Orchestration & Core | **KubeVirt** | [`docs/orchestration-core/kubevirt/`](docs/orchestration-core/kubevirt) | [`kubevirt/user-guide`](https://github.com/kubevirt/user-guide) (`docs`) | [`a5ee79e`](https://github.com/kubevirt/user-guide/tree/a5ee79eb1158499fe159be30c5980b70f6470800) | Markdown | 109 | 1.16 MB |
| Orchestration & Core | **Karmada** | [`docs/orchestration-core/karmada/`](docs/orchestration-core/karmada) | [`karmada-io/website`](https://github.com/karmada-io/website) (`docs`) | [`09a9148`](https://github.com/karmada-io/website/tree/09a91484291f42b53ca695abbce9bbe6b95bb7f1) | Markdown | 302 | 3.12 MB |
| Networking & Mesh | **Cilium** | [`docs/networking-mesh/cilium/`](docs/networking-mesh/cilium) | [`cilium/cilium`](https://github.com/cilium/cilium) (`Documentation`) | [`f32bb49`](https://github.com/cilium/cilium/tree/f32bb49abd833dec942d9692ca902a401fa4f0f6) | reStructuredText (`.rst`) | 695 | 5.04 MB |
| Networking & Mesh | **Envoy** | [`docs/networking-mesh/envoy/`](docs/networking-mesh/envoy) | [`envoyproxy/envoy`](https://github.com/envoyproxy/envoy) (`docs/root`) | [`56d0713`](https://github.com/envoyproxy/envoy/tree/56d0713f6e74bd88850304aa003abf8427017996) | reStructuredText (`.rst`) | 716 | 6.81 MB |
| Networking & Mesh | **Istio** | [`docs/networking-mesh/istio/`](docs/networking-mesh/istio) | [`istio/istio.io`](https://github.com/istio/istio.io) (`content/en/docs`) | [`962f6f6`](https://github.com/istio/istio.io/tree/962f6f65b5ec120fd7cfa5904f2aa252ec37540f) | Markdown | 733 | 7.75 MB |
| Networking & Mesh | **Linkerd** | [`docs/networking-mesh/linkerd/`](docs/networking-mesh/linkerd) | [`linkerd/website`](https://github.com/linkerd/website) (`linkerd.io/content/2.19`) | [`4a84011`](https://github.com/linkerd/website/tree/4a84011881f22a204d2a4348a3476bc9c5ec42f0) | Markdown | 157 | 1.43 MB |
| Observability | **Prometheus** | [`docs/observability/prometheus/`](docs/observability/prometheus) | [`prometheus/docs`](https://github.com/prometheus/docs) (`docs`)<br>[`prometheus/prometheus`](https://github.com/prometheus/prometheus) (`docs`)<br>[`prometheus/alertmanager`](https://github.com/prometheus/alertmanager) (`docs`) | [`9bc542d`](https://github.com/prometheus/docs/tree/9bc542d9e249eac482c719668d19387e8774559f)<br>[`49c815a`](https://github.com/prometheus/prometheus/tree/49c815a0ea46c7a6a6b723e4b634c4bf36f7022c)<br>[`b6c5821`](https://github.com/prometheus/alertmanager/tree/b6c5821b9f33187955b411c976114eeaf7b18c47) | Markdown | 111 | 1.57 MB |
| Observability | **OpenTelemetry** | [`docs/observability/opentelemetry/`](docs/observability/opentelemetry) | [`open-telemetry/opentelemetry.io`](https://github.com/open-telemetry/opentelemetry.io) (`content/en/docs`) | [`6916167`](https://github.com/open-telemetry/opentelemetry.io/tree/6916167d61aba7cef0a2fcb7a757d90397c26f1c) | Markdown | 504 | 5.85 MB |
| Observability | **Jaeger** | [`docs/observability/jaeger/`](docs/observability/jaeger) | [`jaegertracing/documentation`](https://github.com/jaegertracing/documentation) (`content/docs/v2/2.23`) | [`fc38927`](https://github.com/jaegertracing/documentation/tree/fc38927c851c96094ba69f603ed3ed56bf3a6926) | Markdown | 41 | 0.46 MB |
| Observability | **Fluentd** | [`docs/observability/fluentd/`](docs/observability/fluentd) | [`fluent/fluentd-docs-gitbook`](https://github.com/fluent/fluentd-docs-gitbook) (`/`) | [`c454def`](https://github.com/fluent/fluentd-docs-gitbook/tree/c454defcb185e11cb85735535fff04f0bf09ca3e) | Markdown | 220 | 1.81 MB |
| GitOps & Packaging | **Helm** | [`docs/gitops-packaging/helm/`](docs/gitops-packaging/helm) | [`helm/helm-www`](https://github.com/helm/helm-www) (`docs`) | [`f963027`](https://github.com/helm/helm-www/tree/f9630272ef357f051d72e4311b97a3d2c701c8c0) | Markdown | 139 | 0.89 MB |
| GitOps & Packaging | **Argo (CD, Workflows, Rollouts)** | [`docs/gitops-packaging/argo/`](docs/gitops-packaging/argo) | [`argoproj/argo-cd`](https://github.com/argoproj/argo-cd) (`docs`)<br>[`argoproj/argo-workflows`](https://github.com/argoproj/argo-workflows) (`docs`)<br>[`argoproj/argo-rollouts`](https://github.com/argoproj/argo-rollouts) (`docs`) | [`502a751`](https://github.com/argoproj/argo-cd/tree/502a7513e54939143f740e4fc0b278ec53d4336a)<br>[`93303d1`](https://github.com/argoproj/argo-workflows/tree/93303d1862325845bb73e9b194857732ec2615f7)<br>[`4008dce`](https://github.com/argoproj/argo-rollouts/tree/4008dce7c67639675f777d5588db366581739534) | Markdown | 855 | 10.11 MB |
| GitOps & Packaging | **Flux** | [`docs/gitops-packaging/flux/`](docs/gitops-packaging/flux) | [`fluxcd/website`](https://github.com/fluxcd/website) (`content/en/flux`) | [`8692e41`](https://github.com/fluxcd/website/tree/8692e419ef59246141b8b83e7018c104d40eb43b) | Markdown | 161 | 1.74 MB |
| Security & Identity | **SPIFFE / SPIRE** | [`docs/security-identity/spiffe-spire/`](docs/security-identity/spiffe-spire) | [`spiffe/spiffe.io`](https://github.com/spiffe/spiffe.io) (`content/docs/latest`)<br>[`spiffe/spire`](https://github.com/spiffe/spire) (`doc`) | [`e329662`](https://github.com/spiffe/spiffe.io/tree/e329662c0e27b97b9a680fc5cf9de0de0dc83e53)<br>[`ca4c244`](https://github.com/spiffe/spire/tree/ca4c2442bac1334a859a15c72a5500b44be32ab3) | Markdown | 177 | 1.94 MB |
| Security & Identity | **Open Policy Agent (OPA)** | [`docs/security-identity/opa/`](docs/security-identity/opa) | [`open-policy-agent/opa`](https://github.com/open-policy-agent/opa) (`docs/docs`) | [`ef171a8`](https://github.com/open-policy-agent/opa/tree/ef171a816f9da4bc26085f634f14f477d85d242c) | Markdown | 608 | 1.87 MB |
| Security & Identity | **Kyverno** | [`docs/security-identity/kyverno/`](docs/security-identity/kyverno) | [`kyverno/website`](https://github.com/kyverno/website) (`src/content/docs`) | [`eb7c94b`](https://github.com/kyverno/website/tree/eb7c94bb94153c0501855b251c9ba2e723b419df) | Markdown | 80 | 1.40 MB |
| Security & Identity | **cert-manager** | [`docs/security-identity/cert-manager/`](docs/security-identity/cert-manager) | [`cert-manager/website`](https://github.com/cert-manager/website) (`content/docs`) | [`8274510`](https://github.com/cert-manager/website/tree/82745109ed8dc8b2d7ce67bb4a8394d5f06ae1a6) | Markdown | 261 | 3.59 MB |
| Security & Identity | **Falco** | [`docs/security-identity/falco/`](docs/security-identity/falco) | [`falcosecurity/falco-website`](https://github.com/falcosecurity/falco-website) (`content/en/docs`) | [`a163869`](https://github.com/falcosecurity/falco-website/tree/a16386978afdaaad8bb6fb74bd5a8640c5d7e7d1) | Markdown | 163 | 0.79 MB |
| Security & Identity | **Harbor** | [`docs/security-identity/harbor/`](docs/security-identity/harbor) | [`goharbor/website`](https://github.com/goharbor/website) (`docs`) | [`f592baf`](https://github.com/goharbor/website/tree/f592bafad330584e5ddaaf0ba05ab44ac751e73e) | Markdown | 96 | 0.82 MB |
| Storage & Messaging | **Rook** | [`docs/storage-messaging/rook/`](docs/storage-messaging/rook) | [`rook/rook`](https://github.com/rook/rook) (`Documentation`) | [`719f345`](https://github.com/rook/rook/tree/719f345e220db7b9617c98a43f74160fa039cc7d) | Markdown | 98 | 1.19 MB |
| Storage & Messaging | **NATS** | [`docs/storage-messaging/nats/`](docs/storage-messaging/nats) | [`nats-io/nats.docs`](https://github.com/nats-io/nats.docs) (`/`) | [`f115bec`](https://github.com/nats-io/nats.docs/tree/f115becf6563e3bbe16bb94cbf87bfceb84199c1) | Markdown | 209 | 1.65 MB |
| AI / ML | **Kubeflow** | [`docs/ai-ml/kubeflow/`](docs/ai-ml/kubeflow) | [`kubeflow/website`](https://github.com/kubeflow/website) (`content/en/docs`) | [`a7b22c9`](https://github.com/kubeflow/website/tree/a7b22c962aeddfecb68d6cf747f8a1bbb0543018) | Markdown | 268 | 2.73 MB |

## Keeping the Backup Updated

`scripts/sync_docs.py` uses `git clone --depth 1 --filter=blob:none --sparse` with no third-party Python dependencies:

```bash
# Re-sync all 26 CNCF Graduated projects (default scope: text-svg)
python3 scripts/sync_docs.py

# Re-sync specific project(s) only
python3 scripts/sync_docs.py --project kubernetes --project cilium

# Switch backup scope if desired (text-only | text-svg | all-media)
python3 scripts/sync_docs.py --scope text-only
```

## Using This Corpus for Retrieval / RAG

```bash
# Export all prose docs (.md/.mdx/.rst/.txt) with extracted titles & pinned GitHub blob URLs
python3 scripts/export_jsonl.py --output corpus.jsonl

# Include standalone YAML/JSON/code example files as well
python3 scripts/export_jsonl.py --include-code --output corpus_with_code.jsonl
```

1. **Provenance & deep-linking (`manifest/lock.json`):** Every project entry in `manifest/lock.json` records its exact `commit_sha`, `upstream_path`, and `local_subdir`, allowing your ingestion pipeline to attach canonical GitHub source URLs and CNCF layer metadata to each chunk.
2. **File formats:**
   - **Markdown / MDX (`.md`, `.mdx`):** 24 of 26 projects. Note that Hugo/Docusaurus/Starlight frontmatter (`--- ... ---`) at the top of files contains clean `title`, `description`, and `weight` metadata useful for hybrid search.
   - **reStructuredText (`.rst`):** Cilium and Envoy use Sphinx `.rst` directives (`.. code-block::`, `.. note::`, `:ref:`).
3. **Licenses:** Upstream `UPSTREAM_LICENSE*` files are preserved inside each project directory alongside the documentation.
