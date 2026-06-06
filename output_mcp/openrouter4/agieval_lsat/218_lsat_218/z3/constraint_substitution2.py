from z3 import *

clues = ['R', 'S', 'T', 'U', 'W', 'X', 'Z']

def get_all_solutions(replace_constraint1_with=None):
    """Get all solutions under the given constraints.
    If replace_constraint1_with is given, replace the 'T != 1' constraint with it."""
    solver = Solver()
    
    # Decision variables: chapter number for each clue
    chap = {c: Int(f'chap_{c}') for c in clues}
    
    # Domain: each chapter is 1-7
    for c in clues:
        solver.add(chap[c] >= 1, chap[c] <= 7)
    
    # All different: each clue in a different chapter
    solver.add(Distinct([chap[c] for c in clues]))
    
    # Original constraint 1: T cannot be in chapter 1
    if replace_constraint1_with is None:
        solver.add(chap['T'] != 1)
    else:
        solver.add(replace_constraint1_with)
    
    # Constraint 2: T before W, exactly 2 chapters separating them
    solver.add(chap['T'] < chap['W'])
    solver.add(chap['W'] - chap['T'] == 3)
    
    # Constraint 3: S and Z not adjacent
    solver.add(Abs(chap['S'] - chap['Z']) != 1)
    
    # Constraint 4: W and X not adjacent
    solver.add(Abs(chap['W'] - chap['X']) != 1)
    
    # Constraint 5: U and X adjacent
    solver.add(Abs(chap['U'] - chap['X']) == 1)
    
    # Enumerate all solutions
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = tuple(m.eval(chap[c], model_completion=True).as_long() for c in clues)
        solutions.append(sol)
        # Block this solution
        solver.add(Or([chap[c] != m.eval(chap[c], model_completion=True).as_long() for c in clues]))
    
    return set(solutions), chap

# Get baseline solutions (original constraints)
print("Computing baseline solutions with original constraint 'T != 1'...")
baseline, _ = get_all_solutions()
print(f"Number of baseline solutions: {len(baseline)}")

# Now test each option by replacing T != 1 with the option's constraint
options_exprs = {
    "A": lambda chap: chap['U'] != 2,  # U cannot be in chapter 2
    "B": lambda chap: chap['W'] != 4,  # W cannot be in chapter 4
    "C": lambda chap: chap['X'] != 6,  # X cannot be in chapter 6
    "D": lambda chap: chap['U'] < chap['T'],  # U before T
    "E": lambda chap: chap['X'] < chap['W'],  # X before W
}

for letter, constr_func in options_exprs.items():
    # Build the constraint expression properly
    # We need chap from inside the function
    def make_constr(l, func):
        sol_set, chap = get_all_solutions(replace_constraint1_with=func(chap_inner := chap))
        return sol_set, chap
    # Hmm, this is getting messy. Let me restructure.

print("\n" + "="*60 + "\n")

# Let me restructure more carefully
for letter in ["A", "B", "C", "D", "E"]:
    print(f"Testing Option {letter}...")
    
    def get_sols_for_option(opt_letter):
        _, chap = get_all_solutions()  # just to get chap
        if opt_letter == "A":
            constr = chap['U'] != 2
        elif opt_letter == "B":
            constr = chap['W'] != 4
        elif opt_letter == "C":
            constr = chap['X'] != 6
        elif opt_letter == "D":
            constr = chap['U'] < chap['T']
        elif opt_letter == "E":
            constr = chap['X'] < chap['W']
        else:
            return None
        sol_set, _ = get_all_solutions(replace_constraint1_with=constr)
        return sol_set
    
    # Actually the chap from different calls is the same structure but different objects
    # Let me just define the constraints directly without needing chap
    
    # Let me use a different approach - inline it
    pass

# Simpler approach: just build the constraint using Int variables
print("\n=== SIMPLER APPROACH ===\n")

def get_all_solutions_v2(extra_constr_fn=None):
    solver = Solver()
    chap = {c: Int(f'chap_{c}') for c in clues}
    
    for c in clues:
        solver.add(chap[c] >= 1, chap[c] <= 7)
    solver.add(Distinct([chap[c] for c in clues]))
    
    if extra_constr_fn is None:
        # Original constraint 1
        solver.add(chap['T'] != 1)
    else:
        solver.add(extra_constr_fn(chap))
    
    solver.add(chap['T'] < chap['W'])
    solver.add(chap['W'] - chap['T'] == 3)
    solver.add(Abs(chap['S'] - chap['Z']) != 1)
    solver.add(Abs(chap['W'] - chap['X']) != 1)
    solver.add(Abs(chap['U'] - chap['X']) == 1)
    
    solutions = set()
    while solver.check() == sat:
        m = solver.model()
        sol = tuple(m.eval(chap[c], model_completion=True).as_long() for c in clues)
        solutions.add(sol)
        solver.add(Or([chap[c] != m.eval(chap[c], model_completion=True).as_long() for c in clues]))
    
    return solutions

# Get baseline
baseline = get_all_solutions_v2()
print(f"Baseline solutions count: {len(baseline)}")

# Test each option
option_fns = {
    "A": lambda ch: ch['U'] != 2,
    "B": lambda ch: ch['W'] != 4,
    "C": lambda ch: ch['X'] != 6,
    "D": lambda ch: ch['U'] < ch['T'],
    "E": lambda ch: ch['X'] < ch['W'],
}

for letter, fn in option_fns.items():
    sols = get_all_solutions_v2(extra_constr_fn=fn)
    print(f"\nOption {letter}: {len(sols)} solutions")
    if sols == baseline:
        print(f"  ✅ MATCHES BASELINE!")
    else:
        only_base = baseline - sols
        only_opt = sols - baseline
        if only_base:
            print(f"  Missing from option: {len(only_base)} solutions")
        if only_opt:
            print(f"  Extra in option: {len(only_opt)} solutions")