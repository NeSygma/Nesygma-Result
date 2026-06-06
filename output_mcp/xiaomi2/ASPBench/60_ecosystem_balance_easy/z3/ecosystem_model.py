from z3 import *

solver = Solver()

# === SPECIES POPULATIONS (Real for fractional ecological ratios) ===
grass = Real('grass')
rabbits = Real('rabbits')
foxes = Real('foxes')
hawks = Real('hawks')

# === CARRYING CAPACITIES ===
CC_GRASS = 100
CC_RABBITS = 30
CC_FOXES = 10
CC_HAWKS = 5

# === CONSUMPTION RATES (Food Web) ===
cr_rabbits_grass = Real('cr_rabbits_grass')   # Rabbits consume Grass
cr_foxes_rabbits = Real('cr_foxes_rabbits')   # Foxes consume Rabbits
cr_hawks_rabbits = Real('cr_hawks_rabbits')   # Hawks consume Rabbits
cr_hawks_foxes = Real('cr_hawks_foxes')       # Hawks consume Foxes

# ============================================================
# CONSTRAINT 1: Non-negative populations
# ============================================================
solver.add(grass >= 0, rabbits >= 0, foxes >= 0, hawks >= 0)

# ============================================================
# CONSTRAINT 2: Populations cannot exceed carrying capacity
# ============================================================
solver.add(grass <= CC_GRASS)
solver.add(rabbits <= CC_RABBITS)
solver.add(foxes <= CC_FOXES)
solver.add(hawks <= CC_HAWKS)

# ============================================================
# CONSTRAINT 3: Herbivore sustainability (Rabbits ≤ 0.5 × Grass)
# ============================================================
solver.add(rabbits <= 0.5 * grass)

# ============================================================
# CONSTRAINT 4: Predator sustainability (Foxes ≤ 0.3 × Rabbits)
# ============================================================
solver.add(foxes <= 0.3 * rabbits)

# ============================================================
# CONSTRAINT 5: No species can go extinct (all > 0)
# ============================================================
solver.add(grass > 0, rabbits > 0, foxes > 0, hawks > 0)

# ============================================================
# CONSTRAINT 6: Consumption rates between 0.1 and 0.5
# ============================================================
solver.add(cr_rabbits_grass >= 0.1, cr_rabbits_grass <= 0.5)
solver.add(cr_foxes_rabbits >= 0.1, cr_foxes_rabbits <= 0.5)
solver.add(cr_hawks_rabbits >= 0.1, cr_hawks_rabbits <= 0.5)
solver.add(cr_hawks_foxes >= 0.1, cr_hawks_foxes <= 0.5)

# ============================================================
# ADDITIONAL ECOLOGICAL CONSTRAINTS (Food Web Balance)
# ============================================================

# Hawks sustainability: Hawks eat both rabbits and foxes
# Hawks must be supportable by available prey biomass
solver.add(hawks <= 0.2 * rabbits + 0.3 * foxes)

# Consumption must not exceed available prey
# Rabbits eating grass: total consumption ≤ grass available
solver.add(cr_rabbits_grass * rabbits <= grass)

# Foxes eating rabbits: total consumption ≤ rabbits available
solver.add(cr_foxes_rabbits * foxes <= rabbits)

# Hawks eating rabbits: portion of rabbit consumption by hawks ≤ rabbits
solver.add(cr_hawks_rabbits * hawks <= rabbits)

# Hawks eating foxes: portion of fox consumption by hawks ≤ foxes
solver.add(cr_hawks_foxes * hawks <= foxes)

# Total predation on rabbits must not exceed rabbit population
solver.add(cr_foxes_rabbits * foxes + cr_hawks_rabbits * hawks <= rabbits)

# ============================================================
# ECOSYSTEM HEALTH METRICS
# ============================================================

# Biodiversity index: average of population-to-capacity ratios (0-1)
biodiversity_index = Real('biodiversity_index')
solver.add(biodiversity_index == (
    grass / CC_GRASS +
    rabbits / CC_RABBITS +
    foxes / CC_FOXES +
    hawks / CC_HAWKS
) / 4)
solver.add(biodiversity_index >= 0, biodiversity_index <= 1)

# Stability score: minimum headroom across all species (0-1)
# Measures how resilient the ecosystem is to perturbations
stability_score = Real('stability_score')
solver.add(stability_score >= 0, stability_score <= 1)
solver.add(stability_score <= 1 - grass / CC_GRASS)
solver.add(stability_score <= 1 - rabbits / CC_RABBITS)
solver.add(stability_score <= 1 - foxes / CC_FOXES)
solver.add(stability_score <= 1 - hawks / CC_HAWKS)

# Sustainability: True if all constraints are satisfied (model exists)
sustainability = Bool('sustainability')
solver.add(sustainability == True)

# Balance achieved: True if ecological balance constraints hold
balance_achieved = Bool('balance_achieved')
solver.add(balance_achieved == True)

# ============================================================
# SOLVE
# ============================================================
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("=== Stable Populations ===")
    print(f"stable_populations.Grass = {m[grass]}")
    print(f"stable_populations.Rabbits = {m[rabbits]}")
    print(f"stable_populations.Foxes = {m[foxes]}")
    print(f"stable_populations.Hawks = {m[hawks]}")
    print()
    print("=== Food Web (Consumption Rates) ===")
    print(f"food_web.Rabbits_eat_Grass.rate = {m[cr_rabbits_grass]}")
    print(f"food_web.Foxes_eat_Rabbits.rate = {m[cr_foxes_rabbits]}")
    print(f"food_web.Hawks_eat_Rabbits.rate = {m[cr_hawks_rabbits]}")
    print(f"food_web.Hawks_eat_Foxes.rate = {m[cr_hawks_foxes]}")
    print()
    print("=== Ecosystem Health ===")
    print(f"ecosystem_health.biodiversity_index = {m[biodiversity_index]}")
    print(f"ecosystem_health.stability_score = {m[stability_score]}")
    print(f"ecosystem_health.sustainability = {m[sustainability]}")
    print(f"balance_achieved = {m[balance_achieved]}")
    print()
    # Verify constraints in model
    print("=== Verification ===")
    g = m[grass].as_fraction()
    r = m[rabbits].as_fraction()
    f = m[foxes].as_fraction()
    h = m[hawks].as_fraction()
    print(f"Rabbits/Grass ratio = {float(r)/float(g):.4f} (limit: 0.5)")
    print(f"Foxes/Rabbits ratio = {float(f)/float(r):.4f} (limit: 0.3)")
    print(f"Grass utilization = {float(g)/CC_GRASS:.4f}")
    print(f"Rabbits utilization = {float(r)/CC_RABBITS:.4f}")
    print(f"Foxes utilization = {float(f)/CC_FOXES:.4f}")
    print(f"Hawks utilization = {float(h)/CC_HAWKS:.4f}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")