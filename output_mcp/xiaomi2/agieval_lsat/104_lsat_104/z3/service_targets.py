from z3 import *

solver = Solver()

# Variables: website (W) and voicemail (V) targets for each client
# Values: 1, 2, or 3 days
IW = Int('IW')  # Image website
IV = Int('IV')  # Image voicemail
SW = Int('SW')  # Solide website
SV = Int('SV')  # Solide voicemail
TW = Int('TW')  # Truvest website
TV = Int('TV')  # Truvest voicemail

all_vars = [IW, IV, SW, SV, TW, TV]

# Domain: each target is 1, 2, or 3
for v in all_vars:
    solver.add(And(v >= 1, v <= 3))

# Constraint 1: Website target <= voicemail target for each client
solver.add(IW <= IV)
solver.add(SW <= SV)
solver.add(TW <= TV)

# Constraint 2: Image's voicemail target is shorter than other clients' voicemail targets
solver.add(IV < SV)
solver.add(IV < TV)

# Constraint 3: Solide's website target is shorter than Truvest's website target
solver.add(SW < TW)

# Constraint 4 (question-specific): Truvest's website target is shorter than its voicemail target
solver.add(TW < TV)

# Now check each answer choice to see which MUST be true
# An option "must be true" if its negation is unsatisfiable (no model exists where it's false)

options = {
    "A": IV == 2,           # Image's voicemail target is 2 days
    "B": IW == 2,           # Image's website target is 2 days
    "C": IW == 1,           # Image's website target is 1 day
    "D": SW == 2,           # Solide's website target is 2 days
    "E": SW == 1,           # Solide's website target is 1 day
}

found_options = []
for letter, constr in options.items():
    # Check if the negation is unsatisfiable (i.e., the statement MUST be true)
    s = Solver()
    s.add(solver.assertions())
    s.add(Not(constr))
    if s.check() == unsat:
        # The negation is unsat, so the statement must be true
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")

# Also enumerate all valid configurations for verification
print("\n--- All valid configurations ---")
s2 = Solver()
s2.add(solver.assertions())
count = 0
while s2.check() == sat:
    m = s2.model()
    count += 1
    config = {str(v): m[v] for v in all_vars}
    print(f"Config {count}: {config}")
    s2.add(Or([v != m[v] for v in all_vars]))
print(f"Total configurations: {count}")