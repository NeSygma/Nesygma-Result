from z3 import *

# Same setup as before
photo = [Int(f'photo_{i}') for i in range(6)]
solver = Solver()

# Domain constraints
for i in range(6):
    solver.add(Or(photo[i] == 0, photo[i] == 1, photo[i] == 2))

# Photographer counts
f_count = Sum([If(photo[i] == 0, 1, 0) for i in range(6)])
g_count = Sum([If(photo[i] == 1, 1, 0) for i in range(6)])
h_count = Sum([If(photo[i] == 2, 1, 0) for i in range(6)])

solver.add(f_count >= 1, f_count <= 3)
solver.add(g_count >= 1, g_count <= 3)
solver.add(h_count >= 1, h_count <= 3)

# Lifestyle-Metro photographer overlap constraint
lifestyle_has_f = Or(photo[0] == 0, photo[1] == 0)
lifestyle_has_g = Or(photo[0] == 1, photo[1] == 1)
lifestyle_has_h = Or(photo[0] == 2, photo[1] == 2)

metro_has_f = Or(photo[2] == 0, photo[3] == 0)
metro_has_g = Or(photo[2] == 1, photo[3] == 1)
metro_has_h = Or(photo[2] == 2, photo[3] == 2)

solver.add(Or(
    And(lifestyle_has_f, metro_has_f),
    And(lifestyle_has_g, metro_has_g),
    And(lifestyle_has_h, metro_has_h)
))

# Hue in Lifestyle = Fuentes in Sports
h_lifestyle = Sum([If(photo[i] == 2, 1, 0) for i in range(2)])
f_sports = Sum([If(photo[i] == 0, 1, 0) for i in range(4, 6)])
solver.add(h_lifestyle == f_sports)

# No Gagnon in Sports
solver.add(photo[4] != 1)
solver.add(photo[5] != 1)

# Question condition: one Gagnon and one Hue in Lifestyle
solver.add(Or(
    And(photo[0] == 1, photo[1] == 2),
    And(photo[0] == 2, photo[1] == 1)
))

# Find all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = tuple(m[photo[i]].as_long() for i in range(6))
    solutions.append(sol)
    # Block this solution
    solver.add(Or([photo[i] != m[photo[i]] for i in range(6)]))

print(f"Found {len(solutions)} solutions:")
for i, sol in enumerate(solutions):
    print(f"Solution {i+1}: {sol}")
    # Decode
    photographers = ["F", "G", "H"]
    print(f"  Lifestyle: {photographers[sol[0]]}, {photographers[sol[1]]}")
    print(f"  Metro: {photographers[sol[2]]}, {photographers[sol[3]]}")
    print(f"  Sports: {photographers[sol[4]]}, {photographers[sol[5]]}")
    
    # Check counts
    f_count = sum(1 for p in sol if p == 0)
    g_count = sum(1 for p in sol if p == 1)
    h_count = sum(1 for p in sol if p == 2)
    print(f"  Counts: F={f_count}, G={g_count}, H={h_count}")
    
    # Check options
    f_metro = sum(1 for i in [2,3] if sol[i] == 0)
    g_metro = sum(1 for i in [2,3] if sol[i] == 1)
    h_sports = sum(1 for i in [4,5] if sol[i] == 2)
    print(f"  Options: A={f_metro==1}, B={g_metro==1}, C={g_metro==2}, D={h_sports==1}, E={h_sports==2}")
    print()