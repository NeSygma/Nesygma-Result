from z3 import *

# We have 7 spaces (1-7). We'll assign each business a space number.
# Businesses: optometrist (O), pharmacy (P), restaurant1 (R1), restaurant2 (R2),
# shoe store (S), toy store (T), veterinarian (V)
# All distinct spaces 1-7.

O, P, R1, R2, S, T, V = Ints('O P R1 R2 S T V')
businesses = [O, P, R1, R2, S, T, V]

solver = Solver()

# Domain: each business in space 1..7
for b in businesses:
    solver.add(b >= 1, b <= 7)

# All different spaces
solver.add(Distinct(businesses))

# Constraint 1: The pharmacy must be at one end of the row and one of the restaurants at the other.
# Ends are space 1 and space 7.
solver.add(Or(P == 1, P == 7))
solver.add(Or(R1 == 1, R1 == 7, R2 == 1, R2 == 7))
# The pharmacy and the restaurant at the other end must be at opposite ends.
# If P == 1 then one restaurant is at 7; if P == 7 then one restaurant is at 1.
solver.add(Implies(P == 1, Or(R1 == 7, R2 == 7)))
solver.add(Implies(P == 7, Or(R1 == 1, R2 == 1)))

# Constraint 2: The two restaurants must be separated by at least two other businesses.
# |R1 - R2| >= 3 (since at least 2 businesses between means difference >= 3)
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Constraint 3: The pharmacy must be next to either the optometrist or the veterinarian.
# Next to means |P - O| == 1 or |P - V| == 1
solver.add(Or(Abs(P - O) == 1, Abs(P - V) == 1))

# Constraint 4: The toy store cannot be next to the veterinarian.
# |T - V| != 1
solver.add(Abs(T - V) != 1)

# Now we need to check which option, when substituted for constraint 2 (restaurants separated by at least 2),
# has the same effect. That means: the set of all valid assignments under the original constraints
# should be identical to the set under the modified constraints (with constraint 2 replaced by the option).

# First, let's find all solutions under the original constraints.
# We'll collect all solutions as tuples of (O,P,R1,R2,S,T,V).

def get_all_solutions(s):
    """Given a solver with constraints, return list of all models as tuples."""
    solutions = []
    while s.check() == sat:
        m = s.model()
        sol = (m[O].as_long(), m[P].as_long(), m[R1].as_long(), m[R2].as_long(),
               m[S].as_long(), m[T].as_long(), m[V].as_long())
        solutions.append(sol)
        # Block this solution
        s.add(Or([b != m[b].as_long() for b in businesses]))
    return solutions

# Get original solutions
solver_orig = Solver()
for b in businesses:
    solver_orig.add(b >= 1, b <= 7)
solver_orig.add(Distinct(businesses))
solver_orig.add(Or(P == 1, P == 7))
solver_orig.add(Or(R1 == 1, R1 == 7, R2 == 1, R2 == 7))
solver_orig.add(Implies(P == 1, Or(R1 == 7, R2 == 7)))
solver_orig.add(Implies(P == 7, Or(R1 == 1, R2 == 1)))
solver_orig.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))
solver_orig.add(Or(Abs(P - O) == 1, Abs(P - V) == 1))
solver_orig.add(Abs(T - V) != 1)

orig_solutions = get_all_solutions(solver_orig)
print(f"Original solutions count: {len(orig_solutions)}")
# for sol in sorted(orig_solutions):
#     print(sol)

# Now test each option by replacing constraint 2 with the option's constraint.
# We need to check if the set of solutions is exactly the same.

# Option A: A restaurant must be in either space 3, space 4, or space 5.
# i.e., R1 in {3,4,5} or R2 in {3,4,5}
def opt_a(s):
    s.add(Or(Or(R1 == 3, R1 == 4, R1 == 5), Or(R2 == 3, R2 == 4, R2 == 5)))

# Option B: A restaurant must be next to either the optometrist or the veterinarian.
# i.e., |R1 - O| == 1 or |R1 - V| == 1 or |R2 - O| == 1 or |R2 - V| == 1
def opt_b(s):
    s.add(Or(Abs(R1 - O) == 1, Abs(R1 - V) == 1, Abs(R2 - O) == 1, Abs(R2 - V) == 1))

# Option C: Either the toy store or the veterinarian must be somewhere between the two restaurants.
# Between means: min(R1,R2) < T < max(R1,R2) or min(R1,R2) < V < max(R1,R2)
def opt_c(s):
    s.add(Or(
        And(R1 < T, T < R2),
        And(R2 < T, T < R1),
        And(R1 < V, V < R2),
        And(R2 < V, V < R1)
    ))

# Option D: No more than two businesses can separate the pharmacy and the restaurant nearest it.
# "No more than two businesses separate" means the distance (in spaces) is at most 3.
# The restaurant nearest the pharmacy: min(|P-R1|, |P-R2|) <= 3
def opt_d(s):
    s.add(Or(Abs(P - R1) <= 3, Abs(P - R2) <= 3))

# Option E: The optometrist cannot be next to the shoe store.
# |O - S| != 1
def opt_e(s):
    s.add(Abs(O - S) != 1)

# For each option, build a solver with all original constraints EXCEPT constraint 2,
# and add the option constraint instead. Then compare solution sets.

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []

for letter, opt_fn in options:
    s = Solver()
    for b in businesses:
        s.add(b >= 1, b <= 7)
    s.add(Distinct(businesses))
    s.add(Or(P == 1, P == 7))
    s.add(Or(R1 == 1, R1 == 7, R2 == 1, R2 == 7))
    s.add(Implies(P == 1, Or(R1 == 7, R2 == 7)))
    s.add(Implies(P == 7, Or(R1 == 1, R2 == 1)))
    # Replace constraint 2 with the option
    opt_fn(s)
    s.add(Or(Abs(P - O) == 1, Abs(P - V) == 1))
    s.add(Abs(T - V) != 1)
    
    opt_solutions = get_all_solutions(s)
    print(f"Option {letter} solutions count: {len(opt_solutions)}")
    
    # Check if the solution sets are identical
    if set(opt_solutions) == set(orig_solutions):
        found_options.append(letter)
        print(f"Option {letter} MATCHES original")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")