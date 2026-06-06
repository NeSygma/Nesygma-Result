from z3 import *

# Countries: V=Venezuela, Y=Yemen, Z=Zambia
# Candidates: J=0(Jaramillo), K=1(Kayne), L=2(Landon), N=3(Novetzke), O=4(Ong)

def make_solver(extra_constraints=None):
    s = Solver()
    V, Y, Z = Ints('V Y Z')
    
    # Each country gets one of the 5 candidates
    s.add(And(V >= 0, V <= 4))
    s.add(And(Y >= 0, Y <= 4))
    s.add(And(Z >= 0, Z <= 4))
    # All different (no ambassador to more than one country)
    s.add(Distinct(V, Y, Z))
    
    # Helper: is candidate c assigned?
    def assigned(c):
        return Or(V == c, Y == c, Z == c)
    
    # Constraint 1: Exactly one of Kayne(1) or Novetzke(3) is assigned
    s.add(Xor(assigned(1), assigned(3)))
    
    # Constraint 3: If Ong(4) assigned to V, Kayne(1) not assigned to Y
    s.add(Implies(V == 4, Y != 1))
    
    # Constraint 4: If Landon(2) assigned, it's to Zambia(Z)
    s.add(Implies(assigned(2), Z == 2))
    
    if extra_constraints:
        for c in extra_constraints:
            s.add(c)
    
    return s, V, Y, Z

def assigned_in_model(m, V, Y, Z, c):
    """Check if candidate c is assigned in model m"""
    return is_true(m.eval(Or(V == c, Y == c, Z == c)))

def get_assignments(solver, V, Y, Z):
    """Enumerate all solutions"""
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = (m.eval(V).as_long(), m.eval(Y).as_long(), m.eval(Z).as_long())
        solutions.append(sol)
        # Block this solution
        solver.add(Not(And(V == sol[0], Y == sol[1], Z == sol[2])))
    return set(solutions)

# --- Get original solutions (with constraint 2) ---
s_orig, V, Y, Z = make_solver()
# Constraint 2: If Jaramillo(0) assigned, then Kayne(1) assigned
s_orig.add(Implies(Or(V == 0, Y == 0, Z == 0), Or(V == 1, Y == 1, Z == 1)))
original_solutions = get_assignments(s_orig, V, Y, Z)

print(f"Original solutions count: {len(original_solutions)}")
for sol in sorted(original_solutions):
    names = {0:'J', 1:'K', 2:'L', 3:'N', 4:'O'}
    print(f"  V={names[sol[0]]}, Y={names[sol[1]]}, Z={names[sol[2]]}")

# --- Define answer options ---
def assigned(c, V, Y, Z):
    return Or(V == c, Y == c, Z == c)

# Option A: If Kayne assigned, then Jaramillo assigned
opt_a = Implies(assigned(1, V, Y, Z), assigned(0, V, Y, Z))

# Option B: If Landon and Ong both assigned, then Novetzke assigned
opt_b = Implies(And(assigned(2, V, Y, Z), assigned(4, V, Y, Z)), assigned(3, V, Y, Z))

# Option C: If Ong not assigned, then Kayne assigned
opt_c = Implies(Not(assigned(4, V, Y, Z)), assigned(1, V, Y, Z))

# Option D: Jaramillo and Novetzke not both assigned
opt_d = Not(And(assigned(0, V, Y, Z), assigned(3, V, Y, Z)))

# Option E: Novetzke and Ong not both assigned
opt_e = Not(And(assigned(3, V, Y, Z), assigned(4, V, Y, Z)))

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

# --- Check each option ---
found_options = []
for letter, opt_constr in options:
    s_opt, Vo, Yo, Zo = make_solver(extra_constraints=[opt_constr])
    opt_solutions = get_assignments(s_opt, Vo, Yo, Zo)
    
    match = (opt_solutions == original_solutions)
    print(f"\nOption {letter}: solutions={len(opt_solutions)}, match={match}")
    for sol in sorted(opt_solutions):
        names = {0:'J', 1:'K', 2:'L', 3:'N', 4:'O'}
        print(f"  V={names[sol[0]]}, Y={names[sol[1]]}, Z={names[sol[2]]}")
    
    if match:
        found_options.append(letter)

print(f"\nMatching options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")