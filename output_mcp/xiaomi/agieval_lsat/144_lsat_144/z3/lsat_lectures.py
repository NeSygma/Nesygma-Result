from z3 import *

solver = Solver()

# Four historians: Farley, Garcia, Holden, Jiang
# Four topics: lithographs, oil_paintings, sculptures, watercolors
# Each historian gives exactly one lecture, each topic used exactly once
# Position 1-4 (first to fourth)

Farley, Garcia, Holden, Jiang = Ints('Farley Garcia Holden Jiang')
lithographs, oil_paintings, sculptures, watercolors = Ints('lithographs oil_paintings sculptures watercolors')

historians = [Farley, Garcia, Holden, Jiang]
topics = [lithographs, oil_paintings, sculptures, watercolors]

# Each historian and topic is in position 1-4
for h in historians:
    solver.add(And(h >= 1, h <= 4))
for t in topics:
    solver.add(And(t >= 1, t <= 4))

# All historians in different positions
solver.add(Distinct(historians))
# All topics in different positions
solver.add(Distinct(topics))

# Each historian's position equals their topic's position
# (historian gives that topic at that time slot)

# Constraints:
# 1. Oil paintings and watercolors must both be earlier than lithographs
solver.add(oil_paintings < lithographs)
solver.add(watercolors < lithographs)

# 2. Farley's lecture must be earlier than the oil paintings lecture
solver.add(Farley < oil_paintings)

# 3. Holden's lecture must be earlier than both Garcia's and Jiang's
solver.add(Holden < Garcia)
solver.add(Holden < Jiang)

# Now test each option
# Option A: Farley: sculptures; Holden: lithographs; Garcia: oil paintings; Jiang: watercolors
# Position 1=Farley/sculptures, 2=Holden/lithographs, 3=Garcia/oil_paintings, 4=Jiang/watercolors
opt_a_constr = And(
    Farley == 1, sculptures == 1,
    Holden == 2, lithographs == 2,
    Garcia == 3, oil_paintings == 3,
    Jiang == 4, watercolors == 4
)

# Option B: Farley: watercolors; Jiang: oil paintings; Holden: sculptures; Garcia: lithographs
opt_b_constr = And(
    Farley == 1, watercolors == 1,
    Jiang == 2, oil_paintings == 2,
    Holden == 3, sculptures == 3,
    Garcia == 4, lithographs == 4
)

# Option C: Garcia: sculptures; Farley: watercolors; Holden: oil paintings; Jiang: lithographs
opt_c_constr = And(
    Garcia == 1, sculptures == 1,
    Farley == 2, watercolors == 2,
    Holden == 3, oil_paintings == 3,
    Jiang == 4, lithographs == 4
)

# Option D: Holden: oil paintings; Jiang: watercolors; Farley: lithographs; Garcia: sculptures
opt_d_constr = And(
    Holden == 1, oil_paintings == 1,
    Jiang == 2, watercolors == 2,
    Farley == 3, lithographs == 3,
    Garcia == 4, sculptures == 4
)

# Option E: Holden: sculptures; Farley: watercolors; Jiang: oil paintings; Garcia: lithographs
opt_e_constr = And(
    Holden == 1, sculptures == 1,
    Farley == 2, watercolors == 2,
    Jiang == 3, oil_paintings == 3,
    Garcia == 4, lithographs == 4
)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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