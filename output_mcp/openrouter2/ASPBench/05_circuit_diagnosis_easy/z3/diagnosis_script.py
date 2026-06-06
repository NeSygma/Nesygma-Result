from z3 import *
import itertools

# Component names
components = ['and1', 'or1', 'notgate1', 'xor1', 'and2']

# Input constants
in1 = BoolVal(True)
in2 = BoolVal(False)
in3 = BoolVal(True)
in4 = BoolVal(True)

# Observed outputs
out1_obs = BoolVal(True)   # observed out1 = 1
out2_obs = BoolVal(False)  # observed out2 = 0

# Collect all diagnoses (as frozensets of component names)
all_diagnoses = []

# Iterate over all subsets of components
for r in range(len(components)+1):
    for subset in itertools.combinations(components, r):
        faulty = set(subset)
        solver = Solver()
        # Declare output variables
        w1 = Bool('w1')
        w2 = Bool('w2')
        out1 = Bool('out1')
        w3 = Bool('w3')
        out2 = Bool('out2')
        # Add constraints for non-faulty components
        if 'and1' not in faulty:
            solver.add(w1 == And(in1, in2))
        if 'or1' not in faulty:
            solver.add(w2 == Or(w1, in3))
        if 'notgate1' not in faulty:
            solver.add(out1 == Not(w2))
        if 'xor1' not in faulty:
            solver.add(w3 == Xor(in1, in4))
        if 'and2' not in faulty:
            solver.add(out2 == And(w3, in2))
        # Observed outputs
        solver.add(out1 == out1_obs)
        solver.add(out2 == out2_obs)
        # Check satisfiability
        if solver.check() == sat:
            all_diagnoses.append(frozenset(faulty))

# Filter minimal diagnoses
minimal_diagnoses = []
for d in all_diagnoses:
    # A diagnosis is minimal if no proper subset is also a diagnosis
    if not any((sub < d) for sub in all_diagnoses if sub != d):
        minimal_diagnoses.append(d)

# Sort diagnoses for consistent output
sorted_diagnoses = sorted(minimal_diagnoses, key=lambda s: sorted(list(s)))

# Prepare output
print("STATUS: sat")
print("diagnoses:", [sorted(list(d)) for d in sorted_diagnoses])
print("components:", sorted(components))
print("minimal: true")
print("explanation: Found all minimal diagnoses explaining the discrepancy in out1.")