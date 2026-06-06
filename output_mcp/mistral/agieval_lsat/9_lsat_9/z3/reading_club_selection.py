from z3 import *

solver = Solver()

# Declare selection variables for each work
# French novels (3 total)
sel_fn1, sel_fn2, sel_fn3 = Bools('sel_fn1 sel_fn2 sel_fn3')
# Russian novels (3 total)
sel_rn1, sel_rn2, sel_rn3 = Bools('sel_rn1 sel_rn2 sel_rn3')
# French plays (2 total)
sel_fp1, sel_fp2 = Bools('sel_fp1 sel_fp2')
# Russian play (1 total)
sel_rp = Bool('sel_rp')

# Base constraints

# 1. Exactly 3 French novels are selected (given condition)
solver.add(And(sel_fn1, sel_fn2, sel_fn3))

# 2. Total selected works: at least 5 and at most 6
# Count selected works
total_selected = Sum([
    If(sel_fn1, 1, 0), If(sel_fn2, 1, 0), If(sel_fn3, 1, 0),
    If(sel_rn1, 1, 0), If(sel_rn2, 1, 0), If(sel_rn3, 1, 0),
    If(sel_fp1, 1, 0), If(sel_fp2, 1, 0),
    If(sel_rp, 1, 0)
])
solver.add(total_selected >= 5, total_selected <= 6)

# 3. No more than 4 French works selected (French novels + French plays)
french_works_selected = Sum([
    If(sel_fn1, 1, 0), If(sel_fn2, 1, 0), If(sel_fn3, 1, 0),
    If(sel_fp1, 1, 0), If(sel_fp2, 1, 0)
])
solver.add(french_works_selected <= 4)

# 4. At least 3 but no more than 4 novels selected (French novels + Russian novels)
novels_selected = Sum([
    If(sel_fn1, 1, 0), If(sel_fn2, 1, 0), If(sel_fn3, 1, 0),
    If(sel_rn1, 1, 0), If(sel_rn2, 1, 0), If(sel_rn3, 1, 0)
])
solver.add(novels_selected >= 3, novels_selected <= 4)

# 5. At least as many French novels as Russian novels selected
# Count selected French novels and Russian novels
selected_french_novels = Sum([
    If(sel_fn1, 1, 0), If(sel_fn2, 1, 0), If(sel_fn3, 1, 0)
])
selected_russian_novels = Sum([
    If(sel_rn1, 1, 0), If(sel_rn2, 1, 0), If(sel_rn3, 1, 0)
])
solver.add(selected_french_novels >= selected_russian_novels)

# 6. If both French plays are selected, then the Russian play is not selected
solver.add(Implies(And(sel_fp1, sel_fp2), Not(sel_rp)))

# Evaluate each option
found_options = []

# Option A: one Russian novel
solver.push()
solver.add(And(
    # Exactly one Russian novel selected
    Sum([If(sel_rn1, 1, 0), If(sel_rn2, 1, 0), If(sel_rn3, 1, 0)]) == 1,
    # No French plays selected
    Not(sel_fp1), Not(sel_fp2),
    # No Russian play selected
    Not(sel_rp)
))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: two French plays
solver.push()
solver.add(And(
    # Exactly two French plays selected
    sel_fp1, sel_fp2,
    # No Russian play selected (due to constraint 6)
    Not(sel_rp),
    # Exactly zero Russian novels selected (since total novels must be 3 or 4, and we have 3 French novels already)
    Sum([If(sel_rn1, 1, 0), If(sel_rn2, 1, 0), If(sel_rn3, 1, 0)]) == 0
))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: one Russian novel, one Russian play
solver.push()
solver.add(And(
    # Exactly one Russian novel selected
    Sum([If(sel_rn1, 1, 0), If(sel_rn2, 1, 0), If(sel_rn3, 1, 0)]) == 1,
    # Russian play selected
    sel_rp,
    # No French plays selected
    Not(sel_fp1), Not(sel_fp2)
))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: one Russian novel, two French plays
solver.push()
solver.add(And(
    # Exactly one Russian novel selected
    Sum([If(sel_rn1, 1, 0), If(sel_rn2, 1, 0), If(sel_rn3, 1, 0)]) == 1,
    # Two French plays selected
    sel_fp1, sel_fp2,
    # No Russian play selected (due to constraint 6)
    Not(sel_rp)
))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: two Russian novels, one French play
solver.push()
solver.add(And(
    # Exactly two Russian novels selected
    Sum([If(sel_rn1, 1, 0), If(sel_rn2, 1, 0), If(sel_rn3, 1, 0)]) == 2,
    # Exactly one French play selected
    Or(And(sel_fp1, Not(sel_fp2)), And(Not(sel_fp1), sel_fp2)),
    # No Russian play selected (since we have 3 French novels and 2 Russian novels = 5 novels total, which is allowed)
    Not(sel_rp)
))
if solver.check() == sat:
    found_options.append("E")
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