from z3 import *

# Countries: Venezuela, Yemen, Zambia
countries = ['Venezuela', 'Yemen', 'Zambia']
# Candidates: Jaramillo, Kayne, Landon, Novetzke, Ong
candidates = ['Jaramillo', 'Kayne', 'Landon', 'Novetzke', 'Ong']

# Create assignment variables: assign[country] = candidate assigned to that country
assign = {c: Int(f'assign_{c}') for c in countries}

# Domain constraints: each country gets a candidate from 0 to 4 (index in candidates list)
solver = Solver()
for c in countries:
    solver.add(assign[c] >= 0)
    solver.add(assign[c] <= 4)

# All different: each country gets a different candidate
solver.add(Distinct([assign[c] for c in countries]))

# Helper functions to get candidate index
def cand_index(name):
    return candidates.index(name)

# Constraint 1: Either Kayne or Novetzke, but not both, is assigned
# This means exactly one of them appears in the assignment
kayne_idx = cand_index('Kayne')
novetzke_idx = cand_index('Novetzke')
# Count how many times Kayne appears in assignments
kayne_assigned = Sum([If(assign[c] == kayne_idx, 1, 0) for c in countries])
novetzke_assigned = Sum([If(assign[c] == novetzke_idx, 1, 0) for c in countries])
solver.add(kayne_assigned + novetzke_assigned == 1)

# Constraint 2: If Jaramillo is assigned, then Kayne is assigned
jaramillo_idx = cand_index('Jaramillo')
jaramillo_assigned = Sum([If(assign[c] == jaramillo_idx, 1, 0) for c in countries])
solver.add(Implies(jaramillo_assigned >= 1, kayne_assigned >= 1))

# Constraint 3: If Ong is assigned to Venezuela, then Kayne is NOT assigned to Yemen
ong_idx = cand_index('Ong')
solver.add(Implies(assign['Venezuela'] == ong_idx, assign['Yemen'] != kayne_idx))

# Constraint 4: If Landon is assigned, it is to Zambia
landon_idx = cand_index('Landon')
landon_assigned = Sum([If(assign[c] == landon_idx, 1, 0) for c in countries])
solver.add(Implies(landon_assigned >= 1, assign['Zambia'] == landon_idx))

# Now test each answer choice
# Each choice is a pair of candidates who are NOT assigned
# We need to add constraints that both are unassigned (i.e., not in any country assignment)

found_options = []

# Option A: Jaramillo and Novetzke are NOT assigned
solver.push()
solver.add(assign['Venezuela'] != jaramillo_idx)
solver.add(assign['Yemen'] != jaramillo_idx)
solver.add(assign['Zambia'] != jaramillo_idx)
solver.add(assign['Venezuela'] != novetzke_idx)
solver.add(assign['Yemen'] != novetzke_idx)
solver.add(assign['Zambia'] != novetzke_idx)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: Jaramillo and Ong are NOT assigned
solver.push()
solver.add(assign['Venezuela'] != jaramillo_idx)
solver.add(assign['Yemen'] != jaramillo_idx)
solver.add(assign['Zambia'] != jaramillo_idx)
solver.add(assign['Venezuela'] != ong_idx)
solver.add(assign['Yemen'] != ong_idx)
solver.add(assign['Zambia'] != ong_idx)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: Kayne and Landon are NOT assigned
solver.push()
solver.add(assign['Venezuela'] != kayne_idx)
solver.add(assign['Yemen'] != kayne_idx)
solver.add(assign['Zambia'] != kayne_idx)
solver.add(assign['Venezuela'] != landon_idx)
solver.add(assign['Yemen'] != landon_idx)
solver.add(assign['Zambia'] != landon_idx)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: Kayne and Novetzke are NOT assigned
solver.push()
solver.add(assign['Venezuela'] != kayne_idx)
solver.add(assign['Yemen'] != kayne_idx)
solver.add(assign['Zambia'] != kayne_idx)
solver.add(assign['Venezuela'] != novetzke_idx)
solver.add(assign['Yemen'] != novetzke_idx)
solver.add(assign['Zambia'] != novetzke_idx)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Landon and Ong are NOT assigned
solver.push()
solver.add(assign['Venezuela'] != landon_idx)
solver.add(assign['Yemen'] != landon_idx)
solver.add(assign['Zambia'] != landon_idx)
solver.add(assign['Venezuela'] != ong_idx)
solver.add(assign['Yemen'] != ong_idx)
solver.add(assign['Zambia'] != ong_idx)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")