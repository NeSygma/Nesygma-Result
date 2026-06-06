from z3 import *

# Define components
components = ['and1', 'or1', 'notgate1', 'xor1', 'and2']

# Create boolean variables for each component's fault status
faulty = {comp: Bool(f'faulty_{comp}') for comp in components}

# Input variables
in1, in2, in3, in4 = Bools('in1 in2 in3 in4')

# Internal wires
w1, w2, w3 = Bools('w1 w2 w3')

# Output variables
out1, out2 = Bools('out1 out2')

# Create solver
solver = Solver()

# Add input constraints (given test case)
solver.add(in1 == True)   # 1
solver.add(in2 == False)  # 0
solver.add(in3 == True)   # 1
solver.add(in4 == True)   # 1

# Add expected output constraints (what should happen if all components work)
# Expected: out1=0, out2=0
expected_out1 = False
expected_out2 = False

# Add observed output constraints
solver.add(out1 == True)   # observed out1=1
solver.add(out2 == False)  # observed out2=0

# Define normal behavior of each gate (when not faulty)
# and1: w1 = in1 AND in2
# or1: w2 = w1 OR in3
# notgate1: out1 = NOT w2
# xor1: w3 = in1 XOR in4
# and2: out2 = w3 AND in2

# For each gate, we need to model: if NOT faulty, then output = normal function
# If faulty, output can be anything (we don't constrain it)

# and1
solver.add(Implies(Not(faulty['and1']), w1 == And(in1, in2)))

# or1
solver.add(Implies(Not(faulty['or1']), w2 == Or(w1, in3)))

# notgate1
solver.add(Implies(Not(faulty['notgate1']), out1 == Not(w2)))

# xor1
solver.add(Implies(Not(faulty['xor1']), w3 == Xor(in1, in4)))

# and2
solver.add(Implies(Not(faulty['and2']), out2 == And(w3, in2)))

# Now we need to find all minimal diagnoses
# A diagnosis is a set of faulty components that makes observations consistent
# We need to find all minimal sets

print("Finding all minimal diagnoses...")
print("=" * 50)

# We'll use a systematic approach:
# 1. Find all possible diagnoses (sets of faulty components)
# 2. Filter for minimal ones (no proper subset is also a diagnosis)

# First, let's find all possible diagnoses by checking all 2^5 = 32 combinations
all_diagnoses = []

for mask in range(1 << len(components)):
    # Create a subset based on the bitmask
    subset = [components[i] for i in range(len(components)) if (mask >> i) & 1]
    
    # Create a temporary solver for this subset
    temp_solver = Solver()
    
    # Add all base constraints
    temp_solver.add(in1 == True)
    temp_solver.add(in2 == False)
    temp_solver.add(in3 == True)
    temp_solver.add(in4 == True)
    temp_solver.add(out1 == True)
    temp_solver.add(out2 == False)
    
    # Add gate constraints
    temp_solver.add(Implies(Not(faulty['and1']), w1 == And(in1, in2)))
    temp_solver.add(Implies(Not(faulty['or1']), w2 == Or(w1, in3)))
    temp_solver.add(Implies(Not(faulty['notgate1']), out1 == Not(w2)))
    temp_solver.add(Implies(Not(faulty['xor1']), w3 == Xor(in1, in4)))
    temp_solver.add(Implies(Not(faulty['and2']), out2 == And(w3, in2)))
    
    # Set the components in the subset as faulty
    for comp in components:
        if comp in subset:
            temp_solver.add(faulty[comp] == True)
        else:
            temp_solver.add(faulty[comp] == False)
    
    # Check if this subset is a diagnosis
    if temp_solver.check() == sat:
        all_diagnoses.append(subset)

print(f"Found {len(all_diagnoses)} possible diagnoses (not necessarily minimal)")
print()

# Now filter for minimal diagnoses
minimal_diagnoses = []
for diag in all_diagnoses:
    is_minimal = True
    for other_diag in all_diagnoses:
        if diag != other_diag and set(other_diag).issubset(set(diag)):
            is_minimal = False
            break
    if is_minimal:
        minimal_diagnoses.append(diag)

print(f"Found {len(minimal_diagnoses)} minimal diagnoses:")
print()

# Sort components alphabetically within each diagnosis and print
for i, diag in enumerate(minimal_diagnoses, 1):
    sorted_diag = sorted(diag)
    print(f"Diagnosis {i}: {sorted_diag}")

print()
print("=" * 50)
print("Summary:")
print(f"components: {components}")
print(f"minimal: true")
print(f"explanation: Found {len(minimal_diagnoses)} minimal diagnosis sets that explain the discrepancy")
print()
print("STATUS: sat")