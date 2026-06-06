from z3 import *

solver = Solver()

# Candidates: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
# Countries: 0=Venezuela, 1=Yemen, 2=Zambia

assign = [[Bool(f"assign_{c}_{r}") for r in range(3)] for c in range(5)]

# Each country gets exactly one ambassador
for r in range(3):
    solver.add(Sum([assign[c][r] for c in range(5)]) == 1)

# Each candidate assigned to at most one country
for c in range(5):
    solver.add(Sum([assign[c][r] for r in range(3)]) <= 1)

# Helper: is candidate c assigned anywhere?
def is_assigned(c):
    return Sum([assign[c][r] for r in range(3)]) == 1

# Constraint 1: Either Kayne or Novetzke, but not both, is assigned
solver.add(Or(And(is_assigned(1), Not(is_assigned(3))), And(Not(is_assigned(1)), is_assigned(3))))

# Constraint 2: If Jaramillo is assigned, then Kayne is assigned
solver.add(Implies(is_assigned(0), is_assigned(1)))

# Constraint 3: If Ong is assigned to Venezuela, Kayne is not assigned to Yemen
solver.add(Implies(assign[4][0], Not(assign[1][1])))

# Constraint 4: If Landon is assigned, it is to Zambia
solver.add(Implies(is_assigned(2), assign[2][2]))

# Test each option: which pair of candidates is NOT assigned
options = {
    "A": (0, 3),  # Jaramillo and Novetzke
    "B": (0, 4),  # Jaramillo and Ong
    "C": (1, 2),  # Kayne and Landon
    "D": (1, 3),  # Kayne and Novetzke
    "E": (2, 4),  # Landon and Ong
}

found_options = []
for letter, (c1, c2) in options.items():
    solver.push()
    solver.add(Not(is_assigned(c1)))
    solver.add(Not(is_assigned(c2)))
    if solver.check() == sat:
        found_options.append(letter)
        # Also print the model for the valid option
        if letter == "A":  # print first found for debugging
            m = solver.model()
            print(f"Model for option {letter}:")
            for c in range(5):
                for r in range(3):
                    if m.eval(assign[c][r]):
                        cand_names = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]
                        country_names = ["Venezuela", "Yemen", "Zambia"]
                        print(f"  {cand_names[c]} -> {country_names[r]}")
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")