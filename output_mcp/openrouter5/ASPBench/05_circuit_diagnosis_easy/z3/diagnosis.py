from z3 import *

# Components
components = ['and1', 'or1', 'notgate1', 'xor1', 'and2']

# For each component, we have a boolean: is it faulty?
faulty = {c: Bool(f'faulty_{c}') for c in components}

# For each wire, we have the actual (observed) value.
# We model the actual output of each gate given its inputs.
# If a gate is faulty, its output can be anything (0 or 1) — we model this with a free Bool variable.
# If a gate is not faulty, its output is determined by its function.

# Wires
in1, in2, in3, in4 = True, False, True, True  # 1,0,1,1
# Expected outputs: out1=0, out2=0
# Observed outputs: out1=1, out2=0

# Internal wires
w1 = Bool('w1')   # output of and1
w2 = Bool('w2')   # output of or1
w3 = Bool('w3')   # output of xor1
out1 = Bool('out1')  # output of notgate1
out2 = Bool('out2')  # output of and2

solver = Solver()

# --- Gate behavior constraints ---

# and1: if not faulty, w1 = in1 AND in2
solver.add(Implies(Not(faulty['and1']), w1 == And(in1, in2)))

# or1: if not faulty, w2 = w1 OR in3
solver.add(Implies(Not(faulty['or1']), w2 == Or(w1, in3)))

# notgate1: if not faulty, out1 = NOT w2
solver.add(Implies(Not(faulty['notgate1']), out1 == Not(w2)))

# xor1: if not faulty, w3 = in1 XOR in4
solver.add(Implies(Not(faulty['xor1']), w3 == (in1 != in4)))

# and2: if not faulty, out2 = w3 AND in2
solver.add(Implies(Not(faulty['and2']), out2 == And(w3, in2)))

# --- Observation constraints ---
# Observed outputs
solver.add(out1 == True)   # observed out1=1
solver.add(out2 == False)  # observed out2=0

# --- Diagnosis: at least one component must be faulty (otherwise expected outputs would hold) ---
solver.add(Or([faulty[c] for c in components]))

# --- Find all minimal diagnoses ---
# Strategy: enumerate all satisfying assignments to faulty[],
# then filter for minimality.

diagnoses = []

while solver.check() == sat:
    m = solver.model()
    # Get the set of faulty components in this solution
    diag = tuple(sorted([c for c in components if is_true(m.eval(faulty[c]))]))
    diagnoses.append(diag)
    
    # Block this exact diagnosis
    solver.add(Or([faulty[c] != is_true(m.eval(faulty[c])) for c in components]))

# Now filter for minimal diagnoses
# A diagnosis is minimal if no proper subset is also a diagnosis
minimal_diagnoses = []
for d in diagnoses:
    is_minimal = True
    for other in diagnoses:
        if other != d and set(other).issubset(set(d)):
            is_minimal = False
            break
    if is_minimal:
        minimal_diagnoses.append(list(d))

# Sort each diagnosis alphabetically and sort the list
minimal_diagnoses = sorted([sorted(d) for d in minimal_diagnoses])

print("STATUS: sat")
print(f"diagnoses: {minimal_diagnoses}")
print(f"components: {components}")
print(f"minimal: true")
print(f"explanation: All minimal diagnosis sets found that explain out1=1, out2=0")