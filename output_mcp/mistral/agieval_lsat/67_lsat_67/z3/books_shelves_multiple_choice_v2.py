from z3 import *

solver = Solver()

# Declare shelf assignments for each book
# 0: top, 1: middle, 2: bottom
book_to_shelf = {
    "F": Int("F"),
    "G": Int("G"),
    "H": Int("H"),
    "I": Int("I"),
    "K": Int("K"),
    "L": Int("L"),
    "M": Int("M"),
    "O": Int("O"),
}

# Helper: shelf assignment is 0 (top), 1 (middle), 2 (bottom)
for book in book_to_shelf:
    solver.add(book_to_shelf[book] >= 0, book_to_shelf[book] <= 2)

# Constraint 3: I is on the middle shelf
solver.add(book_to_shelf["I"] == 1)

# Constraint 4: K is on a higher shelf than F
solver.add(book_to_shelf["K"] > book_to_shelf["F"])

# Constraint 5: O is on a higher shelf than L
solver.add(book_to_shelf["O"] > book_to_shelf["L"])

# Constraint 6: F is on the same shelf as M
solver.add(book_to_shelf["F"] == book_to_shelf["M"])

# At least two books per shelf
solver.add(Sum([If(book_to_shelf[book] == 0, 1, 0) for book in book_to_shelf]) >= 2)
solver.add(Sum([If(book_to_shelf[book] == 1, 1, 0) for book in book_to_shelf]) >= 2)
solver.add(Sum([If(book_to_shelf[book] == 2, 1, 0) for book in book_to_shelf]) >= 2)

# More books on bottom than top
solver.add(Sum([If(book_to_shelf[book] == 2, 1, 0) for book in book_to_shelf]) >
            Sum([If(book_to_shelf[book] == 0, 1, 0) for book in book_to_shelf]))

# Now evaluate each option for uniqueness
found_options = []

# Option A: I and M are on the same shelf as each other.
# Since I is on middle (1), this means M is on middle (1)
opt_a_constr = (book_to_shelf["M"] == 1)
solver.push()
solver.add(opt_a_constr)
res_a = solver.check()
if res_a == sat:
    # Check if the solution is unique
    model_a = solver.model()
    # Block this model
    solver.add(Or([book_to_shelf[book] != model_a[book_to_shelf[book]] for book in book_to_shelf]))
    res_a_unique = solver.check()
    if res_a_unique == unsat:
        found_options.append("A")
    solver.pop()
else:
    solver.pop()

# Option B: K and G are on the same shelf as each other.
opt_b_constr = (book_to_shelf["K"] == book_to_shelf["G"])
solver.push()
solver.add(opt_b_constr)
res_b = solver.check()
if res_b == sat:
    model_b = solver.model()
    solver.add(Or([book_to_shelf[book] != model_b[book_to_shelf[book]] for book in book_to_shelf]))
    res_b_unique = solver.check()
    if res_b_unique == unsat:
        found_options.append("B")
    solver.pop()
else:
    solver.pop()

# Option C: L and F are on the same shelf as each other.
opt_c_constr = (book_to_shelf["L"] == book_to_shelf["F"])
solver.push()
solver.add(opt_c_constr)
res_c = solver.check()
if res_c == sat:
    model_c = solver.model()
    solver.add(Or([book_to_shelf[book] != model_c[book_to_shelf[book]] for book in book_to_shelf]))
    res_c_unique = solver.check()
    if res_c_unique == unsat:
        found_options.append("C")
    solver.pop()
else:
    solver.pop()

# Option D: M and H are on the same shelf as each other.
opt_d_constr = (book_to_shelf["M"] == book_to_shelf["H"])
solver.push()
solver.add(opt_d_constr)
res_d = solver.check()
if res_d == sat:
    model_d = solver.model()
    solver.add(Or([book_to_shelf[book] != model_d[book_to_shelf[book]] for book in book_to_shelf]))
    res_d_unique = solver.check()
    if res_d_unique == unsat:
        found_options.append("D")
    solver.pop()
else:
    solver.pop()

# Option E: H and O are on the same shelf as each other.
opt_e_constr = (book_to_shelf["H"] == book_to_shelf["O"])
solver.push()
solver.add(opt_e_constr)
res_e = solver.check()
if res_e == sat:
    model_e = solver.model()
    solver.add(Or([book_to_shelf[book] != model_e[book_to_shelf[book]] for book in book_to_shelf]))
    res_e_unique = solver.check()
    if res_e_unique == unsat:
        found_options.append("E")
    solver.pop()
else:
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