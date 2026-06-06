from z3 import *

solver = Solver()

# Declare position variables for each singer
K = Int('K')  # Kammer
L = Int('L')  # Lugo
T = Int('T')  # Trillo
W = Int('W')  # Waite
Y = Int('Y')  # Yoshida
Z = Int('Z')  # Zinn

# All positions are between 1 and 6 and distinct
positions = [K, L, T, W, Y, Z]
for p in positions:
    solver.add(p >= 1, p <= 6)
solver.add(Distinct(positions))

# Constraint: fourth audition cannot be recorded -> position 4 is not K or L
solver.add(Or(K != 4, L != 4))  # Actually we need that the singer at position 4 is not K or L.
# More precise: The singer at position 4 is not K and not L.
# We can express: If K == 4 then false, but we can just add K != 4 and L != 4.
solver.add(K != 4)
solver.add(L != 4)

# Constraint: fifth audition must be recorded -> position 5 is K or L
solver.add(Or(K == 5, L == 5))

# Constraint: Waite's audition must take place earlier than the two recorded auditions
solver.add(W < K)
solver.add(W < L)

# Constraint: Kammer's audition must take place earlier than Trillo's audition
solver.add(K < T)

# Constraint: Zinn's audition must take place earlier than Yoshida's audition
solver.add(Z < Y)

# Base constraints added

# Now test each option: which singer cannot be at position 2?
# We'll use the skeleton: for each option, add constraint that singer is at position 2, check sat.
found_options = []
options = [
    ("A", K == 2),   # Kammer's audition
    ("B", L == 2),   # Lugo's audition
    ("C", T == 2),   # Trillo's audition
    ("D", W == 2),   # Waite's audition
    ("E", Z == 2),   # Zinn's audition
]

for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# According to the skeleton, if exactly one option is sat, that's the answer.
# But in this problem, we expect exactly one option to be unsat (cannot be second).
# So found_options should have 4 letters, not 1.
# However, we follow the skeleton and print accordingly.
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")

# Additionally, we compute the answer as the singer that cannot be second.
# The singer not in found_options is the one that cannot be second.
all_letters = [letter for letter, _ in options]
impossible = [letter for letter in all_letters if letter not in found_options]
if len(impossible) == 1:
    # Override the print to give the correct answer
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: Unexpected number of impossible options: {impossible}")