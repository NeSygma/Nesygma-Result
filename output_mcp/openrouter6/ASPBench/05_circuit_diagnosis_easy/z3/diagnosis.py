from z3 import *

# Define component names
components = ['and1', 'or1', 'notgate1', 'xor1', 'and2']

# Boolean variables for faulty status
f_and1 = Bool('f_and1')
f_or1 = Bool('f_or1')
f_notgate1 = Bool('f_notgate1')
f_xor1 = Bool('f_xor1')
f_and2 = Bool('f_and2')
faulty_vars = [f_and1, f_or1, f_notgate1, f_xor1, f_and2]

# Input constants (given)
in1 = 1
in2 = 0
in3 = 1
in4 = 1

# Internal signals and outputs as Boolean variables
w1 = Bool('w1')
w2 = Bool('w2')
out1 = Bool('out1')
w3 = Bool('w3')
out2 = Bool('out2')

# Circuit constraints (if component not faulty, output must match logic)
# and1: w1 = in1 AND in2
solver = Solver()
solver.add(Or(f_and1, w1 == (in1 & in2)))
# or1: w2 = w1 OR in3
solver.add(Or(f_or1, w2 == (w1 | in3)))
# notgate1: out1 = NOT w2
solver.add(Or(f_notgate1, out1 == Not(w2)))
# xor1: w3 = in1 XOR in4
solver.add(Or(f_xor1, w3 == (in1 ^ in4)))
# and2: out2 = w3 AND in2
solver.add(Or(f_and2, out2 == (w3 & in2)))

# Observed outputs
solver.add(out1 == True)   # observed out1 = 1
solver.add(out2 == False)  # observed out2 = 0

# Enumerate all satisfying assignments for faulty variables
diagnoses = []  # list of sets of component names that are faulty
while solver.check() == sat:
    model = solver.model()
    # Determine which components are faulty in this model
    faulty_set = set()
    for comp, var in zip(components, faulty_vars):
        if is_true(model[var]):
            faulty_set.add(comp)
    diagnoses.append(frozen(faulty_set))
    # Blocking clause: exclude this exact assignment
    solver.add(Or([var != model[var] for var in faulty_vars]))

# Filter for minimal diagnoses (no proper subset is also a diagnosis)
minimal_diagnoses = []
for d in diagnoses:
    is_minimal = True
    for other in diagnoses:
        if other != d and other.issubset(d):
            is_minimal = False
            break
    if is_minimal:
        minimal_diagnoses.append(d)

# Prepare output
# List of all faulty component names across minimal diagnoses (sorted)
faulty_components = sorted(set().union(*minimal_diagnoses)) if minimal_diagnoses else []

# Convert diagnoses to sorted lists
diagnoses_lists = [sorted(list(d)) for d in minimal_diagnoses]

# Explanation
explanation = f"Found {len(minimal_diagnoses)} minimal diagnosis sets that explain out1=1 (instead of 0) while out2=0 matches expectation."

# Print results in required format
print("STATUS: sat")
print("diagnoses:", diagnoses_lists)
print("components:", faulty_components)
print("minimal: true")
print("explanation:", explanation)