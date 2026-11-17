# InfiniBand vs RoCE for AI clusters: a PM's decision framework

## The decision

An AI cluster usually has two or three networks: a **back-end (scale-out) fabric** carrying GPU-to-GPU traffic for distributed training, a **front-end network** for users, storage, and management, and often an **out-of-band management network**. This document is about the back-end fabric, where the choice is mainly between:

- **InfiniBand (IB):** a purpose-built HPC fabric with native lossless, credit-based flow control and in-network features designed for collective operations.
- **RoCE v2 (RDMA over Converged Ethernet):** RDMA carried over routable UDP/IP on Ethernet, which needs careful lossless or congestion-control tuning to perform well.

Both can run large training jobs. The real question is which one this team can **deliver, operate, and scale** at the target cost and risk.

## Start from the workload

| Workload | What stresses the fabric | Implication |
|---|---|---|
| Large-scale pre-training | All-reduce and all-to-all collectives across many nodes; tail latency stalls every GPU | Fabric performance and congestion behavior matter most |
| Fine-tuning / mid-size training | Same patterns at smaller scale | Either fabric is usually adequate; operations and cost matter more |
| Inference | Mostly front-end and storage traffic; some multi-node serving for very large models | Back-end fabric is often less critical; Ethernet is often sufficient |
| Mixed / multi-tenant GPU cloud | Isolation, noisy neighbors, many job sizes | Tenancy features and operational tooling matter as much as raw speed |

## Comparison

| Dimension | InfiniBand | RoCE v2 (Ethernet) |
|---|---|---|
| Lossless behavior | Native, credit-based | Needs PFC and/or ECN-based congestion control, tuned end to end |
| Collective acceleration | In-network reduction features available on some platforms | Depends on vendor and switch generation |
| Routing and scale | Subnet-managed fabric; fat-tree and rail-optimized designs are common | Standard IP routing; scales with familiar Ethernet designs |
| Ecosystem | Concentrated supplier base | Multi-vendor switches, NICs, and optics; industry efforts such as the Ultra Ethernet Consortium are evolving the standard |
| Operations skills | Specialized; fewer engineers have it | Builds on existing network team skills, but RDMA tuning is still specialist work |
| Tooling and telemetry | Integrated fabric managers | Varies by vendor; strong in modern AI-focused Ethernet platforms |
| Multi-tenancy | Partition keys (PKeys) for isolation | VRF/VLAN/EVPN and existing Ethernet segmentation patterns |
| Cost profile | Often a premium; less price competition | More competition; total cost depends heavily on optics and switch tier |
| Lock-in risk | Higher | Lower, though "AI Ethernet" features can still be vendor-specific |

## Decision guide

**Lean InfiniBand when:**
- The cluster is dedicated to large-scale training and peak collective performance is the goal
- The team already has IB operations skills, or the vendor provides a fully managed reference design
- Time-to-first-job matters more than supplier diversity

**Lean RoCE / Ethernet when:**
- The infrastructure is a multi-tenant GPU cloud, or mixes training and inference
- The organization wants one networking skill set and a multi-vendor supply chain
- Cost, supply availability, or integration with existing data center automation and security tooling is a top concern

**Either way:** keep the front-end and management networks on Ethernet, and design the storage path deliberately. Slow checkpointing or data loading can waste more GPU time than the back-end fabric does.

## Evidence I'd require before committing

A PoC on the real target node design (the same GPUs, NICs, and topology), not a vendor slide:

| Test | What it tells us | Example acceptance criterion |
|---|---|---|
| Collective benchmarks (e.g. NCCL all-reduce / all-to-all bus bandwidth) across 2, 8, 32+ nodes | Scaling efficiency as the cluster grows | Bus bandwidth stays within an agreed % of line rate at target scale |
| Representative training job | Real time-to-train and GPU utilization | Step time within X% of reference; GPU utilization above target |
| Congestion and incast test | Behavior under contention, the usual RoCE weak spot | No sustained pause storms; tail latency within bound |
| Failure injection (link, switch, NIC) | Recovery time and job impact | Job checkpoint/resume works; fabric reconverges within target |
| Multi-tenant isolation test | Whether one tenant can degrade another | Noisy-neighbor impact below agreed threshold |
| Day-2 operations walkthrough | Can our team run it? | Telemetry, alerting, and upgrade procedure documented and rehearsed |

## Risks to track

- **Tuning debt (RoCE):** PFC/ECN misconfiguration causes head-of-line blocking or pause storms. Mitigate with validated reference configs and continuous telemetry.
- **Supply and lead times (both):** switches, NICs, and especially optics can gate the schedule. Track them as a roadmap dependency.
- **Skills concentration (IB):** a fabric only two people understand is an operational risk.
- **Topology lock-in:** rail-optimized vs fat-tree choices are hard to change after cabling.

## What I'd put in the PRD

- The workload mix and target scale for the next 2–3 hardware generations
- Fabric choice with the PoC evidence attached
- Performance SLOs (collective bandwidth, job step time, GPU utilization)
- Isolation requirements for tenants
- Day-2 operations requirements: telemetry, upgrades, failure recovery
