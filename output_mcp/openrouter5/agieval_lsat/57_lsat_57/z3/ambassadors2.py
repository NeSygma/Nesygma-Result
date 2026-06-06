from z3 import *

solver = Solver()

# Candidates: Jaramillo=0, Kayne=1, Landon=2, Novetzke=3, Ong=4
# Countries: Venezuela=0, Yemen=1, Zambia=2

# We'll use assignment variables: for each candidate, which country they go to (or -1 for none)
# Or better: for each country, which candidate.

Venezuela, Yemen, Zambia = Ints('Venezuela Yemen Zambia')
countries = [Venezuela, Yemen, Zambia]

for c in countries:
    solver.add(c >= 0, c <= 4)

solver.add(Distinct(countries))

# Constraint 1: Either Kayne(1) or Novetzke(3), but not both, is assigned.
kayne_assigned = Or([Venezuela == 1, Yemen == 1, Zambia == 1])
novetzke_assigned = Or([Venezuela == 3, Yemen == 3, Zambia == 3])
solver.add(If(kayne_assigned, 1, 0) + If(novetzke_assigned, 1, 0) == 1)

# Constraint 2: If Jaramillo(0) is assigned, then Kayne(1) is assigned.
jaramillo_assigned = Or([Venezuela == 0, Yemen == 0, Zambia == 0])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Constraint 3: If Ong(4) is assigned to Venezuela, Kayne(1) is not assigned to Yemen.
solver.add(Implies(Venezuela == 4, Yemen != 1))

# Constraint 4: If Landon(2) is assigned, it is to Zambia.
landon_assigned = Or([Venezuela == 2, Yemen == 2, Zambia == 2])
solver.add(Implies(landon_assigned, Zambia == 2))

# Given: Kayne is assigned as ambassador to Yemen.
solver.add(Yemen == 1)

# Let's first see what models exist to understand the situation
print("Checking satisfiability with given condition...")
result = solver.check()
if result == sat:
    m = solver.model()
    print("Venezuela:", m[Venezuela])
    print("Yemen:", m[Yemen])
    print("Zambia:", m[Zambia])
    
    # Map numbers to names
    names = {0: "Jaramillo", 1: "Kayne", 2: "Landon", 3: "Novetzke", 4: "Ong"}
    for c_name, c_var in [("Venezuela", Venezuela), ("Yemen", Yemen), ("Zambia", Zambia)]:
        val = m[c_var].as_long()
        print(f"{c_name}: {names[val]}")
    
    # Now let's enumerate all solutions to see what MUST be true
    solver.push()
    solutions = []
    while solver.check() == sat:
        m2 = solver.model()
        sol = (m2[Venezuela].as_long(), m2[Yemen].as_long(), m2[Zambia].as_long())
        solutions.append(sol)
        solver.add(Or([Venezuela != m2[Venezuela], Yemen != m2[Yemen], Zambia != m2[Zambia]]))
    solver.pop()
    
    print(f"\nTotal solutions: {len(solutions)}")
    for s in solutions:
        print(f"  V={names[s[0]]}, Y={names[s[1]]}, Z={names[s[2]]}")
    
    # Now check each option across all solutions
    # Option A: Jaramillo is assigned as ambassador to Venezuela.
    opt_a_all = all(s[0] == 0 for s in solutions)
    # Option B: Landon is assigned as ambassador to Zambia.
    opt_b_all = all(s[2] == 2 for s in solutions)
    # Option C: Ong is assigned as ambassador to Zambia.
    opt_c_all = all(s[2] == 4 for s in solutions)
    # Option D: Jaramillo is not assigned to an ambassadorship.
    opt_d_all = all(s[0] != 0 and s[1] != 0 and s[2] != 0 for s in solutions)
    # Option E: Ong is not assigned to an ambassadorship.
    opt_e_all = all(s[0] != 4 and s[1] != 4 and s[2] != 4 for s in solutions)
    
    print(f"\nOption A (Jaramillo to Venezuela) holds in all solutions: {opt_a_all}")
    print(f"Option B (Landon to Zambia) holds in all solutions: {opt_b_all}")
    print(f"Option C (Ong to Zambia) holds in all solutions: {opt_c_all}")
    print(f"Option D (Jaramillo not assigned) holds in all solutions: {opt_d_all}")
    print(f"Option E (Ong not assigned) holds in all solutions: {opt_e_all}")
    
    # Now use the multiple choice skeleton properly
    # "Must be true" means the option holds in ALL solutions.
    # So we need to check if the option is forced (its negation is unsat).
    
    found_options = []
    for letter, constr in [("A", Venezuela == 0), ("B", Zambia == 2), ("C", Zambia == 4), 
                           ("D", And(Venezuela != 0, Yemen != 0, Zambia != 0)),
                           ("E", And(Venezuela != 4, Yemen != 4, Zambia != 4))]:
        solver.push()
        # Check if the negation of the option is unsat (meaning option must be true)
        solver.add(Not(constr))
        if solver.check() == unsat:
            found_options.append(letter)
        solver.pop()
    
    print(f"\nMust-be-true options: {found_options}")
    
    if len(found_options) == 1:
        print("STATUS: sat")
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")
else:
    print("STATUS: unsat")
    print("Refine: No solutions with given condition")