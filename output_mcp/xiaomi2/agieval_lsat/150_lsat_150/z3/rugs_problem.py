from z3 import *

# Colors: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
# Rug assignment: 0=not used, 1=rug1, 2=rug2, 3=rug3
colors = ['forest', 'olive', 'peach', 'turquoise', 'white', 'yellow']
N_COLORS = 6
N_RUGS = 3

# For each answer choice, we check if it's TRUE in ALL valid models.
# An answer "must be true" iff its NEGATION is unsatisfiable (no model violates it).

# We'll build the base constraints once, then for each option check if Not(option) is satisfiable.

def build_base(solver):
    # Assignment variables: color[i] in {0,1,2,3} where 0=not used, 1-3=rug
    assign = [Int(f'assign_{c}') for c in colors]
    
    for i in range(N_COLORS):
        solver.add(Or(assign[i] == 0, assign[i] == 1, assign[i] == 2, assign[i] == 3))
    
    # Exactly 5 colors used (assigned to rug 1-3), 1 not used
    solver.add(Sum([If(assign[i] != 0, 1, 0) for i in range(N_COLORS)]) == 5)
    
    # Rule 1: If white is used in a rug, that rug has exactly 3 colors
    # white_idx = 4
    for r in range(1, N_RUGS + 1):
        # If white is in rug r, then rug r has exactly 3 colors
        count_in_rug_r = Sum([If(assign[i] == r, 1, 0) for i in range(N_COLORS)])
        solver.add(Implies(assign[4] == r, count_in_rug_r == 3))
    
    # Rule 2: If olive is used in a rug, peach is also used in the same rug
    # olive_idx=1, peach_idx=2
    for r in range(1, N_RUGS + 1):
        solver.add(Implies(assign[1] == r, assign[2] == r))
    
    # Rule 3: Forest(0) and Turquoise(3) not in same rug
    for r in range(1, N_RUGS + 1):
        solver.add(Not(And(assign[0] == r, assign[3] == r)))
    
    # Rule 4: Peach(2) and Turquoise(3) not in same rug
    for r in range(1, N_RUGS + 1):
        solver.add(Not(And(assign[2] == r, assign[3] == r)))
    
    # Rule 5: Peach(2) and Yellow(5) not in same rug
    for r in range(1, N_RUGS + 1):
        solver.add(Not(And(assign[2] == r, assign[5] == r)))
    
    return assign

# For each option, check if its negation is satisfiable.
# If negation is UNSAT, the option MUST be true.
# If negation is SAT, the option can be false, so it doesn't MUST be true.

results = {}

# Option A: "No multicolored rugs in which forest is used"
# Forest is either not used, or in a solid rug (rug with exactly 1 color)
# Negation: Forest IS used in a multicolored rug (rug with 2+ colors)
def check_option_A():
    s = Solver()
    assign = build_base(s)
    # Negation: forest is used AND in a multicolored rug
    s.add(assign[0] != 0)  # forest is used
    # forest's rug has 2+ colors
    for r in range(1, N_RUGS + 1):
        count_r = Sum([If(assign[i] == r, 1, 0) for i in range(N_COLORS)])
        s.add(Implies(assign[0] == r, count_r >= 2))
    return s.check()

# Option B: "No multicolored rugs in which turquoise is used"
# Negation: turquoise IS used in a multicolored rug
def check_option_B():
    s = Solver()
    assign = build_base(s)
    s.add(assign[3] != 0)  # turquoise is used
    for r in range(1, N_RUGS + 1):
        count_r = Sum([If(assign[i] == r, 1, 0) for i in range(N_COLORS)])
        s.add(Implies(assign[3] == r, count_r >= 2))
    return s.check()

# Option C: "Peach is used in one of the rugs"
# Negation: Peach is NOT used
def check_option_C():
    s = Solver()
    assign = build_base(s)
    s.add(assign[2] == 0)  # peach not used
    return s.check()

# Option D: "Turquoise is used in one of the rugs"
# Negation: Turquoise is NOT used
def check_option_D():
    s = Solver()
    assign = build_base(s)
    s.add(assign[3] == 0)  # turquoise not used
    return s.check()

# Option E: "Yellow is used in one of the rugs"
# Negation: Yellow is NOT used
def check_option_E():
    s = Solver()
    assign = build_base(s)
    s.add(assign[5] == 0)  # yellow not used
    return s.check()

options = {
    'A': check_option_A,
    'B': check_option_B,
    'C': check_option_C,
    'D': check_option_D,
    'E': check_option_E,
}

must_be_true = []
for letter, check_fn in options.items():
    result = check_fn()
    if result == unsat:
        # Negation is unsatisfiable => option MUST be true
        must_be_true.append(letter)
        print(f"Option {letter}: MUST be true (negation is UNSAT)")
    else:
        print(f"Option {letter}: NOT necessarily true (negation is SAT)")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true: {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No option must be true")