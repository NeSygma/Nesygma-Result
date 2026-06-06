from z3 import *

solver = Solver()

# Positions 1..8
pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T = Ints('pos_F pos_H pos_L pos_O pos_P pos_R pos_S pos_T')
all_pos = [pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]

# Domain: each position between 1 and 8
for p in all_pos:
    solver.add(p >= 1, p <= 8)

# All distinct
solver.add(Distinct(all_pos))

# 1. T is performed either immediately before F or immediately after R.
solver.add(Or(pos_T == pos_F - 1, pos_T == pos_R + 1))

# 2. At least two compositions are performed either after F and before R, or after R and before F.
# |pos_F - pos_R| >= 3
solver.add(Or(pos_F + 3 <= pos_R, pos_R + 3 <= pos_F))

# 3. O is performed either first or fifth.
solver.add(Or(pos_O == 1, pos_O == 5))

# 4. The eighth composition is either L or H.
solver.add(Or(pos_L == 8, pos_H == 8))

# 5. P is performed at some time before S.
solver.add(pos_P < pos_S)

# 6. At least one composition is performed either after O and before S, or after S and before O.
# |pos_O - pos_S| >= 2
solver.add(Or(pos_O + 2 <= pos_S, pos_S + 2 <= pos_O))

# Given: P is third, S is sixth
solver.add(pos_P == 3)
solver.add(pos_S == 6)

# Let's first find all possible values for position 5 by enumeration
# We'll use a helper: for each composition, check if it can be at position 5
possible_fifth = []
comp_names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
comp_vars = [pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]

for name, var in zip(comp_names, comp_vars):
    s = Solver()
    # Add all the same constraints
    for p in all_pos:
        s.add(p >= 1, p <= 8)
    s.add(Distinct(all_pos))
    s.add(Or(pos_T == pos_F - 1, pos_T == pos_R + 1))
    s.add(Or(pos_F + 3 <= pos_R, pos_R + 3 <= pos_F))
    s.add(Or(pos_O == 1, pos_O == 5))
    s.add(Or(pos_L == 8, pos_H == 8))
    s.add(pos_P < pos_S)
    s.add(Or(pos_O + 2 <= pos_S, pos_S + 2 <= pos_O))
    s.add(pos_P == 3)
    s.add(pos_S == 6)
    # Add constraint that this composition is at position 5
    s.add(var == 5)
    if s.check() == sat:
        possible_fifth.append(name)
        # Print a full model for reference
        m = s.model()
        print(f"Possible fifth: {name}")
        for n, v in zip(comp_names, [pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]):
            print(f"  {n} = {m[v]}")
        print()

print("All possible fifth compositions:", possible_fifth)

# Now evaluate each answer choice
# Option A: F or H
# Option B: F or O
# Option C: F or T
# Option D: H or L
# Option E: O or R

options = [
    ("A", [pos_F, pos_H]),
    ("B", [pos_F, pos_O]),
    ("C", [pos_F, pos_T]),
    ("D", [pos_H, pos_L]),
    ("E", [pos_O, pos_R])
]

found_options = []
for letter, var_list in options:
    solver.push()
    # Check if position 5 MUST be one of these: test if it's possible that position 5 is NOT any of these
    # If position 5 cannot be any other composition, then it must be one of these.
    # We test: is it possible that position 5 is NOT in this set?
    # i.e., position 5 is equal to some composition not in the set
    other_vars = [v for v in all_pos if v not in var_list]
    solver.add(And([v != 5 for v in other_vars]))  # none of the others are at position 5
    # Wait, actually we need to test: can position 5 be something other than the two?
    # Let's test: Is it possible that the fifth composition is not in {X, Y}?
    # We assert that all compositions NOT in the set are not at position 5, meaning position 5 IS one of the set.
    # If this leads to sat, it means position 5 can be one of the set. That's not what we want.
    # We want: does the constraint set force position 5 to be one of the set?
    # So test if it's possible that position 5 is NOT one of the set.
    s2 = Solver()
    for p in all_pos:
        s2.add(p >= 1, p <= 8)
    s2.add(Distinct(all_pos))
    s2.add(Or(pos_T == pos_F - 1, pos_T == pos_R + 1))
    s2.add(Or(pos_F + 3 <= pos_R, pos_R + 3 <= pos_F))
    s2.add(Or(pos_O == 1, pos_O == 5))
    s2.add(Or(pos_L == 8, pos_H == 8))
    s2.add(pos_P < pos_S)
    s2.add(Or(pos_O + 2 <= pos_S, pos_S + 2 <= pos_O))
    s2.add(pos_P == 3)
    s2.add(pos_S == 6)
    # Assert that position 5 is NOT in the set
    # position 5 is the composition at position 5, which is exactly one of the vars equal to 5
    # So we assert: for each var in var_list, var != 5 (i.e., position 5 is NOT F and NOT H for option A)
    for v in var_list:
        s2.add(v != 5)
    # Now check: if unsat, then position 5 must be one of var_list
    if s2.check() == unsat:
        found_options.append(letter)
    solver.pop()

print("Options that MUST contain the fifth composition:", found_options)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")