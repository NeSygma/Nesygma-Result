from z3 import *

# Define enumeration sort for compositions
Comp, comps = EnumSort('Comp', ['F','H','L','O','P','R','S','T'])
F, H, L, O, P, R, S, T = comps

# Position variables for each composition
pos_F = Int('pos_F')
pos_H = Int('pos_H')
pos_L = Int('pos_L')
pos_O = Int('pos_O')
pos_P = Int('pos_P')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_T = Int('pos_T')

solver = Solver()

# All positions between 1 and 8
solver.add(pos_F >= 1, pos_F <= 8)
solver.add(pos_H >= 1, pos_H <= 8)
solver.add(pos_L >= 1, pos_L <= 8)
solver.add(pos_O >= 1, pos_O <= 8)
solver.add(pos_P >= 1, pos_P <= 8)
solver.add(pos_R >= 1, pos_R <= 8)
solver.add(pos_S >= 1, pos_S <= 8)
solver.add(pos_T >= 1, pos_T <= 8)

# All distinct
solver.add(Distinct([pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]))

# Condition 1: T immediately before F or immediately after R
solver.add(Or(
    pos_T == pos_F - 1,
    pos_T == pos_R + 1
))

# Condition 2: At least two compositions between F and R
# Compute low and high
low_FR = If(pos_F < pos_R, pos_F, pos_R)
high_FR = If(pos_F < pos_R, pos_R, pos_F)
# Count compositions between low_FR and high_FR
count_FR = Sum([If(And(pos > low_FR, pos < high_FR), 1, 0) for pos in [pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]])
solver.add(count_FR >= 2)

# Condition 3: O is first or fifth
solver.add(Or(pos_O == 1, pos_O == 5))

# Condition 4: Eighth is L or H
solver.add(Or(pos_L == 8, pos_H == 8))

# Condition 5: P before S
solver.add(pos_P < pos_S)

# Condition 6: At least one composition between O and S
low_OS = If(pos_O < pos_S, pos_O, pos_S)
high_OS = If(pos_O < pos_S, pos_S, pos_O)
count_OS = Sum([If(And(pos > low_OS, pos < high_OS), 1, 0) for pos in [pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]])
solver.add(count_OS >= 1)

# Additional given: P third, S sixth
solver.add(pos_P == 3)
solver.add(pos_S == 6)

# Define comp_at_5: the composition at position 5
comp_at_5 = Const('comp_at_5', Comp)
# Ensure comp_at_5 equals the composition whose position is 5
solver.add(Or(
    And(pos_F == 5, comp_at_5 == F),
    And(pos_H == 5, comp_at_5 == H),
    And(pos_L == 5, comp_at_5 == L),
    And(pos_O == 5, comp_at_5 == O),
    And(pos_P == 5, comp_at_5 == P),
    And(pos_R == 5, comp_at_5 == R),
    And(pos_S == 5, comp_at_5 == S),
    And(pos_T == 5, comp_at_5 == T)
))

# Now test each option by checking if the negation is unsatisfiable
found_options = []

# Option A: F or H
opt_a_constr = Or(comp_at_5 == F, comp_at_5 == H)
solver.push()
solver.add(Not(opt_a_constr))
if solver.check() == unsat:
    found_options.append('A')
solver.pop()

# Option B: F or O
opt_b_constr = Or(comp_at_5 == F, comp_at_5 == O)
solver.push()
solver.add(Not(opt_b_constr))
if solver.check() == unsat:
    found_options.append('B')
solver.pop()

# Option C: F or T
opt_c_constr = Or(comp_at_5 == F, comp_at_5 == T)
solver.push()
solver.add(Not(opt_c_constr))
if solver.check() == unsat:
    found_options.append('C')
solver.pop()

# Option D: H or L
opt_d_constr = Or(comp_at_5 == H, comp_at_5 == L)
solver.push()
solver.add(Not(opt_d_constr))
if solver.check() == unsat:
    found_options.append('D')
solver.pop()

# Option E: O or R
opt_e_constr = Or(comp_at_5 == O, comp_at_5 == R)
solver.push()
solver.add(Not(opt_e_constr))
if solver.check() == unsat:
    found_options.append('E')
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")