# GPU cluster PRD template

A requirements template for building or expanding a GPU cluster, written for a platform product manager working with infrastructure engineering, security, finance, and the teams who will run workloads on it.

Replace the bracketed prompts. Delete sections that don't apply, but say why.

---

## 1. Summary

- **What we're building:** [e.g. a GPU cluster for fine-tuning and inference, available as an internal shared service]
- **Why now:** [demand signal, cost of the status quo, strategic driver]
- **Decision needed:** [what leadership is being asked to approve: budget, vendor, timeline]

## 2. Customers and workloads

| Customer / team | Workload type | Job size (GPUs) | Duration | Priority |
|---|---|---|---|---|
| [Team A] | [Pre-training / fine-tuning / batch inference / online inference] | [8 / 64 / 512] | [hours / days] | [P0–P2] |

- Expected demand curve over 12–24 months
- Peak vs average utilization, and how idle capacity will be used

## 3. Goals and non-goals

**Goals** (measurable):
- [e.g. Reach X% average GPU utilization within 2 quarters of launch]
- [e.g. Keep queue wait for P0 jobs under Y hours]
- [e.g. Lower cost per GPU-hour below the current cloud baseline]

**Non-goals:**
- [e.g. Serving external customers in phase 1]

## 4. Functional requirements

### Compute
- GPU model and generation; GPUs per node; CPU and memory per node
- Node-level interconnect requirements (GPU-to-GPU within a node)

### Network
- Back-end fabric: [InfiniBand / RoCE]; see the [fabric decision framework](01-infiniband-vs-roce.md)
- Topology: [fat-tree / rail-optimized], oversubscription ratio, target scale per pod
- Front-end and storage networks; out-of-band management network

### Storage
- Dataset and checkpoint capacity; required read/write throughput
- Checkpoint frequency and restore-time target

### Scheduling and platform
- Scheduler: [Kubernetes / Slurm / both]; quota and priority model
- Self-service: how users request capacity, and approval rules
- Image and driver lifecycle: how CUDA, drivers, and firmware are tested and rolled out

### Multi-tenancy
- Isolation model per tenant (network, storage, scheduler, GPU partitioning)
- Chargeback or showback model

## 5. Non-functional requirements

| Area | Requirement | Target |
|---|---|---|
| Performance | Collective bandwidth at target scale | [≥ X% of line rate] |
| Performance | Representative job step time | [within X% of reference] |
| Utilization | Average GPU utilization | [≥ X%] |
| Reliability | Node availability | [≥ X%] |
| Reliability | Job recovery from node or link failure | [resume from checkpoint within X min] |
| Security | See [zero-trust segmentation](04-zero-trust-ai-infrastructure.md) | Controls in section 6 |
| Operability | Telemetry coverage | GPU, NIC, switch, power, thermal |
| Facilities | Power and cooling per rack | [kW per rack; air vs liquid cooling] |

## 6. Security and compliance requirements

- Management plane (BMC, switch management) on an isolated out-of-band network
- Tenant isolation enforced at the network, storage, and scheduler layers
- Model weights and training data: access control, encryption at rest and in transit, audit logging
- Privileged access through just-in-time, audited paths
- Compliance and data-residency constraints: [e.g. which data can't leave which region]

## 7. Build vs buy and options considered

| Option | Pros | Cons | Cost (3-year TCO) |
|---|---|---|---|
| On-prem cluster | | | See [TCO model](03-gpu-tco-model.md) |
| Reserved cloud GPUs | | | |
| GPU cloud provider (neocloud) | | | |
| Hybrid: baseline on-prem, burst to cloud | | | |

## 8. Rollout plan

| Phase | Scope | Exit criteria |
|---|---|---|
| PoC | [N] nodes, target fabric | Benchmarks and acceptance criteria met |
| Pilot | First 1–2 customer teams | Utilization and satisfaction targets met |
| GA | All internal teams | Support model, runbooks, chargeback live |
| Expansion | Next pod / generation | Demand trigger reached |

## 9. Success metrics

- **Adoption:** active teams, GPU-hours consumed
- **Efficiency:** GPU utilization, queue wait time, cost per GPU-hour
- **Reliability:** job failure rate attributable to infrastructure, mean time to recover
- **Customer:** time from request to running job; internal satisfaction

## 10. Risks and dependencies

| Risk / dependency | Impact | Mitigation | Owner |
|---|---|---|---|
| GPU and optics lead times | Schedule slip | Early commits, alternate SKUs | |
| Power / cooling capacity | Can't rack hardware | Facilities assessment before PO | |
| Driver / firmware regressions | Job failures | Staged rollout with canary nodes | |
| Skills gap on fabric operations | Slow incident response | Training, vendor support, runbooks | |

## 11. Open questions

- [List decisions not yet made, and who owns each one]
