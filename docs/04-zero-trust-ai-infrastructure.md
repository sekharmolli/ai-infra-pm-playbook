# Zero-trust segmentation for AI infrastructure

## Why AI infrastructure needs its own security design

A GPU cluster concentrates three things attackers want: **expensive compute**, **sensitive training data**, and **model weights** that may be the most valuable asset the company owns. It also brings network paths that traditional enterprise security tooling often doesn't see, such as RDMA traffic on the back-end fabric that bypasses the host networking stack.

Zero trust here means the usual principles (no implicit trust based on network location, explicit verification, least privilege, assume breach), applied to the specific planes of an AI cluster. NIST SP 800-207 is a useful reference for the general architecture.

## The planes to segment

| Plane | What lives there | Primary risk | Key controls |
|---|---|---|---|
| **Out-of-band management** | BMCs, switch and PDU management, console servers | Full hardware takeover | Physically or logically separate network; jump-host access only; MFA; no internet path; firmware integrity checks |
| **Control plane** | Schedulers, Kubernetes control plane, provisioning, identity | Cluster-wide compromise | Admin-only network segment; strong identity and RBAC; audited privileged access |
| **Back-end GPU fabric** | GPU-to-GPU RDMA traffic (InfiniBand or RoCE) | Cross-tenant data leakage; lateral movement | Tenant isolation (IB partition keys, or VRF/VLAN/EVPN for RoCE); fabric reserved for job traffic only |
| **Front-end / service network** | User access, APIs, inference endpoints | External attack surface | Identity-aware access; micro-segmentation between services; WAF and API gateways for inference |
| **Storage network** | Datasets, checkpoints, model weights | Data or model exfiltration | Per-tenant access policies; encryption at rest and in transit; egress monitoring |

## Tenant isolation model

For a shared or multi-tenant GPU platform, isolation has to hold at **every layer**. One weak layer undoes the others.

1. **Scheduler:** tenants get namespaces/partitions and quotas; no cross-tenant job visibility
2. **Node:** whole-node allocation for sensitive tenants; GPU partitioning only where the isolation guarantees fit the risk
3. **Fabric:** each tenant's jobs on its own partition or virtual network
4. **Storage:** per-tenant volumes and keys; no shared writable paths
5. **Data handling:** GPU memory and local disks cleared between tenants

## Protecting model weights and training data

- Classify weights and datasets; apply the strictest controls to the crown-jewel models
- Encrypt at rest with keys in a KMS/HSM; restrict key use to specific workloads
- Restrict and log every path that can read weights: training jobs, export pipelines, admin access
- Monitor for unusual egress volume from storage and inference nodes
- Use confidential-computing capabilities on newer CPUs and GPUs where the threat model justifies the overhead

## Firewall and policy modernization

AI clusters change fast, and manual firewall change processes become the bottleneck. A modern policy workflow:

1. **Intent-based requests:** "service A needs to reach service B on port X"
2. **Automated validation:** checks against policy rules and conflict detection before approval
3. **Policy as code:** rules versioned, reviewed, and deployed through CI/CD
4. **Post-change verification:** automated tests confirm the intended flow works and nothing else opened up
5. **Rollback readiness and audit evidence:** every change traceable for compliance

## Requirements I'd put in the PRD

- Management network isolated with no route from tenant workloads
- Tenant isolation verified by test at the fabric, storage, and scheduler layers before GA
- All privileged access through MFA-protected, just-in-time, recorded sessions
- Model weights encrypted at rest, with access limited to named workloads and logged
- Security telemetry covering east–west flows, not just the perimeter
- Firewall and segmentation changes deployed as code, with automated verification

## Metrics

| Metric | Why it matters |
|---|---|
| % of east–west flows covered by explicit policy | Measures how much of the cluster is actually segmented |
| Mean time to approve and deploy a policy change | Security that slows AI teams too much gets bypassed |
| Privileged sessions without a ticket or JIT approval | Should be zero |
| Cross-tenant isolation test pass rate | Should be 100% before every major change |
| Time to detect anomalous data egress | Measures readiness against exfiltration |
