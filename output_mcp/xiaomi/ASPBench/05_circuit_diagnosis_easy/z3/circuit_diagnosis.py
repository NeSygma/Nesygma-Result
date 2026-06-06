from z3 import *

# Components
components = ['and1', 'or1', 'notgate1', 'xor1', 'and2']

# Boolean variables for whether each component is faulty
faulty = {c: Bool(f'faulty_{c}') for c in components}

# Wire values (symbolic - may differ from expected if upstream component is faulty)
# We model the actual wire values in the circuit
w1 = Bool('w1')   # output of and1
w2 = Bool('w2')   # output of or1
out1 = Bool('out1') # output of notgate1
w3 = Bool('w3')   # output of xor1
out2 = Bool('out2') # output of and2

# Input values (fixed by test case)
in1 = True
in2 = False
in3 = True
in4 = True

def encode_gate_fault(solver, gate_name, output_var, expected_output_expr):
    """
    For a gate: if not faulty, output equals expected computation.
    If faulty, output can be anything (no constraint).
    """
    solver.add(Implies(Not(faulty[gate_name]), output_var == expected_output_expr))

solver = Solver()

# Gate behaviors (only enforced when gate is NOT faulty)
# and1: w1 = in1 AND in2
expected_w1 = And(in1, in2)  # True AND False = False
encode_gate_fault(solver, 'and1', w1, expected_w1)

# or1: w2 = w1 OR in3
expected_w2 = Or(w1, in3)
encode_gate_fault(solver, 'or1', w2, expected_w2)

# notgate1: out1 = NOT w2
expected_out1 = Not(w2)
encode_gate_fault(solver, 'notgate1', out1, expected_out1)

# xor1: w3 = in1 XOR in4
expected_w3 = Xor(in1, in4)  # True XOR True = False
encode_gate_fault(solver, 'xor1', w3, expected_w3)

# and2: out2 = w3 AND in2
expected_out2 = And(w3, in2)
encode_gate_fault(solver, 'and2', out2, expected_out2)

# Observed outputs
solver.add(out1 == True)   # observed out1=1
solver.add(out2 == False)  # observed out2=0

# Now enumerate all minimal diagnoses
# A diagnosis is a set of faulty components that makes the observations consistent.
# We find all minimal ones by iteratively finding solutions and blocking.

all_diagnoses = []

while True:
    if solver.check() != sat:
        break
    m = solver.model()
    
    # Extract which components are faulty in this model
    diagnosis = set()
    for c in components:
        if is_true(m.evaluate(faulty[c])):
            diagnosis.add(c)
    
    all_diagnoses.append(diagnosis)
    
    # Block this exact diagnosis (and any superset that includes exactly these faulty ones)
    # We block by requiring at least one component in this diagnosis to be NOT faulty
    # OR at least one component NOT in this diagnosis to be faulty
    # This blocks exactly this diagnosis set
    block_clauses = []
    for c in components:
        if c in diagnosis:
            block_clauses.append(Not(faulty[c]))
        else:
            block_clauses.append(faulty[c])
    solver.add(Or(block_clauses))

# Filter to keep only minimal diagnoses
minimal_diagnoses = []
for d in all_diagnoses:
    is_minimal = True
    for other in all_diagnoses:
        if other < d:  # other is a proper subset of d
            is_minimal = False
            break
    if is_minimal:
        minimal_diagnoses.append(d)

# Sort each diagnosis alphabetically and sort the list for consistent output
sorted_diagnoses = sorted([sorted(list(d)) for d in minimal_diagnoses])

print("STATUS: sat")
print(f"Total diagnoses found: {len(all_diagnoses)}")
print(f"Minimal diagnoses: {len(sorted_diagnoses)}")
print()
for i, diag in enumerate(sorted_diagnoses):
    print(f"Diagnosis {i+1}: {{{', '.join(diag)}}}")

# Print structured output
print()
print("=== STRUCTURED OUTPUT ===")
print(f"diagnoses: {sorted_diagnoses}")
print(f"components: {sorted(components)}")
print(f"minimal: true")
print(f"explanation: Found {len(sorted_diagnoses)} minimal diagnosis(es) explaining out1=1 (expected 0) while out2=0 matches. Each diagnosis identifies a minimal set of faulty components whose malfunction is sufficient to produce the observed outputs.")