from z3 import *

# Witnesses: Franco (F), Garcia (G), Hong (H), Iturbe (I), Jackson (J)
# Days: Monday=0, Tuesday=1, Wednesday=2

F, G, H, I, J = Ints('F G H I J')
witnesses = [F, G, H, I, J]

solver = Solver()

# Domain: each witness testifies on exactly one day (Mon, Tue, Wed)
for w in witnesses:
    solver.add(0 <= w, w <= 2)

# Constraint 1: Franco does not testify on same day as Garcia
solver.add(F != G)

# Constraint 2: Iturbe testifies on Wednesday
solver.add(I == 2)

# Constraint 3: Exactly two witnesses testify on Tuesday
# Count how many have day == 1
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)

# Constraint 4: Hong does not testify on Monday
solver.add(H != 0)

# Constraint 5: At least one witness testifies on Monday
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)

# Additional condition: Franco testifies on the same day as Hong
solver.add(F == H)

# Now check each answer choice for "must be true"
# For "must be true", we check if NOT(option) is UNSAT

found_options = []

# Option A: Franco is scheduled to testify on Wednesday
solver.push()
solver.add(F != 2)  # Negation: Franco is NOT on Wednesday
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Option B: Garcia is scheduled to testify on Monday
solver.push()
solver.add(G != 0)  # Negation: Garcia is NOT on Monday
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: Garcia is scheduled to testify on Wednesday
solver.push()
solver.add(G != 2)  # Negation: Garcia is NOT on Wednesday
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: Hong is scheduled to testify on Tuesday
solver.push()
solver.add(H != 1)  # Negation: Hong is NOT on Tuesday
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: Iturbe is the only witness scheduled to testify on Wednesday
# Negation: Either Iturbe is not on Wednesday, or some other witness is also on Wednesday
# Iturbe IS on Wednesday (fixed), so negation means some other witness is also on Wednesday
solver.push()
# Check if it's possible that some other witness is also on Wednesday
# If it IS possible, then option E is NOT forced
other_on_wed = Or([w == 2 for w in [F, G, H, J]])
solver.add(other_on_wed)
if solver.check() == unsat:
    # If no other witness can be on Wednesday, then E must be true
    found_options.append("E")
solver.pop()

print(f"Options whose negation is UNSAT (must be true): {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")