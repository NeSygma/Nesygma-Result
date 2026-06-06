from z3 import *

solver = Solver()

# Slots: 1 to 5
# Slot 1: screen 1, 7pm
# Slot 2: screen 1, 9pm
# Slot 3: screen 2, 7pm
# Slot 4: screen 2, 9pm
# Slot 5: screen 3, 8pm

screen = [1, 1, 2, 2, 3]
time = [7, 9, 7, 9, 8]

h, m, r, s, w = Ints('h m r s w')
movies = [h, m, r, s, w]

for var in movies:
    solver.add(var >= 1, var <= 5)
solver.add(Distinct(movies))

# 1. Western before horror: time[w] < time[h]
solver.add(Or([And(w == i, h == j, time[i-1] < time[j-1]) for i in range(1,6) for j in range(1,6)]))

# 2. Sci-fi not on screen 3: screen[s] != 3
solver.add(Or([And(s == i, screen[i-1] != 3) for i in range(1,6)]))

# 3. Romance not on screen 2: screen[r] != 2
solver.add(Or([And(r == i, screen[i-1] != 2) for i in range(1,6)]))

# 4. Horror and mystery different screens: screen[h] != screen[m]
solver.add(Or([And(h == i, m == j, screen[i-1] != screen[j-1]) for i in range(1,6) for j in range(1,6)]))

# Condition: sci-fi and romance same screen: screen[s] == screen[r]
solver.add(Or([And(s == i, r == j, screen[i-1] == screen[j-1]) for i in range(1,6) for j in range(1,6)]))

# Now check each option: we need the one that MUST be true.
# Test option O: is (base + condition + NOT O) satisfiable?
# If unsat, then O must be true.

options = {
    "A": lambda: Or([And(w == i, time[i-1] == 7) for i in range(1,6)]),
    "B": lambda: Or([And(s == i, time[i-1] == 9) for i in range(1,6)]),
    "C": lambda: Or([And(m == i, time[i-1] == 8) for i in range(1,6)]),
    "D": lambda: Or([And(r == i, time[i-1] == 9) for i in range(1,6)]),
    "E": lambda: Or([And(h == i, time[i-1] == 8) for i in range(1,6)])
}

must_be_true = []
for letter, constr in options.items():
    solver.push()
    solver.add(Not(constr()))  # Can the option be false?
    if solver.check() == unsat:
        must_be_true.append(letter)
    solver.pop()

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")