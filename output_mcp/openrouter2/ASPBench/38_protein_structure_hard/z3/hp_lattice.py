from z3 import *

# Problem parameters
sequence = "HPHPHHPHPH"
N = len(sequence)

# Create solver (Optimize for minimization)
opt = Optimize()

# Declare coordinates
x = [Int(f'x_{i}') for i in range(N)]
y = [Int(f'y_{i}') for i in range(N)]

# Helper: encode coordinate to a single Int for Distinct
# Since walk length <= N-1, coordinates are within [-N+1, N-1]
# We'll offset by N to make them non-negative and encode as (x+N)* (2*N) + (y+N)
offset = N
scale = 2*N
encode = [ (x[i] + offset) * scale + (y[i] + offset) for i in range(N) ]

# Self-avoiding walk: all coordinates distinct
opt.add(Distinct(encode))

# Connectivity: consecutive residues adjacent (Manhattan distance 1)
for i in range(N-1):
    opt.add(Abs(x[i] - x[i+1]) + Abs(y[i] - y[i+1]) == 1)

# Define H residues
is_H = [sequence[i] == 'H' for i in range(N)]

# Energy: sum over non-sequential H-H contacts
energy_terms = []
for i in range(N):
    for j in range(i+1, N):
        if abs(i-j) > 1 and is_H[i] and is_H[j]:
            # Adjacent check
            adj = Abs(x[i] - x[j]) + Abs(y[i] - y[j]) == 1
            energy_terms.append(If(adj, -1, 0))

energy = Sum(energy_terms)

# Minimize energy
opt.minimize(energy)

# Check and output
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    # Print coordinates
    for i in range(N):
        xi = model.evaluate(x[i], model_completion=True)
        yi = model.evaluate(y[i], model_completion=True)
        print(f"residue {i+1} ({sequence[i]}): ({xi}, {yi})")
    # Print energy
    energy_val = model.evaluate(energy, model_completion=True)
    print(f"energy = {energy_val}")
elif result == unsat:
    print("STATUS: unsat")
    if True:  # BENCHMARK_MODE assumed True
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")