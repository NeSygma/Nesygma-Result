from z3 import *

# Define rider indices
R, S, T, Y = 0, 1, 2, 3
# Bicycle indices: F=0, G=1, H=2, J=3

# Variables for day 1 and day 2 assignments
assign1 = [Int(f'assign1_{i}') for i in range(4)]
assign2 = [Int(f'assign2_{i}') for i in range(4)]

solver = Solver()

# Domain constraints: each assignment is between 0 and 3
for i in range(4):
    solver.add(assign1[i] >= 0, assign1[i] <= 3)
    solver.add(assign2[i] >= 0, assign2[i] <= 3)

# All bicycles tested each day: all distinct
solver.add(Distinct(assign1))
solver.add(Distinct(assign2))

# Reynaldo cannot test F (0)
solver.add(assign1[R] != 0)
solver.add(assign2[R] != 0)

# Yuki cannot test J (3)
solver.add(assign1[Y] != 3)
solver.add(assign2[Y] != 3)

# Theresa must test H (2) at least once
solver.add(Or(assign1[T] == 2, assign2[T] == 2))

# Bicycle Yuki tests on day 1 must be tested by Seamus on day 2
solver.add(assign2[S] == assign1[Y])

# Each rider tests a different bicycle each day
for i in range(4):
    solver.add(assign1[i] != assign2[i])

# Define option constraints
def option_A():
    # Both Reynaldo and Seamus test J (3)
    return And(
        Or(assign1[R] == 3, assign2[R] == 3),
        Or(assign1[S] == 3, assign2[S] == 3)
    )

def option_B():
    # Both Reynaldo and Theresa test J (3)
    return And(
        Or(assign1[R] == 3, assign2[R] == 3),
        Or(assign1[T] == 3, assign2[T] == 3)
    )

def option_C():
    # Both Reynaldo and Yuki test G (1)
    return And(
        Or(assign1[R] == 1, assign2[R] == 1),
        Or(assign1[Y] == 1, assign2[Y] == 1)
    )

def option_D():
    # Both Seamus and Theresa test G (1)
    return And(
        Or(assign1[S] == 1, assign2[S] == 1),
        Or(assign1[T] == 1, assign2[T] == 1)
    )

def option_E():
    # Both Theresa and Yuki test F (0)
    return And(
        Or(assign1[T] == 0, assign2[T] == 0),
        Or(assign1[Y] == 0, assign2[Y] == 0)
    )

# Evaluate each option for unsat (cannot be true)
found_unsat = []
for letter, constr in [("A", option_A()), ("B", option_B()), ("C", option_C()), ("D", option_D()), ("E", option_E())]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        found_unsat.append(letter)
    solver.pop()

if len(found_unsat) == 1:
    print("STATUS: sat")
    print(f"answer:{found_unsat[0]}")
elif len(found_unsat) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found unsat {found_unsat}")
else:
    print("STATUS: unsat")
    print("Refine: No options found unsat")