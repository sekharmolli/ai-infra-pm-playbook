#!/usr/bin/env python3
"""GPU on-prem vs cloud TCO calculator.

Implements the model in docs/03-gpu-tco-model.md. All default values are
illustrative placeholders; replace them with real quotes and demand data.
"""
import argparse

HOURS_PER_YEAR = 8760


def on_prem_cost_per_used_hour(gpus, hardware_cost, years, annual_opex, utilization):
    annual_capex = hardware_cost / years
    used_hours = gpus * HOURS_PER_YEAR * utilization
    return (annual_capex + annual_opex) / used_hours


def break_even_utilization(gpus, hardware_cost, years, annual_opex, cloud_rate):
    annual_fixed = hardware_cost / years + annual_opex
    return annual_fixed / (gpus * HOURS_PER_YEAR * cloud_rate)


def main():
    p = argparse.ArgumentParser(description="Compare on-prem vs cloud cost per used GPU-hour.")
    p.add_argument("--gpus", type=int, default=64, help="number of GPUs")
    p.add_argument("--hardware-cost", type=float, default=3_000_000,
                   help="total hardware cost incl. servers, network, optics (USD)")
    p.add_argument("--years", type=float, default=4, help="depreciation period in years")
    p.add_argument("--annual-opex", type=float, default=900_000,
                   help="power, cooling, facilities, support, staff per year (USD)")
    p.add_argument("--utilization", type=float, default=0.6, help="expected average utilization, 0-1")
    p.add_argument("--cloud-rate", type=float, default=4.0,
                   help="blended cloud cost per used GPU-hour incl. egress/storage (USD)")
    a = p.parse_args()

    if not 0 < a.utilization <= 1:
        p.error("--utilization must be between 0 and 1")

    on_prem = on_prem_cost_per_used_hour(a.gpus, a.hardware_cost, a.years, a.annual_opex, a.utilization)
    be = break_even_utilization(a.gpus, a.hardware_cost, a.years, a.annual_opex, a.cloud_rate)

    print(f"On-prem cost per used GPU-hour at {a.utilization:.0%} utilization: ${on_prem:,.2f}")
    print(f"Cloud cost per used GPU-hour:                       ${a.cloud_rate:,.2f}")
    if be > 1:
        print("Break-even utilization: above 100% -> cloud is cheaper at any utilization")
    else:
        print(f"Break-even utilization:                             {be:.0%}")
    verdict = "on-prem" if on_prem < a.cloud_rate else "cloud"
    print(f"At the expected utilization, {verdict} is cheaper.\n")

    print("Utilization sensitivity (on-prem cost per used GPU-hour):")
    for u in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9):
        c = on_prem_cost_per_used_hour(a.gpus, a.hardware_cost, a.years, a.annual_opex, u)
        marker = "  <- cheaper than cloud" if c < a.cloud_rate else ""
        print(f"  {u:>4.0%}  ${c:>7,.2f}{marker}")


if __name__ == "__main__":
    main()
