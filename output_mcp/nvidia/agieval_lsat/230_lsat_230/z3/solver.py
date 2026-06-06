from z3 import *

# Define buildings and their classes
buildings = ["Garza", "Flores", "Yates", "Zimmer", "Lynch", "King", "Meyer", "Ortiz"]
class_of = {
    "Garza": 1,
    "Flores": 1,
    "Yates": 3,
    "Zimmer": 3,
    "Lynch": 2,
    "King": 2,
    "Meyer": 2,
    "Ortiz": 2
}

# Companies: RealProp=R, Southco=S, Trustcorp=T
companies = ["R", "S", "T"]

# Boolean variable: bool_vars[(building, company)] = True if company owns building
bool_vars = {}
for b in buildings:
    for c in companies:
        bool_vars[(b, c)] = Bool(f"{b}_{c}")

solver = Solver()

# Exactly one company owns each building
for b in buildings:
    # At least one owner
    solver.add(Or([bool_vars[(b, c)] for c in companies]))
    # At most one owner (pairwise exclusive)
    for i in range(len(companies)):
        for j in range(i+1, len(companies)):
            ci = companies[i]
            cj = companies[j]
            solver.add(Not(And(bool_vars[(b, ci)], bool_vars[(b, cj)])))

# Invariant: 4*c1 + 2*c2 + c3 == 6 for each company
for comp in companies:
    c1 = Sum([If(bool_vars[(b, comp)], 1, 0) for b in buildings if class_of[b] == 1])
    c2 = Sum([If(bool_vars[(b, comp)], 1, 0) for b in buildings if class_of[b] == 2])
    c3 = Sum([If(bool_vars[(b, comp)], 1, 0) for b in buildings if class_of[b] == 3])
    solver.add(4*c1 + 2*c2 + c3 == 6)

# Answer options mapping
answers = {
    "A": ("R", ["Lynch", "Meyer", "Ortiz"]),
    "B": ("S", ["Garza", "Meyer"]),
    "C": ("S", ["King", "Meyer", "Ortiz"]),
    "D": ("T", ["Flores", "Yates"]),
    "E": ("T", ["Garza", "Lynch"])
}

# Evaluate each answer for unsatisfiability (cannot be true)
unsat_options = []
for letter, (comp_owner, owned_buildings) in answers.items():
    solver.push()
    # The company owns exactly the listed buildings
    for b in owned_buildings:
        solver.add(bool_vars[(b, comp_owner)] == True)
    for b in buildings:
        if b not in owned_buildings:
            solver.add(bool_vars[(b, comp_owner)] == False)
    # Check satisfiability
    if solver.check() == unsat:
        unsat_options.append(letter)
    solver.pop()

# Determine the answer: exactly one option cannot be true
if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be true {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options cannot be true")