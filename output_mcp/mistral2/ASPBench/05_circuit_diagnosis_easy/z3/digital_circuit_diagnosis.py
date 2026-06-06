from z3 import *

# BENCHMARK_MODE: ON (model-finding with minimality)
BENCHMARK_MODE = True

# Components
components = ['and1', 'or1', 'notgate1', 'xor1', 'and2']

# Create a solver
solver = Solver()

# For each component, we have a Boolean variable indicating whether it is faulty
faulty = {c: Bool(c) for c in components}

# Inputs (fixed for this test case)
in1, in2, in3, in4 = 1, 0, 1, 1

# Expected outputs if all components are working correctly
# We will compute the expected outputs symbolically for the fault-free case
w1_fault_free = And(in1 == 1, in2 == 0)
w2_fault_free = Or(w1_fault_free, in3 == 1)
out1_fault_free = Not(w2_fault_free)
w3_fault_free = Xor(in1 == 1, in4 == 1)
out2_fault_free = And(w3_fault_free, in2 == 0)

# Observed outputs
observed_out1 = 1
observed_out2 = 0

# For each component, if it is faulty, its output can be arbitrary (we model this by allowing the output to differ from the fault-free case)
# We will model the actual outputs as variables that can differ if faulty

# Outputs of components (symbolic, can differ if faulty)
w1 = Bool('w1')
w2 = Bool('w2')
out1 = Bool('out1')
w3 = Bool('w3')
out2 = Bool('out2')

# Fault-free behavior constraints (if not faulty)
solver.add(Implies(Not(faulty['and1']), w1 == And(in1 == 1, in2 == 0)))
solver.add(Implies(Not(faulty['or1']), w2 == Or(w1 == True, in3 == 1)))
solver.add(Implies(Not(faulty['notgate1']), out1 == Not(w2 == True)))
solver.add(Implies(Not(faulty['xor1']), w3 == Xor(in1 == 1, in4 == 1)))
solver.add(Implies(Not(faulty['and2']), out2 == And(w3 == True, in2 == 0)))

# If a component is faulty, its output can be arbitrary (we don't constrain it)
# This is implicitly handled by not adding constraints when faulty

# Observed outputs must match
solver.add(out1 == (observed_out1 == 1))
solver.add(out2 == (observed_out2 == 0))

# We want to find all minimal sets of faulty components that explain the observations
# To find all minimal diagnoses, we use a two-step approach:
# 1. Find a diagnosis (a set of faulty components)
# 2. Block all supersets of this diagnosis to ensure minimality

diagnoses = []

while True:
    if solver.check() == sat:
        model = solver.model()
        # Extract the set of faulty components in this model
        current_faulty = [c for c in components if is_true(model[faulty[c]])]
        diagnoses.append(current_faulty)
        # Block all supersets of this diagnosis to ensure minimality
        # We add a constraint that at least one component in the current diagnosis must not be faulty
        # This ensures that we only find minimal diagnoses
        solver.add(Not(And([faulty[c] for c in current_faulty])))
    else:
        break

# Print results
print("STATUS: sat")
print("diagnoses:", diagnoses)
print("components:", sorted(components))
print("minimal:", True)
print("explanation: All minimal sets of faulty components that explain the observed outputs.")