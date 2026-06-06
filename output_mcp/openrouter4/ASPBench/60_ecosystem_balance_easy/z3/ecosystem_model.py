from z3 import *

solver = Solver()

# ============================================================
# 1. POPULATION VARIABLES (Real numbers for ecological precision)
# ============================================================
Grass   = Real('Grass')
Rabbits = Real('Rabbits')
Foxes   = Real('Foxes')
Hawks   = Real('Hawks')

# Carrying capacities
GRASS_CAP   = 100
RABBITS_CAP = 30
FOXES_CAP   = 10
HAWKS_CAP   = 5

# ============================================================
# 2. CONSUMPTION RATES for each feeding relationship (0.1 to 0.5)
# ============================================================
R_rg = Real('R_rg')   # Rabbits eat Grass
R_fr = Real('R_fr')   # Foxes eat Rabbits
R_hr = Real('R_hr')   # Hawks eat Rabbits
R_hf = Real('R_hf')   # Hawks eat Foxes

# ============================================================
# 3. CONSTRAINTS
# ============================================================

# Constraint 1: Non-negative populations
solver.add(Grass >= 0)
solver.add(Rabbits >= 0)
solver.add(Foxes >= 0)
solver.add(Hawks >= 0)

# Constraint 2: Cannot exceed carrying capacity
solver.add(Grass <= GRASS_CAP)
solver.add(Rabbits <= RABBITS_CAP)
solver.add(Foxes <= FOXES_CAP)
solver.add(Hawks <= HAWKS_CAP)

# Constraint 3: Herbivore sustainable (Rabbits <= 0.5 * Grass)
solver.add(Rabbits <= 0.5 * Grass)

# Constraint 4: Predator sustainable (Foxes <= 0.3 * Rabbits)
solver.add(Foxes <= 0.3 * Rabbits)

# Constraint 5: No extinction (all populations > 0)
solver.add(Grass > 0)
solver.add(Rabbits > 0)
solver.add(Foxes > 0)
solver.add(Hawks > 0)

# Constraint 6: Food web consumption rates between 0.1 and 0.5
solver.add(R_rg >= 0.1)
solver.add(R_rg <= 0.5)
solver.add(R_fr >= 0.1)
solver.add(R_fr <= 0.5)
solver.add(R_hr >= 0.1)
solver.add(R_hr <= 0.5)
solver.add(R_hf >= 0.1)
solver.add(R_hf <= 0.5)

# ============================================================
# 4. ECOLOGICAL BALANCE CONSTRAINTS
# ============================================================

# Prey consumption cannot exceed prey population (sustainability)
# Total rabbits eaten by foxes and hawks cannot exceed rabbit population
solver.add(R_fr * Foxes + R_hr * Hawks <= Rabbits)

# Total grass eaten by rabbits cannot exceed grass population
solver.add(R_rg * Rabbits <= Grass)

# Total foxes eaten by hawks cannot exceed fox population
solver.add(R_hf * Hawks <= Foxes)

# Predators must have sufficient food - each predator species gets enough
# Hawks need both types of prey to survive (minimum consumption threshold)
solver.add(R_hr * Hawks >= 0.05 * Rabbits)   # hawks get at least 5% of rabbits
solver.add(R_hf * Hawks >= 0.05 * Foxes)      # hawks get at least 5% of foxes

# Foxes need enough rabbits
solver.add(R_fr * Foxes >= 0.05 * Rabbits)

# Rabbits need enough grass
solver.add(R_rg * Rabbits >= 0.05 * Grass)

# ============================================================
# 5. SOLVE AND EXTRACT
# ============================================================
print("Solving ecosystem model...")
result = solver.check()

