from z3 import *

solver = Solver()

# Define student constants
george = IntVal(0)
helen = IntVal(1)
irving = IntVal(2)
kyle = IntVal(3)
lenore = IntVal(4)
nina = IntVal(5)
olivia = IntVal(6)
robert = IntVal(7)

# Slot variables
m0 = Int('m0')  # Mon morning
am0 = Int('a0')  # Mon afternoon (typo? should be a0)
m1 = Int('m1')  # Tue morning
am1 = Int('a1')  # Tue afternoon
m2 = Int('m2')  # Wed morning
am2 = Int('a2')  # Wed afternoon

# Base constraints
solver.add(Distinct([m0, am0, m1, am1, m2, am2]))
solver.add(m0 != george)
solver.add(am0 != george)
solver.add(m2 != george)
solver.add(am2 != george)
solver.add(am0 != olivia)
solver.add(am1 != olivia)
solver.add(am2 != olivia)
solver.add(am0 != robert)
solver.add(am1 != robert)
solver.add(am2 != robert)

# Conditional Nina rule
monday_nina = Or(m0 == nina, am0 == nina)
tuesday_consequent = And(
    Or(m1 == helen, m1 == irving),
    Or(am1 == helen, am1 == irving),
    Distinct(m1, am1),
    Or(And(m1 == helen, am1 == irving), And(m1 == irving, am1 == helen))
)
solver.add(Implies(monday_nina, tuesday_consequent))

tuesday_nina = Or(m1 == nina, am1 == nina)
wednesday_consequent = And(
    Or(m2 == helen, m2 == irving),
    Or(am2 == helen, am2 == irving),
    Distinct(m2, am2),
    Or(And(m2 == helen, am2 == irving), And(m2 == irving, am2 == helen))
)
solver.add(Implies(tuesday_nina, wednesday_consequent))

# Option constraints
opt_a_constr = [
    m0 == helen,
    am0 == robert,
    m1 == olivia,
    am1 == irving,
    m2 == lenore,
    am2 == kyle
]
opt_b_constr = [
    m0 == irving,
    am0 == olivia,
    m1 == helen,
    am1 == kyle,
    m2 == nina,
    am2 == lenore
]
opt_c_constr = [
    m0 == lenore,
    am0 == helen,
    m1 == george,
    am1 == kyle,
    m2 == robert,
    am2 == irving
]
opt_d_constr = [
    m0 == nina,
    am0 == helen,
    m1 == robert,
    am1 == irving,
    m2 == olivia,
    am2 == lenore
]
opt_e_constr = [
    m0 == olivia,
    am0 == nina,
    m1 == irving,
    am1 == helen,
    m2 == kyle,
    am2 == george
]

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    for c in constr:
        solver.add(c)
    result = solver.check()
    if result == sat:
        model = solver.model()
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