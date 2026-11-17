# GPU cloud vs on-prem: a TCO framework

## The question

"Should we buy GPUs or rent them?" The answer turns almost entirely on **utilization** and **time horizon**. Owned hardware has low marginal cost but high fixed cost. Rented capacity costs more per hour but nothing when idle. The PM's job is to make those inputs explicit, test them against real demand data, and show where the break-even sits.

## The model

### On-prem effective cost per *used* GPU-hour

```
annual_capex      = hardware_cost / depreciation_years
annual_opex       = power_and_cooling + facilities + network_and_storage
                    + support_contracts + operations_staff
annual_gpu_hours  = gpu_count × 8,760 × utilization

on_prem_cost_per_used_gpu_hour = (annual_capex + annual_opex) / annual_gpu_hours
```

### Cloud effective cost per *used* GPU-hour

```
cloud_cost_per_used_gpu_hour = blended_hourly_rate
                               + data_egress_and_storage_per_hour
                               + idle_reserved_capacity_overhead
```

The *blended* rate mixes on-demand, reserved/committed, and spot capacity in the proportions you'd actually use.

### Break-even utilization

The utilization at which owning and renting cost the same:

```
break_even_utilization = (annual_capex + annual_opex)
                         / (gpu_count × 8,760 × cloud_cost_per_used_gpu_hour)
```

Above this, owning is cheaper. Below it, renting is cheaper.

## Inputs checklist

| Input | Where to get it | Common mistake |
|---|---|---|
| Hardware cost (servers, GPUs, NICs, switches, optics, racks) | Vendor quotes | Forgetting optics and cabling, which can be a large share of fabric cost |
| Depreciation period | Finance | Using a longer life than GPU generations actually stay competitive |
| Power and cooling | Facilities; kW per rack × energy cost × PUE | Ignoring that dense GPU racks may need liquid cooling or facility upgrades |
| Operations staff | Headcount plan | Assuming existing staff can absorb a new fabric and GPU stack |
| Utilization | Scheduler data, demand forecast | Planning on peak demand instead of the realistic average |
| Cloud blended rate | Provider pricing and commit discounts | Comparing against on-demand list price only |
| Data egress and storage | Cloud bill / architecture | Leaving out moving large datasets and checkpoints in and out |

## Non-cost factors that can override the math

- **Time to capacity:** cloud or GPU-cloud capacity may be available in weeks; an on-prem build can take quarters
- **Technology refresh:** renting avoids being stuck on an older generation
- **Data gravity and residency:** sensitive data or regulatory limits may favor on-prem or a specific region
- **Control and security:** owning the full stack simplifies some security and audit requirements
- **Optionality:** a hybrid model (a baseline you own, burst capacity you rent) often wins in practice

## Using the calculator

[`tools/gpu_tco_calculator.py`](../tools/gpu_tco_calculator.py) runs this model so you can compare scenarios quickly:

```bash
python tools/gpu_tco_calculator.py --gpus 64 --hardware-cost 3000000 \
  --years 4 --annual-opex 900000 --utilization 0.6 --cloud-rate 4.0
```

It prints on-prem cost per used GPU-hour, cloud cost, the break-even utilization, and a utilization sensitivity table.

**All defaults and examples are illustrative placeholders.** Replace them with your own quotes, rates, and demand data before using the result in a decision.

## How I'd present it

1. One chart: cost per used GPU-hour vs utilization, with the cloud rate as a horizontal line and the break-even point marked
2. The realistic utilization range from demand data, shown as a band on the chart
3. A recommendation (own, rent, or hybrid split) plus the two or three inputs that would change it
