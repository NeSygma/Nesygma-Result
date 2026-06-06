from z3 import *

# Countries: V=Venezuela, Y=Yemen, Z=Zambia
# Candidates: J=0, K=1, L=2, N=3, O=4
candidates = ['Jaramillo', 'Kayne', 'Landon', 'Novetzke', 'Ong']

def enumerate_solutions(constraint_fn):
    """Enumerate all valid assignments with given constraint function."""
    s = Solver()
    
    # Which candidate is assigned to each country (0-4)
    V = Int('V')  # Venezuela
    Y = Int('Y')  # Yemen
    Z = Int('Z')  # Zambia
    
    # Domain: each country gets one of 5 candidates
    s.add(V >= 0, V <= 4)
    s.add(Y >= 0, Y <= 4)
    s.add(Z >= 0, Z <= 4)
    
    # All different (no ambassador to more than one country)
    s.add(Distinct(V, Y, Z))
    
    # Helper: is candidate c assigned?
    def assigned(c):
        return Or(V == c, Y == c, Z == c)
    
    # Constraint 1: Exactly one of Kayne(1) or Novetzke(3) is assigned (XOR)
    s.add(Xor(assigned(1), assigned(3)))
    
    # Constraint 3: If Ong(4) assigned to Venezuela, Kayne(1) not assigned to Yemen
    s.add(Implies(V == 4, Y != 1))
    
    # Constraint 4: If Landon(2) assigned, it is to Zambia
    s.add(Implies(assigned(2), Z == 2))
    
    # Add the substitution constraint
    s.add(constraint_fn(assigned))
    
    # Enumerate
    solutions = []
    decision_vars = [V, Y, Z]
    
    while s.check() == sat:
        m = s.model()
        sol = tuple(m.eval(v).as_long() for v in decision_vars)
        solutions.append(sol)
        s.add(Or([v != m.eval(v) for v in decision_vars]))
    
    return set(solutions)

# Original constraint 2: If Jaramillo assigned, then Kayne assigned
def c2_original(assigned):
    return Implies(assigned(0), assigned(1))

# Answer options (substitutions for C2)
def opt_a(assigned):  # If Kayne assigned then Jaramillo assigned
    return Implies(assigned(1), assigned(0))

def opt_b(assigned):  # If Landon and Ong both assigned then Novetzke assigned
    return Implies(And(assigned(2), assigned(4)), assigned(3))

def opt_c(assigned):  # If Ong not assigned then Kayne assigned
    return Implies(Not(assigned(4)), assigned(1))

def opt_d(assigned):  # Jaramillo and Novetzke not both assigned
    return Not(And(assigned(0), assigned(3)))

def opt_e(assigned):  # Novetzke and Ong not both assigned
    return Not(And(assigned(3), assigned(4)))

# Enumerate solutions with original constraint 2
s_original = enumerate_solutions(c2_original)
print(f"Original (with C2): {len(s_original)} solutions")
for sol in sorted(s_original):
    print(f"  V={candidates[sol[0]]}, Y={candidates[sol[1]]}, Z={candidates[sol[2]]}")

print()

# Enumerate solutions for each answer option
options = {
    'A': opt_a,
    'B': opt_b,
    'C': opt_c,
    'D': opt_d,
    'E': opt_e,
}

matching = []
for letter, opt_fn in options.items():
    s_opt = enumerate_solutions(opt_fn)
    match = s_opt == s_original
    print(f"Option {letter}: {len(s_opt)} solutions, matches original: {match}")
    for sol in sorted(s_opt):
        print(f"  V={candidates[sol[0]]}, Y={candidates[sol[1]]}, Z={candidates[sol[2]]}")
    if match:
        matching.append(letter)
    print()

print(f"Matching options: {matching}")

if len(matching) == 1:
    print("STATUS: sat")
    print(f"answer:{matching[0]}")
elif len(matching) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {matching}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")