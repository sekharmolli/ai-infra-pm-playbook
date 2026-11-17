# AI Infrastructure PM Playbook

How I think about building, scaling, and securing the infrastructure underneath AI: **GPU clusters, high-performance fabrics, and the security controls around them**, from a product manager's seat.

This repo is a set of decision frameworks and templates. It isn't vendor documentation or an engineering spec. Each document answers a question a product or platform team actually has to settle, and shows the trade-offs, the evidence I'd ask for, and the risks I'd track.

## Contents

| # | Document | The question it answers |
|---|---|---|
| 1 | [InfiniBand vs RoCE for AI clusters](docs/01-infiniband-vs-roce.md) | Which back-end fabric should this cluster use, and how do we prove it? |
| 2 | [GPU cluster PRD template](docs/02-gpu-cluster-prd-template.md) | What does a complete requirements doc for a GPU cluster look like? |
| 3 | [GPU cloud vs on-prem TCO](docs/03-gpu-tco-model.md) | When does owning GPUs beat renting them? |
| 4 | [Zero-trust segmentation for AI infrastructure](docs/04-zero-trust-ai-infrastructure.md) | How do we isolate tenants, protect model weights, and lock down the fabric? |
| – | [TCO calculator](tools/gpu_tco_calculator.py) | A small Python script that runs the TCO comparison from doc 3 |

## How these were shaped

These frameworks come from hands-on infrastructure work: running a 40–50 rack lab and data center environment with Dell PowerEdge and HPE servers, GPU-enabled systems, and InfiniBand / RoCE / RDMA fabrics, then moving into product management for data center, HPC networking, and hybrid-cloud platforms.

The pattern I try to follow in every document:

1. **Start from the workload.** Training, fine-tuning, and inference stress infrastructure differently.
2. **Make the trade-off explicit.** Every choice costs something: money, operational skill, lock-in, or risk.
3. **Define the evidence.** Benchmarks, PoC acceptance criteria, and the metrics that would change the decision.
4. **Treat security as a requirement, not a phase.**

## Who this is for

- Hiring managers for AI infrastructure, GPU cloud, AI networking, and AI security product roles
- PMs moving into infrastructure who want a structured starting point

Related: [ai-pm-foundations](https://github.com/sekharmolli/ai-pm-foundations), on AI product design, evaluation, and guardrails at the application layer.

---

*Chandra Sekhar Molli · [LinkedIn](https://www.linkedin.com/in/chandrasekharmolli)*

*Figures in examples are illustrative inputs for the frameworks, not quotes or benchmarks from any vendor.*
