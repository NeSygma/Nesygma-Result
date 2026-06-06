from z3 import *

# Define countries and ambassadors
countries = ['Venezuela', 'Yemen', 'Zambia']
ambassadors = ['Jaramillo', 'Kayne', 'Landon', 'Novetzke', 'Ong']

# Create assignment variables: assign[country] = ambassador
assign = {c: Int(f'assign_{c}') for c in countries}

# Map ambassador names to integers
amb_to_int = {amb: i for i, amb in enumerate(ambassadors)}
int_to_amb = {i: amb for amb, i in amb_to_int.items()}

# Base constraints
solver = Solver()

# 1. Each country gets exactly one ambassador, and each ambassador assigned to at most one country
for c in countries:
    solver.add(assign[c] >= 0)
    solver.add(assign[c] < len(ambassadors))

# All assignments must be distinct (no ambassador assigned to multiple countries)
solver.add(Distinct([assign[c] for c in countries]))

# 2. Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships
kayne_idx = amb_to_int['Kayne']
novetzke_idx = amb_to_int['Novetzke']

kayne_count = Sum([If(assign[c] == kayne_idx, 1, 0) for c in countries])
novetzke_count = Sum([If(assign[c] == novetzke_idx, 1, 0) for c in countries])

# Exactly one of them is assigned
solver.add(kayne_count + novetzke_count == 1)

# 3. If Jaramillo is assigned, then Kayne is assigned
jaramillo_idx = amb_to_int['Jaramillo']
jaramillo_count = Sum([If(assign[c] == jaramillo_idx, 1, 0) for c in countries])

# If Jaramillo appears (count > 0), then Kayne must appear (count > 0)
solver.add(jaramillo_count <= kayne_count)

# 4. If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
ong_idx = amb_to_int['Ong']
# This is a conditional constraint that should always be in effect
solver.add(Implies(assign['Venezuela'] == ong_idx, assign['Yemen'] != kayne_idx))

# 5. If Landon is assigned, it is to Zambia
landon_idx = amb_to_int['Landon']
# Landon can only be assigned to Zambia (cannot be assigned to Venezuela or Yemen)
solver.add(assign['Venezuela'] != landon_idx)
solver.add(assign['Yemen'] != landon_idx)

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