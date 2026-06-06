from z3 import *

# Base constraints for the scheduling problem
solver = Solver()

# Positions 1..7 for each house
houses = ['J','K','L','M','N','O','P']
pos = {h: Int(f'pos_{h}') for h in houses}
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)
# All positions distinct
solver.add(Distinct([pos[h] for h in houses]))

# Time slot categories (not directly needed for constraints, but we can encode if needed)
# Morning: 1,2 ; Afternoon: 3,4,5 ; Evening: 6,7

# Constraints from problem statement
solver.add(Or(pos['J'] == 6, pos['J'] == 7))          # J in evening
solver.add(Not(Or(pos['K'] == 1, pos['K'] == 2)))    # K not in morning
solver.add(pos['K'] < pos['L'], pos['L'] < pos['M']) # L after K and before M

# Options definitions: adjacency constraint (|posA - posB| == 1)
options = {
    'A': ('J','K'),
    'B': ('J','M'),
    'C': ('J','O'),
    'D': ('J','P'),
    'E': ('M','P')
}

found_options = []
all_letters = list(options.keys())
for letter, (a,b) in options.items():
    solver.push()
    # adjacency constraint
    solver.add(Or(pos[a] - pos[b] == 1, pos[b] - pos[a] == 1))
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine the pair that CANNOT be consecutive (i.e., the one NOT in found_options)
cannot = [l for l in all_letters if l not in found_options]
if len(cannot) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot[0]}")
elif len(found_options) == 1:
    # fallback: if exactly one CAN be consecutive, treat it as answer (unlikely)
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: ambiguous result, found_options={found_options}, cannot={cannot}")