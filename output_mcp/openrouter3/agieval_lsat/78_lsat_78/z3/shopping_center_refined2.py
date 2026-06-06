from z3 import *

solver = Solver()

# Declare position variables for each business
O = Int('optometrist')  # optometrist
P = Int('pharmacy')     # pharmacy
R1 = Int('restaurant1') # first restaurant
R2 = Int('restaurant2') # second restaurant
S = Int('shoe_store')   # shoe store
T = Int('toy_store')    # toy store
V = Int('veterinarian') # veterinarian

# All positions must be between 1 and 7
solver.add(O >= 1, O <= 7)
solver.add(P >= 1, P <= 7)
solver.add(R1 >= 1, R1 <= 7)
solver.add(R2 >= 1, R2 <= 7)
solver.add(S >= 1, S <= 7)
solver.add(T >= 1, T <= 7)
solver.add(V >= 1, V <= 7)

# All positions must be distinct
solver.add(Distinct([O, P, R1, R2, S, T, V]))

# Constraint 1: Pharmacy must be at one end (space 1 or 7)
solver.add(Or(P == 1, P == 7))

# Constraint 2: One restaurant must be at the other end (opposite from pharmacy)
# If P == 1, then one restaurant must be at 7, and the other restaurant cannot be at 1
# If P == 7, then one restaurant must be at 1, and the other restaurant cannot be at 7
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7), And(R1 != 1, R2 != 1)),
    And(P == 7, Or(R1 == 1, R2 == 1), And(R1 != 7, R2 != 7))
))

# Constraint 3: Two restaurants must be separated by at least two other businesses
# |R1 - R2| >= 3
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Constraint 4: Pharmacy must be next to either optometrist or veterinarian
# |P - O| = 1 OR |P - V| = 1
solver.add(Or(
    Or(P - O == 1, O - P == 1),
    Or(P - V == 1, V - P == 1)
))

# Constraint 5: Toy store cannot be next to veterinarian
# |T - V| != 1
solver.add(Not(Or(T - V == 1, V - T == 1)))

# Given constraint: Veterinarian is in space 5
solver.add(V == 5)

# Find all possible solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {
        'O': m[O],
        'P': m[P],
        'R1': m[R1],
        'R2': m[R2],
        'S': m[S],
        'T': m[T],
        'V': m[V]
    }
    solutions.append(sol)
    
    # Blocking clause to find next solution
    solver.add(Or(
        O != m[O],
        P != m[P],
        R1 != m[R1],
        R2 != m[R2],
        S != m[S],
        T != m[T],
        V != m[V]
    ))

print(f"Found {len(solutions)} solutions")
for i, sol in enumerate(solutions):
    print(f"Solution {i+1}: O={sol['O']}, P={sol['P']}, R1={sol['R1']}, R2={sol['R2']}, S={sol['S']}, T={sol['T']}, V={sol['V']}")

# Check which options are always true
always_A = all(sol['O'] == 2 for sol in solutions)
always_B = all(sol['P'] == 7 for sol in solutions)
always_C = all(sol['R1'] == 4 or sol['R2'] == 4 for sol in solutions)
always_D = all(sol['S'] == 6 for sol in solutions)
always_E = all(sol['T'] == 3 for sol in solutions)

print(f"\nOption A (optometrist in space 2): {'Always true' if always_A else 'Not always true'}")
print(f"Option B (pharmacy in space 7): {'Always true' if always_B else 'Not always true'}")
print(f"Option C (restaurant in space 4): {'Always true' if always_C else 'Not always true'}")
print(f"Option D (shoe store in space 6): {'Always true' if always_D else 'Not always true'}")
print(f"Option E (toy store in space 3): {'Always true' if always_E else 'Not always true'}")

# Determine which option must be true
if always_A:
    answer = 'A'
elif always_B:
    answer = 'B'
elif always_C:
    answer = 'C'
elif always_D:
    answer = 'D'
elif always_E:
    answer = 'E'
else:
    answer = None

if answer:
    print(f"\nSTATUS: sat")
    print(f"answer:{answer}")
else:
    print(f"\nSTATUS: unsat")
    print("Refine: No single option is always true")