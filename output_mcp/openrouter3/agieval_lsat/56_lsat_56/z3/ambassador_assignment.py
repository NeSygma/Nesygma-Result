from z3 import *

# Define countries and ambassadors
countries = ['Venezuela', 'Yemen', 'Zambia']
ambassadors = ['Jaramillo', 'Kayne', 'Landon', 'Novetzke', 'Ong']

# Create assignment variables: assign[country] = ambassador
assign = {c: Int(f'assign_{c}') for c in countries}

# Map ambassador names to integers for easier constraint handling
amb_to_int = {amb: i for i, amb in enumerate(ambassadors)}
int_to_amb = {i: amb for amb, i in amb_to_int.items()}

# Base constraints
solver = Solver()

# 1. Each country gets exactly one ambassador, and each ambassador assigned to at most one country
# All assignments must be valid ambassador indices
for c in countries:
    solver.add(assign[c] >= 0)
    solver.add(assign[c] < len(ambassadors))

# All assignments must be distinct (no ambassador assigned to multiple countries)
solver.add(Distinct([assign[c] for c in countries]))

# 2. Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships
# This means exactly one of Kayne or Novetzke appears in the assignments
kayne_idx = amb_to_int['Kayne']
novetzke_idx = amb_to_int['Novetzke']

# Count how many times Kayne appears (0 or 1)
kayne_count = Sum([If(assign[c] == kayne_idx, 1, 0) for c in countries])
# Count how many times Novetzke appears (0 or 1)
novetzke_count = Sum([If(assign[c] == novetzke_idx, 1, 0) for c in countries])

# Exactly one of them is assigned
solver.add(kayne_count + novetzke_count == 1)

# 3. If Jaramillo is assigned, then Kayne is assigned
jaramillo_idx = amb_to_int['Jaramillo']
jaramillo_count = Sum([If(assign[c] == jaramillo_idx, 1, 0) for c in countries])

# If Jaramillo appears (count > 0), then Kayne must appear (count > 0)
# We can encode: jaramillo_count <= kayne_count (since both are 0 or 1)
solver.add(jaramillo_count <= kayne_count)

# 4. If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
ong_idx = amb_to_int['Ong']
# This constraint will be added conditionally based on the question's premise

# 5. If Landon is assigned, it is to Zambia
landon_idx = amb_to_int['Landon']
landon_count = Sum([If(assign[c] == landon_idx, 1, 0) for c in countries])
# If Landon appears, it must be in Zambia
# We can encode: if Landon is assigned to any country, that country must be Zambia
# This means Landon cannot be assigned to Venezuela or Yemen
solver.add(Or(
    assign['Venezuela'] != landon_idx,
    assign['Yemen'] != landon_idx
))
# Also, if Landon is assigned, it must be to Zambia (so if Zambia gets Landon, that's fine)
# But we need to ensure that if Landon is assigned at all, it's to Zambia
# This is already covered by the above: Landon can only be in Zambia

# Now, the question: If Ong is assigned to Venezuela, then the other two ambassadors assigned could be...
# We need to test each answer choice

# First, add the premise: Ong is assigned to Venezuela
premise = (assign['Venezuela'] == ong_idx)

# Define the answer choices as constraints on the other two countries (Yemen and Zambia)
# Each choice specifies which two ambassadors are assigned to Yemen and Zambia (in some order)

# Option A: Jaramillo and Landon
opt_a = Or(
    And(assign['Yemen'] == amb_to_int['Jaramillo'], assign['Zambia'] == amb_to_int['Landon']),
    And(assign['Yemen'] == amb_to_int['Landon'], assign['Zambia'] == amb_to_int['Jaramillo'])
)

# Option B: Jaramillo and Novetzke
opt_b = Or(
    And(assign['Yemen'] == amb_to_int['Jaramillo'], assign['Zambia'] == amb_to_int['Novetzke']),
    And(assign['Yemen'] == amb_to_int['Novetzke'], assign['Zambia'] == amb_to_int['Jaramillo'])
)

# Option C: Kayne and Landon
opt_c = Or(
    And(assign['Yemen'] == amb_to_int['Kayne'], assign['Zambia'] == amb_to_int['Landon']),
    And(assign['Yemen'] == amb_to_int['Landon'], assign['Zambia'] == amb_to_int['Kayne'])
)

# Option D: Kayne and Novetzke
opt_d = Or(
    And(assign['Yemen'] == amb_to_int['Kayne'], assign['Zambia'] == amb_to_int['Novetzke']),
    And(assign['Yemen'] == amb_to_int['Novetzke'], assign['Zambia'] == amb_to_int['Kayne'])
)

# Option E: Landon and Novetzke
opt_e = Or(
    And(assign['Yemen'] == amb_to_int['Landon'], assign['Zambia'] == amb_to_int['Novetzke']),
    And(assign['Yemen'] == amb_to_int['Novetzke'], assign['Zambia'] == amb_to_int['Landon'])
)

# Now evaluate each option with the premise
found_options = []

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(premise)
    solver.add(constr)
    # Also add constraint 4 (If Ong is assigned to Venezuela, Kayne is not assigned to Yemen)
    # This is part of the base constraints but depends on the premise
    # We add it here since it's conditional on Ong being in Venezuela
    solver.add(Implies(assign['Venezuela'] == ong_idx, assign['Yemen'] != kayne_idx))
    
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")