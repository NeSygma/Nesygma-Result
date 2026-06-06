from z3 import *
import itertools, json

# Component names
components = ['and1', 'or1', 'notgate1', 'xor1', 'and2']
# Input values (as Booleans)
in1 = BoolVal(True)
in2 = BoolVal(False)
in3 = BoolVal(True)
in4 = BoolVal(True)
# Observed outputs
obs_out1 = BoolVal(True)   # 1
obs_out2 = BoolVal(False)  # 0

# Function to build solver for a given fault set

def build_solver(fault_set):
    s = Solver()
    # Fault Bool variables (optional, but we can just use membership)
    f_and1 = Bool('f_and1')
    f_or1 = Bool('f_or1')
    f_notgate1 = Bool('f_notgate1')
    f_xor1 = Bool('f_xor1')
    f_and2 = Bool('f_and2')
    # Assign fault status
    s.add(f_and1 == ("and1" in fault_set))
    s.add(f_or1 == ("or1" in fault_set))
    s.add(f_notgate1 == ("notgate1" in fault_set))
    s.add(f_xor1 == ("xor1" in fault_set))
    s.add(f_and2 == ("and2" in fault_set))
    # Wire variables
    w1 = Bool('w1')
    w2 = Bool('w2')
    w3 = Bool('w3')
    out1 = Bool('out1')
    out2 = Bool('out2')
    # Component constraints when not faulty
    # and1: w1 == in1 AND in2
    s.add(Implies(Not(f_and1), w1 == And(in1, in2)))
    # or1: w2 == w1 OR in3
    s.add(Implies(Not(f_or1), w2 == Or(w1, in3)))
    # notgate1: out1 == NOT w2
    s.add(Implies(Not(f_notgate1), out1 == Not(w2)))
    # xor1: w3 == Xor(in1, in4)
    s.add(Implies(Not(f_xor1), w3 == Xor(in1, in4)))
    # and2: out2 == w3 AND in2
    s.add(Implies(Not(f_and2), out2 == And(w3, in2)))
    # Observed outputs must match
    s.add(out1 == obs_out1)
    s.add(out2 == obs_out2)
    return s

# Find all diagnosis subsets (that make the system SAT)
diag_subsets = []
for r in range(len(components)+1):
    for subset in itertools.combinations(components, r):
        s = build_solver(set(subset))
        if s.check() == sat:
            diag_subsets.append(set(subset))

# Filter minimal diagnoses
minimal_diags = []
for d in diag_subsets:
    # check if any proper subset is also a diagnosis
    is_min = True
    for r in range(len(d)):
        for sub in itertools.combinations(d, r):
            sub_set = set(sub)
            if sub_set != d and sub_set in diag_subsets:
                is_min = False
                break
        if not is_min:
            break
    if is_min:
        minimal_diags.append(d)

# Sort each diagnosis alphabetically and sort list of diagnoses
sorted_diags = [sorted(list(d)) for d in minimal_diags]
sorted_diags.sort()

print("STATUS: sat")
print("diagnoses =", json.dumps(sorted_diags))
print("components =", json.dumps(components))
print("minimal = true")
print("explanation = All minimal sets of faulty components that explain the observed discrepancy.")