if result == sat:
    m = solver.model()
    
    # Extract values
    grass_val   = float(m[Grass].as_fraction())
    rabbits_val = float(m[Rabbits].as_fraction())
    foxes_val   = float(m[Foxes].as_fraction())
    hawks_val   = float(m[Hawks].as_fraction())
    
    rr_val = float(m[R_rg].as_fraction())
    fr_val = float(m[R_fr].as_fraction())
    hr_val = float(m[R_hr].as_fraction())
    hf_val = float(m[R_hf].as_fraction())
    
    # ============================================================
    # 6. COMPUTE ECOSYSTEM HEALTH METRICS
    # ============================================================
    
    # Biodiversity index: Normalized Simpson's Diversity Index
    total = grass_val + rabbits_val + foxes_val + hawks_val
    proportions = [grass_val/total, rabbits_val/total, foxes_val/total, hawks_val/total]
    # Simpson's Index = 1 - sum(p_i^2)
    simpson = 1 - sum(p*p for p in proportions)
    # Maximum possible Simpson D for 4 species is 0.75 (when all equal)
    biodiversity_index = min(simpson / 0.75, 1.0)
    
    # Stability score: based on how evenly populations use their carrying capacities
    cap_ratios = [grass_val/GRASS_CAP, rabbits_val/RABBITS_CAP,
                  foxes_val/FOXES_CAP, hawks_val/HAWKS_CAP]
    mean_ratio = sum(cap_ratios) / 4
    # Lower variance = more balanced = more stable
    variance = sum((r - mean_ratio)**2 for r in cap_ratios) / 4
    stability_score = 1.0 / (1.0 + variance * 10)  # normalized 0-1
    
    # Sustainability and balance (both true since we found a valid solution)
    sustainability = "true"
    balance = "true"
    
    print("STATUS: sat")
    print()
    print(f"stable_populations = {{")
    print(f"    'Grass': {grass_val:.2f},")
    print(f"    'Rabbits': {rabbits_val:.2f},")
    print(f"    'Foxes': {foxes_val:.2f},")
    print(f"    'Hawks': {hawks_val:.2f}")
    print(f"}}")
    print()
    print(f"food_web = [")
    print(f"    {{'predator': 'Rabbits', 'prey': 'Grass', 'consumption_rate': {rr_val:.3f}}},")
    print(f"    {{'predator': 'Foxes', 'prey': 'Rabbits', 'consumption_rate': {fr_val:.3f}}},")
    print(f"    {{'predator': 'Hawks', 'prey': 'Rabbits', 'consumption_rate': {hr_val:.3f}}},")
    print(f"    {{'predator': 'Hawks', 'prey': 'Foxes', 'consumption_rate': {hf_val:.3f}}}")
    print(f"]")
    print()
    print(f"ecosystem_health.biodiversity_index = {biodiversity_index:.4f}")
    print(f"ecosystem_health.stability_score = {stability_score:.4f}")
    print(f"ecosystem_health.sustainability = {sustainability}")
    print(f"balance_achieved = {balance}")
    
    # Verify all constraints are satisfied
    print()
    print("--- CONSTRAINT VERIFICATION ---")
    print(f"1. Non-negative: All > 0 ✓")
    print(f"2. Capacity: Grass={grass_val:.2f}/{GRASS_CAP}, Rabbits={rabbits_val:.2f}/{RABBITS_CAP}, Foxes={foxes_val:.2f}/{FOXES_CAP}, Hawks={hawks_val:.2f}/{HAWKS_CAP}")
    print(f"3. Herbivore sustainable: Rabbits({rabbits_val:.2f}) <= 0.5*Grass({0.5*grass_val:.2f}): {rabbits_val <= 0.5*grass_val}")
    print(f"4. Predator sustainable: Foxes({foxes_val:.2f}) <= 0.3*Rabbits({0.3*rabbits_val:.2f}): {foxes_val <= 0.3*rabbits_val}")
    print(f"5. No extinction: All > 0 ✓")
    print(f"6. Consumption rates: R_rg={rr_val:.3f}, R_fr={fr_val:.3f}, R_hr={hr_val:.3f}, R_hf={hf_val:.3f}")
    print(f"   All in [0.1, 0.5]: {all(0.1 <= v <= 0.5 for v in [rr_val, fr_val, hr_val, hf_val])}")

elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")