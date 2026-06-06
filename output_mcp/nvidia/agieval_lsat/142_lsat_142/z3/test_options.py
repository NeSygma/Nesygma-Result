from z3 import *

# Define solver
solver = Solver()

# Declare position variables for each role
G = Int('G')
K = Int('K')
P = Int('P')
S = Int('S')
T = Int('T')
V = Int('V')

# All positions are distinct and within 1..6
solver.add(Distinct([G, K, P, S, T, V]))
solver.add(G >= 1, G <= 6)
solver.add(K >= 1, K <= 6)
solver.add(P >= 1, P <= 6)
solver.add(S >= 1, S <= 6)
solver.add(T >= 1, T <= 6)
solver.add(V >= 1, V <= 6)

# Constraints
solver.add(G != 4)  # guitarist not fourth
solver.add(P < K)   # percussionist before keyboard
solver.add(V < K)
solver.add(K < G)   # keyboard before guitarist
# S after exactly one of P or T
# Use XOR: (S > P) != (S > T)
# In Z3, we can express as (S > P) != (S > T) using Bools
sp = Bool('sp')
st = Bool('st')
# Actually we can directly use Or/And to encode XOR: (S > P) & ~(S > T) | ~(S > P) & (S > T)
# But easier: use Xor from z3
from z3 import Xor
solver.add(Xor(S > P, S > T))

# Function to test if a given role can be at position 3
def test_role(role_var, role_name):
    s = Solver()
    # copy constraints
    s.add(solver.assertions())
    # add constraint that role_var == 3
    s.add(role_var == 3)
    result = s.check()
    return result == sat, s.model() if result == sat else None

# Test each role
results = {}
for var, name in [(G, "guitarist"), (K, "keyboard"), (P, "percussion"), (S, "sax"), (T, "trumpet"), (V, "violin")]:
    sat, model = test_role(var, name)
    results[name] = (sat, model)

# Print results
for name, (sat, model) in results.items():
    if sat:
        print(f"{name} can be third: SAT")
    else:
        print(f"{name} can be third: UNSAT")