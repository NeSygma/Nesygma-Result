from z3 import *

# Variables: True = Fall, False = Spring
K, L, M, N, O, P = Bools('K L M N O P')
vars = [K, L, M, N, O, P]

# Base constraints (excluding the original condition)
base = []
base.append(M != P)          # M and P cannot be same season
base.append(K == N)         # K and N same season
base.append(Implies(K, O))  # If K in fall then O in fall

# Original condition to be replaced
orig = Implies(M, Not(N))   # If M in fall then N in spring

# Candidate conditions
candA = Implies(L, Not(M))          # If L fall then M spring
candB = Implies(N, P)               # If N fall then P fall
candC = Implies(Not(M), P)          # If M spring then P fall
candD = Implies(Not(N), Not(M))     # If N spring then M spring
candE = Implies(Not(O), Not(N))     # If O spring then N spring

candidates = [
    ("A", candA),
    ("B", candB),
    ("C", candC),
    ("D", candD),
    ("E", candE)
]

solver = Solver()
found_options = []
for letter, cand in candidates:
    solver.push()
    # Add base constraints and condition that candidate differs from original
    solver.add(base)
    # candidate != original  <=> (candidate and Not(original)) or (Not(candidate) and original)
    solver.add(Xor(cand, orig))
    if solver.check() == unsat:
        # No model where they differ => equivalent
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")