from z3 import *

# For "must be true" questions, we need to check if the negation of each option is UNSAT
# If Not(option) is UNSAT given the constraints, then the option MUST be true

def create_base_solver():
    solver = Solver()
    
    # Sections: Lifestyle(0), Metro(1), Sports(2)
    # Photographers: Fuentes(0), Gagnon(1), Hue(2)
    photos = [[Int(f"photo_{s}_{i}") for i in range(2)] for s in range(3)]
    
    # Each photo is by one of the three photographers
    for s in range(3):
        for i in range(2):
            solver.add(Or(photos[s][i] == 0, photos[s][i] == 1, photos[s][i] == 2))
    
    # For each photographer, at least 1 but no more than 3 photographs must appear
    for p in range(3):
        count = Sum([If(photos[s][i] == p, 1, 0) for s in range(3) for i in range(2)])
        solver.add(count >= 1)
        solver.add(count <= 3)
    
    # At least one photograph in Lifestyle must be by a photographer who has at least one in Metro
    solver.add(Or([
        And(
            Or(photos[0][0] == p, photos[0][1] == p),
            Or(photos[1][0] == p, photos[1][1] == p)
        )
        for p in range(3)
    ]))
    
    # Number of Hue's photos in Lifestyle == Number of Fuentes photos in Sports
    hue_lifestyle = Sum([If(photos[0][i] == 2, 1, 0) for i in range(2)])
    fuentes_sports = Sum([If(photos[2][i] == 0, 1, 0) for i in range(2)])
    solver.add(hue_lifestyle == fuentes_sports)
    
    # None of Gagnon's photographs can be in Sports
    for i in range(2):
        solver.add(photos[2][i] != 1)
    
    # Additional condition: one photo in Lifestyle is by Gagnon and one is by Hue
    gagnon_lifestyle = Sum([If(photos[0][i] == 1, 1, 0) for i in range(2)])
    hue_lifestyle_count = Sum([If(photos[0][i] == 2, 1, 0) for i in range(2)])
    solver.add(gagnon_lifestyle == 1)
    solver.add(hue_lifestyle_count == 1)
    
    return solver, photos

# Define options
def get_options(photos):
    return {
        "A": Sum([If(photos[1][i] == 0, 1, 0) for i in range(2)]) == 1,
        "B": Sum([If(photos[1][i] == 1, 1, 0) for i in range(2)]) == 1,
        "C": And(photos[1][0] == 1, photos[1][1] == 1),
        "D": Sum([If(photos[2][i] == 2, 1, 0) for i in range(2)]) == 1,
        "E": And(photos[2][0] == 2, photos[2][1] == 2),
    }

# Check each option: does it MUST be true?
# Option must be true if Not(option) is UNSAT given constraints
must_be_true = []

for letter in ["A", "B", "C", "D", "E"]:
    s, photos = create_base_solver()
    options = get_options(photos)
    
    # Try to find a model where the option is FALSE
    s.add(Not(options[letter]))
    result = s.check()
    
    if result == unsat:
        # Cannot make option false => option MUST be true
        must_be_true.append(letter)
        print(f"Option {letter}: MUST be true (negation is UNSAT)")
    elif result == sat:
        print(f"Option {letter}: NOT necessarily true (found counterexample)")
        m = s.model()
        for sec in range(3):
            vals = [m.evaluate(photos[sec][i]) for i in range(2)]
            print(f"  Section {sec}: {vals}")
    else:
        print(f"Option {letter}: UNKNOWN")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")