from z3 import *

solver = Solver()

# Define the six band members and their solo positions (1-6)
members = ['G', 'K', 'P', 'S', 'T', 'V']
# G = guitarist, K = keyboard, P = percussionist, S = saxophonist, T = trumpeter, V = violinist

pos = {m: Int(f'pos_{m}') for m in members}

# Each member performs exactly one solo, positions 1-6, all distinct
for m in members:
    solver.add(pos[m] >= 1, pos[m] <= 6)
solver.add(Distinct([pos[m] for m in members]))

# Given condition: violinist performs the fourth solo
solver.add(pos['V'] == 4)

# Constraint 1: The guitarist does not perform the fourth solo
solver.add(pos['G'] != 4)

# Constraint 2: The percussionist performs a solo at some time before the keyboard player does
solver.add(pos['P'] < pos['K'])

# Constraint 3: The keyboard player performs a solo at some time after the violinist does
#               and at some time before the guitarist does
solver.add(pos['K'] > pos['V'])  # K after V, so K > 4
solver.add(pos['K'] < pos['G'])  # K before G

# Constraint 4: The saxophonist performs a solo at some time after either the percussionist
#               does or the trumpeter does, but not both
# "after" means strictly later (higher position number)
# XOR: exactly one of (S > P) and (S > T) is true
solver.add(Xor(pos['S'] > pos['P'], pos['S'] > pos['T']))

# First, let's see what solutions exist
print("=== Checking base constraints satisfiability ===")
result = solver.check()
if result == sat:
    m = solver.model()
    print("Base constraints are SAT. Sample model:")
    for mem in members:
        print(f"  pos[{mem}] = {m[pos[mem]]}")
else:
    print(f"Base constraints result: {result}")

# Now evaluate each option: which MUST be true (entailed by constraints)?
# An option MUST be true if its negation is unsatisfiable given the constraints.
options = {
    "A": pos['P'] < pos['V'],   # percussionist before violinist
    "B": pos['T'] < pos['V'],   # trumpeter before violinist
    "C": pos['T'] < pos['G'],   # trumpeter before guitarist
    "D": pos['S'] < pos['V'],   # saxophonist before violinist
    "E": pos['T'] < pos['S'],   # trumpeter before saxophonist
}

print("\n=== Checking which options MUST be true (negation is UNSAT) ===")
must_be_true = []
for letter, opt_constr in options.items():
    s = Solver()
    # Add all base constraints
    for m in members:
        s.add(pos[m] >= 1, pos[m] <= 6)
    s.add(Distinct([pos[m] for m in members]))
    s.add(pos['V'] == 4)
    s.add(pos['G'] != 4)
    s.add(pos['P'] < pos['K'])
    s.add(pos['K'] > pos['V'])
    s.add(pos['K'] < pos['G'])
    s.add(Xor(pos['S'] > pos['P'], pos['S'] > pos['T']))
    
    # Try to find a model where the option is FALSE
    s.add(Not(opt_constr))
    res = s.check()
    if res == unsat:
        print(f"  Option {letter}: MUST be true (negation is UNSAT)")
        must_be_true.append(letter)
    else:
        print(f"  Option {letter}: NOT necessarily true (counterexample exists)")
        if res == sat:
            cm = s.model()
            for mem in members:
                print(f"    pos[{mem}] = {cm[pos[mem]]}")

print(f"\nOptions that MUST be true: {must_be_true}")
print(f"Options that do NOT necessarily be true: {[l for l in ['A','B','C','D','E'] if l not in must_be_true]}")

# The EXCEPT question: which does NOT must be true
not_must = [l for l in ['A','B','C','D','E'] if l not in must_be_true]
if len(not_must) == 1:
    print(f"\nSTATUS: sat")
    print(f"answer:{not_must[0]}")
else:
    print(f"\nSTATUS: unsat")
    print(f"Refine: Multiple exceptions found: {not_must}")