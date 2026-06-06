from z3 import *

# Define photographers: 0=unassigned, 1=Silva, 2=Thorne
Frost = Int('Frost')
Gonzalez = Int('Gonzalez')
Heideck = Int('Heideck')
Knutson = Int('Knutson')
Lai = Int('Lai')
Mays = Int('Mays')
photographers = [Frost, Gonzalez, Heideck, Knutson, Lai, Mays]

domain = [Or(p == 0, p == 1, p == 2) for p in photographers]

# Base constraints (without C7)
base = [
    # At least 2 at Silva
    Sum([If(p == 1, 1, 0) for p in photographers]) >= 2,
    # At least 2 at Thorne
    Sum([If(p == 2, 1, 0) for p in photographers]) >= 2,
    # Frost and Heideck assigned together to same ceremony
    Frost == Heideck,
    Frost != 0,  # Both must be assigned
    # If Lai and Mays both assigned, different ceremonies
    Implies(And(Lai != 0, Mays != 0), Lai != Mays),
    # If Gonzalez at Silva, Lai at Thorne
    Implies(Gonzalez == 1, Lai == 2),
]

# Original constraint 7: If Knutson not at Thorne -> Heideck and Mays both at Thorne
C7 = Implies(Knutson != 2, And(Heideck == 2, Mays == 2))

# Verify base + C7 is satisfiable
s0 = Solver()
s0.add(domain + base + [C7])
res0 = s0.check()
print(f"base + C7 satisfiable: {res0}")
if res0 == sat:
    m = s0.model()
    print(f"  Example: Frost={m[Frost]}, Gonzalez={m[Gonzalez]}, Heideck={m[Heideck]}, "
          f"Knutson={m[Knutson]}, Lai={m[Lai]}, Mays={m[Mays]}")

# Answer choices
# (A) If Knutson at Silva -> Heideck and Mays cannot both be at Silva
opt_a = Implies(Knutson == 1, Not(And(Heideck == 1, Mays == 1)))

# (B) If Knutson at Silva -> Lai at Silva
opt_b = Implies(Knutson == 1, Lai == 1)

# (C) Unless Knutson at Thorne, both Frost and Mays at Thorne
# "Unless X, Y" = "If not X, then Y"
opt_c = Implies(Knutson != 2, And(Frost == 2, Mays == 2))

# (D) Unless Knutson at Thorne, Heideck cannot be at same ceremony as Lai
# Heideck != 0 always (constraint 4), so: Or(Heideck != Lai, Lai == 0)
opt_d = Implies(Knutson != 2, Or(Heideck != Lai, Lai == 0))

# (E) Unless Heideck or Mays at Thorne, Knutson at Thorne
# "Unless X, Y" = "If not X, then Y"
opt_e = Implies(And(Heideck != 2, Mays != 2), Knutson == 2)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, opt in options:
    # Direction 1: Does C7 imply opt? (Check: base + C7 + NOT(opt) satisfiable?)
    s1 = Solver()
    s1.add(domain + base + [C7, Not(opt)])
    res1 = s1.check()
    
    # Direction 2: Does opt imply C7? (Check: base + opt + NOT(C7) satisfiable?)
    s2 = Solver()
    s2.add(domain + base + [opt, Not(C7)])
    res2 = s2.check()
    
    if res1 == unsat and res2 == unsat:
        print(f"Option {letter}: EQUIVALENT to C7")
        found_options.append(letter)
    elif res1 == unsat and res2 == sat:
        print(f"Option {letter}: WEAKER (C7 implies {letter}, but not vice versa)")
        # Show counterexample where opt holds but C7 doesn't
        m = s2.model()
        print(f"  Counterexample: Frost={m[Frost]}, Gonzalez={m[Gonzalez]}, Heideck={m[Heideck]}, "
              f"Knutson={m[Knutson]}, Lai={m[Lai]}, Mays={m[Mays]}")
    elif res1 == sat and res2 == unsat:
        print(f"Option {letter}: STRONGER ({letter} implies C7, but not vice versa)")
    else:
        print(f"Option {letter}: INCOMPARABLE")

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")