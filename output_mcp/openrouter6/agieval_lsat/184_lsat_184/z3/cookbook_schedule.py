from z3 import *

# Define variables for each cookbook: True if published in fall, False if spring
K = Bool('K')
L = Bool('L')
M = Bool('M')
N = Bool('N')
O = Bool('O')
P = Bool('P')

# Base constraints (1-3)
base = [
    M != P,                # M and P cannot be in the same season
    K == N,                # K and N must be in the same season
    Implies(K, O)          # If K is fall, O must be fall
]

# Original condition (4)
original = Implies(M, Not(N))

# Alternative conditions
alt_A = Implies(L, Not(M))          # If L is fall, M must be spring
alt_B = Implies(N, P)               # If N is fall, P must be fall
alt_C = Implies(Not(M), P)          # If M is spring, P must be fall
alt_D = Implies(Not(N), Not(M))     # If N is spring, M must be spring
alt_E = Implies(Not(O), Not(N))     # If O is spring, N must be spring

alternatives = [
    ("A", alt_A),
    ("B", alt_B),
    ("C", alt_C),
    ("D", alt_D),
    ("E", alt_E)
]

# Function to check if base + original implies alt
def implies_original_alt(alt):
    s = Solver()
    s.add(base)
    s.add(original)
    s.add(Not(alt))
    return s.check() == unsat

# Function to check if base + alt implies original
def implies_alt_original(alt):
    s = Solver()
    s.add(base)
    s.add(alt)
    s.add(Not(original))
    return s.check() == unsat

# Find which alternatives are equivalent to original
found_options = []
for letter, alt in alternatives:
    if implies_original_alt(alt) and implies_alt_original(alt):
        found_options.append(letter)

# Output according to the required skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")