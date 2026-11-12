# Cloud-Native, Apache Data Ecosystem & Snowflake Documentation Corpus

Consolidated, version-pinned documentation corpus covering **45 flagship projects** (**26 CNCF Graduated**, **18 Apache Series**, and **Snowflake**) across **12 architectural layers**, structured for learning, offline reference, and Retrieval-Augmented Generation (RAG).

## Corpus Summary

- **Last synced (UTC):** `2026-11-12T02:57:23Z`
- **Backup scope:** `text-svg` (prose docs + config/code examples + vector `.svg` architecture diagrams; latest stable version per project)
- **Total projects:** `45` (synced from `53` upstream GitHub repositories)
- **Total files:** `16,066` (`12,386` Markdown/MDX, `1,247` reStructuredText, `199` AsciiDoc, `1,048` YAML/JSON/SQL/code examples, `1,093` SVG diagrams)
- **Uncompressed corpus size:** `184.20 MB`

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
│   ├── ai-ml/                # Kubeflow
│   ├── data-streaming/       # Apache Kafka, Flink, Spark, Pulsar, Beam
│   ├── data-orchestration/   # Apache Airflow
│   ├── data-lakehouse/       # Apache Iceberg, Hudi, Paimon, Polaris, Arrow, Snowflake
│   ├── data-analytics/       # Apache Druid, Pinot, Doris, Superset
│   └── distributed-storage/  # Apache Cassandra, ZooKeeper, Ozone
├── manifest/
│   ├── projects.json         # Declarative source definitions & dynamic version resolvers
│   └── lock.json             # Exact upstream commit SHAs, timestamps, mappings & file counts
└── scripts/
    ├── sync_docs.py          # Repeatable parallel sparse-checkout sync tool (Python 3 stdlib)
    ├── sync_snowflake_llms.py# Pull Snowflake core docs via docs.snowflake.com/llms.txt (.md)
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
| Data Streaming & Compute | **Apache Kafka** | [`docs/data-streaming/kafka/`](docs/data-streaming/kafka) | [`apache/kafka`](https://github.com/apache/kafka) (`docs`) | [`0e67542`](https://github.com/apache/kafka/tree/0e675429a2d15605322ac6a8e3077433cbe15732) | Markdown | 114 | 1.64 MB |
| Data Streaming & Compute | **Apache Flink** | [`docs/data-streaming/flink/`](docs/data-streaming/flink) | [`apache/flink`](https://github.com/apache/flink) (`docs/content/docs`) | [`9f6afde`](https://github.com/apache/flink/tree/9f6afdeb1ad0e2e24f94070df5bab35bf00517a9) | Markdown | 478 | 9.77 MB |
| Data Streaming & Compute | **Apache Spark** | [`docs/data-streaming/spark/`](docs/data-streaming/spark) | [`apache/spark`](https://github.com/apache/spark) (`docs`) | [`43744f5`](https://github.com/apache/spark/tree/43744f5c5b918ffda501e3c964104f74f7b13b18) | Markdown | 260 | 3.64 MB |
| Data Streaming & Compute | **Apache Pulsar** | [`docs/data-streaming/pulsar/`](docs/data-streaming/pulsar) | [`apache/pulsar-site`](https://github.com/apache/pulsar-site) (`docs`) | [`08529bc`](https://github.com/apache/pulsar-site/tree/08529bc57abee1d90716402df102223e330317e6) | Markdown | 337 | 6.22 MB |
| Data Streaming & Compute | **Apache Beam** | [`docs/data-streaming/beam/`](docs/data-streaming/beam) | [`apache/beam`](https://github.com/apache/beam) (`website/www/site/content/en/documentation`) | [`3a84bd5`](https://github.com/apache/beam/tree/3a84bd59a42027598f4fe9649d51fe0a845176ea) | Markdown | 297 | 6.04 MB |
| Data Orchestration | **Apache Airflow** | [`docs/data-orchestration/airflow/`](docs/data-orchestration/airflow) | [`apache/airflow`](https://github.com/apache/airflow) (`airflow-core/docs, docker-stack-docs`) | [`34c9650`](https://github.com/apache/airflow/tree/34c96509ebcb0e77aaf1066f754da8f7e86919da) | reStructuredText (`.rst`) | 194 | 2.38 MB |
| Data Lakehouse & Warehousing | **Apache Iceberg** | [`docs/data-lakehouse/iceberg/`](docs/data-lakehouse/iceberg) | [`apache/iceberg`](https://github.com/apache/iceberg) (`docs/docs`) | [`e31ea5f`](https://github.com/apache/iceberg/tree/e31ea5f39b3e7d4a536cad3a4dbdc16dcf1e1553) | Markdown | 42 | 0.70 MB |
| Data Lakehouse & Warehousing | **Apache Hudi** | [`docs/data-lakehouse/hudi/`](docs/data-lakehouse/hudi) | [`apache/hudi`](https://github.com/apache/hudi) (`website/docs`) | [`56ebc22`](https://github.com/apache/hudi/tree/56ebc227f0154c913ecdbc85ae186b0a0ca56083) | Markdown | 77 | 4.08 MB |
| Data Lakehouse & Warehousing | **Apache Paimon** | [`docs/data-lakehouse/paimon/`](docs/data-lakehouse/paimon) | [`apache/paimon`](https://github.com/apache/paimon) (`docs/docs`) | [`68023de`](https://github.com/apache/paimon/tree/68023de1160c16a67dd839c638ba817de23a9212) | Markdown | 302 | 2.50 MB |
| Data Lakehouse & Warehousing | **Apache Polaris** | [`docs/data-lakehouse/polaris/`](docs/data-lakehouse/polaris) | [`apache/polaris`](https://github.com/apache/polaris) (`site/content/in-dev/unreleased, site/content/guides`) | [`02ba4b6`](https://github.com/apache/polaris/tree/02ba4b6d21594341ccd4c14c1c929a1da40d0485) | Markdown | 157 | 0.90 MB |
| Data Lakehouse & Warehousing | **Apache Arrow** | [`docs/data-lakehouse/arrow/`](docs/data-lakehouse/arrow) | [`apache/arrow`](https://github.com/apache/arrow) (`docs/source`) | [`7eb865c`](https://github.com/apache/arrow/tree/7eb865cd80793a23a6551ad136a33956783def0a) | reStructuredText (`.rst`) | 243 | 3.57 MB |
| Data Lakehouse & Warehousing | **Snowflake** | [`docs/data-lakehouse/snowflake/`](docs/data-lakehouse/snowflake) | [`Snowflake-Labs/sfquickstarts`](https://github.com/Snowflake-Labs/sfquickstarts) (`site/sfguides/src`)<br>[`snowflakedb/snowpark-python`](https://github.com/snowflakedb/snowpark-python) (`docs`)<br>[`snowflakedb/snowflake-cli`](https://github.com/snowflakedb/snowflake-cli) (`docs`)<br>[`snowflakedb/terraform-provider-snowflake`](https://github.com/snowflakedb/terraform-provider-snowflake) (`docs`) | [`7b2a8ec`](https://github.com/Snowflake-Labs/sfquickstarts/tree/7b2a8eca216b40917cff83e7b9bd0524698b5a4b)<br>[`d5e1f8d`](https://github.com/snowflakedb/snowpark-python/tree/d5e1f8dbb2dfaae8047da2192a35476d4f5fc21c)<br>[`9370ee1`](https://github.com/snowflakedb/snowflake-cli/tree/9370ee1302970ce086bfe620b6ecee85d09ca66b)<br>[`8a7d19b`](https://github.com/snowflakedb/terraform-provider-snowflake/tree/8a7d19b230d48917f630cce54f147e3ed01d01f9) | Markdown | 1,260 | 26.91 MB |
| Real-Time OLAP & Analytics | **Apache Druid** | [`docs/data-analytics/druid/`](docs/data-analytics/druid) | [`apache/druid`](https://github.com/apache/druid) (`docs`) | [`c951187`](https://github.com/apache/druid/tree/c951187c8bd59718b9dc3590bf1522e80567ec11) | Markdown | 269 | 3.65 MB |
| Real-Time OLAP & Analytics | **Apache Pinot** | [`docs/data-analytics/pinot/`](docs/data-analytics/pinot) | [`pinot-contrib/pinot-docs`](https://github.com/pinot-contrib/pinot-docs) (`/`) | [`3bf13a8`](https://github.com/pinot-contrib/pinot-docs/tree/3bf13a86f53de7ad0548c37db76907020b022dce) | Markdown | 661 | 7.82 MB |
| Real-Time OLAP & Analytics | **Apache Doris** | [`docs/data-analytics/doris/`](docs/data-analytics/doris) | [`apache/doris-website`](https://github.com/apache/doris-website) (`docs`) | [`736c70f`](https://github.com/apache/doris-website/tree/736c70f77feb116f6a031393f5ad45e84a8a6a1b) | Markdown | 1,803 | 12.60 MB |
| Real-Time OLAP & Analytics | **Apache Superset** | [`docs/data-analytics/superset/`](docs/data-analytics/superset) | [`apache/superset`](https://github.com/apache/superset) (`docs/docs, docs/admin_docs`) | [`c0a86c7`](https://github.com/apache/superset/tree/c0a86c7596f1587616370950ecf7059fa0d96793) | Markdown | 101 | 1.54 MB |
| Distributed Storage & Coordination | **Apache Cassandra** | [`docs/distributed-storage/cassandra/`](docs/distributed-storage/cassandra) | [`apache/cassandra`](https://github.com/apache/cassandra) (`doc/modules/cassandra/pages, doc/modules/ROOT/pages`) | [`197b73d`](https://github.com/apache/cassandra/tree/197b73dcdf78f0554e7ae8fe411f4296b7875640) | AsciiDoc (`.adoc`) | 201 | 1.67 MB |
| Distributed Storage & Coordination | **Apache ZooKeeper** | [`docs/distributed-storage/zookeeper/`](docs/distributed-storage/zookeeper) | [`apache/zookeeper`](https://github.com/apache/zookeeper) (`zookeeper-website/app/pages/_docs/docs/_mdx`) | [`5dd643f`](https://github.com/apache/zookeeper/tree/5dd643fbf8c9cfec5b2fb00212235a5621abc6dd) | Markdown | 42 | 0.52 MB |
| Distributed Storage & Coordination | **Apache Ozone** | [`docs/distributed-storage/ozone/`](docs/distributed-storage/ozone) | [`apache/ozone-site`](https://github.com/apache/ozone-site) (`docs`) | [`5cc01b7`](https://github.com/apache/ozone-site/tree/5cc01b799cd2fa40d7a2d5b5f2710bbc76c430f4) | Markdown | 469 | 2.84 MB |

## Keeping the Backup Updated

`scripts/sync_docs.py` uses `git clone --depth 1 --filter=blob:none --sparse` with no third-party Python dependencies:

```bash
# Re-sync all 45 CNCF, Apache & Snowflake GitHub projects (default scope: text-svg)
python3 scripts/sync_docs.py

# Re-sync specific project(s) only
python3 scripts/sync_docs.py --project kafka --project flink --project iceberg

# Optional: pull Snowflake's core docs.snowflake.com Markdown pages via llms.txt
# (run on any machine with direct HTTPS access to docs.snowflake.com)
python3 scripts/sync_snowflake_llms.py --section sql-reference --section user-guide

# Switch backup scope if desired (text-only | text-svg | all-media)
python3 scripts/sync_docs.py --scope text-only
```

## Using This Corpus for Retrieval / RAG

```bash
# Export all prose docs (.md/.mdx/.rst/.adoc/.txt) with extracted titles & pinned GitHub blob URLs
python3 scripts/export_jsonl.py --output corpus.jsonl

# Include standalone YAML/JSON/SQL/code example files as well
python3 scripts/export_jsonl.py --include-code --output corpus_with_code.jsonl
```

1. **Provenance & deep-linking (`manifest/lock.json`):** Every project entry in `manifest/lock.json` records its exact `commit_sha`, `upstream_path`, and `local_subdir`, allowing your ingestion pipeline to attach canonical GitHub source URLs and architectural layer metadata to each chunk.
2. **File formats:**
   - **Markdown / MDX (`.md`, `.mdx`):** Majority of CNCF, Apache, and Snowflake docs. Frontmatter (`--- ... ---`) at the top of files contains clean `title`, `description`, and `weight` metadata useful for hybrid search.
   - **reStructuredText (`.rst`):** Cilium, Envoy, Apache Airflow, and Apache Arrow use Sphinx `.rst` directives (`.. code-block::`, `.. note::`, `:ref:`).
   - **AsciiDoc (`.adoc`):** Apache Cassandra (and parts of Apache Polaris) use Antora/AsciiDoc (`= Title`, `[source,cql]`).
3. **Licenses:** Upstream `UPSTREAM_LICENSE*` files are preserved inside each project directory alongside the documentation.
