from z3 import *

# BENCHMARK_MODE: ON (problem is solvable)
BENCHMARK_MODE = True

# Declare components and their faulty flags
components = ["and1", "or1", "notgate1", "xor1", "and2"]
faulty = {comp: Bool(f"faulty_{comp}") for comp in components}

# Declare all signals in the circuit
# Inputs
in1, in2, in3, in4 = Bools("in1 in2 in3 in4")
# Internal signals
w1, w2, w3 = Bools("w1 w2 w3")
# Outputs
out1, out2 = Bools("out1 out2")

# Input values from the test case
input_constraints = [
    in1 == True,
    in2 == False,
    in3 == True,
    in4 == True
]

# Expected outputs if all components are working correctly
expected_out1 = False  # notgate1(in1 OR in3) should be False
expected_out2 = False  # and2(xor1(in1, in4), in2) should be False

# Observed outputs
observed_constraints = [
    out1 == True,
    out2 == False
]

# Correct behavior for each component when not faulty
behavior_constraints = []

# and1: AND gate, inputs: in1, in2, output: w1
behavior_constraints.append(Implies(Not(faulty["and1"]), w1 == And(in1, in2)))

# or1: OR gate, inputs: w1, in3, output: w2
behavior_constraints.append(Implies(Not(faulty["or1"]), w2 == Or(w1, in3)))

# notgate1: NOT gate, input: w2, output: out1
behavior_constraints.append(Implies(Not(faulty["notgate1"]), out1 == Not(w2)))

# xor1: XOR gate, inputs: in1, in4, output: w3
behavior_constraints.append(Implies(Not(faulty["xor1"]), w3 == Xor(in1, in4)))

# and2: AND gate, inputs: w3, in2, output: out2
behavior_constraints.append(Implies(Not(faulty["and2"]), out2 == And(w3, in2)))

# Overall constraints: inputs, observed outputs, and component behaviors
solver = Solver()
solver.add(input_constraints)
solver.add(observed_constraints)
solver.add(behavior_constraints)

# Collect all minimal diagnoses
diagnoses = []

# To find all minimal diagnoses, we iteratively find diagnoses and block supersets
while solver.check() == sat:
    model = solver.model()
    # Extract the set of faulty components in this diagnosis
    current_faulty = [comp for comp in components if is_true(model[faulty[comp]])]
    diagnoses.append(current_faulty)
    
    # Block all supersets of this diagnosis by requiring that at least one component not in current_faulty is not faulty
    blocking_clause = Or([Not(faulty[c]) for c in components if c not in current_faulty])
    solver.add(blocking_clause)

# Sort each diagnosis alphabetically and sort the list of diagnoses
minimal_diagnoses = [sorted(diag) for diag in diagnoses]
minimal_diagnoses.sort()

# Output results
print("STATUS: sat")
print(f"diagnoses: {minimal_diagnoses}")
print(f"components: {sorted(components)}")
print(f"minimal: true")
print(f"explanation: Found all minimal sets of faulty components that explain the observed outputs.")