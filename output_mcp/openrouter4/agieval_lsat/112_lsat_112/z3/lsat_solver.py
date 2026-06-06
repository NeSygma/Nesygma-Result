from z3 import *

solver = Solver()

# Articles
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')
articles = [G, H, J, Q, R, S, Y]

# Domain: positions 1 through 7
for a in articles:
    solver.add(a >= 1, a <= 7)

# All distinct positions
solver.add(Distinct(articles))

# Topic groups
finance = [G, H, J]
nutrition = [Q, R, S]
wildlife = [Y]  # only one article, no consecutive issues

# Constraint 1: Consecutive articles cannot cover the same topic.
# For each pair of articles in the same topic group, they cannot be adjacent.
for group in [finance, nutrition]:
    for i in range(len(group)):
        for j in range(i+1, len(group)):
            a = group[i]
            b = group[j]
            # Not adjacent: pos difference != 1
            solver.add(Not(Or(a == b + 1, b == a + 1)))

# Constraint 2: S can be earlier than Q only if Q is third.
# If S < Q then Q == 3. Equivalently: Not(S < Q) OR Q == 3
solver.add(Or(S >= Q, Q == 3))

# Constraint 3: S must be earlier than Y.
solver.add(S < Y)

# Constraint 4: J < G < R
solver.add(J < G)
solver.add(G < R)

# Define options
opt_a_constr = (G == 2)  # G is second
opt_b_constr = (H == 2)  # H is second
opt_c_constr = (S == 2)  # S is second
opt_d_constr = (R == 3)  # R is third
opt_e_constr = (Y == 3)  # Y is third

options = [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
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