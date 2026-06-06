from z3 import *

solver = Solver()

# Buildings and their classes
buildings = {
    'Garza': 1, 'Yates': 3, 'Zimmer': 3,   # RealProp initial
    'Flores': 1, 'Lynch': 2,                 # Southco initial
    'King': 2, 'Meyer': 2, 'Ortiz': 2        # Trustcorp initial
}

RP, SC, TC = 0, 1, 2
building_names = list(buildings.keys())

# Owner of each building (0=RealProp, 1=Southco, 2=Trustcorp)
owner = {b: Int(f'owner_{b}') for b in building_names}

# Each owner must be 0, 1, or 2
for b in building_names:
    solver.add(Or(owner[b] == RP, owner[b] == SC, owner[b] == TC))

# INVARIANT: 4*c1 + 2*c2 + c3 = 6 for each company
# This is preserved by all three trade types:
#   Type 1 (same class swap): no count change
#   Type 2 (1 c1 <-> 2 c2): delta = 4*(-1)+2*(2)+0 = 0
#   Type 3 (1 c2 <-> 2 c3): delta = 0+2*(-1)+2 = 0
# All companies start with invariant = 6:
#   RP: 4*1 + 2*0 + 2 = 6
#   SC: 4*1 + 2*1 + 0 = 6
#   TC: 4*0 + 2*3 + 0 = 6
for company in [RP, SC, TC]:
    c1 = Sum([If(owner[b] == company, 1, 0) for b in building_names if buildings[b] == 1])
    c2 = Sum([If(owner[b] == company, 1, 0) for b in building_names if buildings[b] == 2])
    c3 = Sum([If(owner[b] == company, 1, 0) for b in building_names if buildings[b] == 3])
    solver.add(4*c1 + 2*c2 + c3 == 6)

# Check each option: "The buildings owned by X are Y and Z" means X owns EXACTLY {Y, Z}
found_options = []

# Option A: RealProp owns exactly {Flores Tower, Garza Tower}
# Both class 1 => c1=2, c2=0, c3=0 => invariant = 4*2+0+0 = 8 != 6 => should be UNSAT
solver.push()
solver.add(owner['Flores'] == RP)
solver.add(owner['Garza'] == RP)
for b in building_names:
    if b not in ['Flores', 'Garza']:
        solver.add(owner[b] != RP)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: Southco owns exactly {Flores Tower, Meyer Building}
# c1=1, c2=1, c3=0 => invariant = 4+2+0 = 6 => should be SAT
solver.push()
solver.add(owner['Flores'] == SC)
solver.add(owner['Meyer'] == SC)
for b in building_names:
    if b not in ['Flores', 'Meyer']:
        solver.add(owner[b] != SC)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: Southco owns exactly {Garza Tower, Lynch Building}
# c1=1, c2=1, c3=0 => invariant = 6 => should be SAT
solver.push()
solver.add(owner['Garza'] == SC)
solver.add(owner['Lynch'] == SC)
for b in building_names:
    if b not in ['Garza', 'Lynch']:
        solver.add(owner[b] != SC)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: Trustcorp owns exactly {Flores Tower, Ortiz Building}
# c1=1, c2=1, c3=0 => invariant = 6 => should be SAT
solver.push()
solver.add(owner['Flores'] == TC)
solver.add(owner['Ortiz'] == TC)
for b in building_names:
    if b not in ['Flores', 'Ortiz']:
        solver.add(owner[b] != TC)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Trustcorp owns exactly {Garza Tower, Meyer Building}
# c1=1, c2=1, c3=0 => invariant = 6 => should be SAT
solver.push()
solver.add(owner['Garza'] == TC)
solver.add(owner['Meyer'] == TC)
for b in building_names:
    if b not in ['Garza', 'Meyer']:
        solver.add(owner[b] != TC)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# The question asks which CANNOT be true (i.e., which is UNSAT)
cannot_be_true = [l for l in ['A','B','C','D','E'] if l not in found_options]

print(f"Options that CAN be true (SAT): {found_options}")
print(f"Options that CANNOT be true (UNSAT): {cannot_be_true}")

if len(cannot_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be_true[0]}")
elif len(cannot_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {cannot_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: All options are possible")