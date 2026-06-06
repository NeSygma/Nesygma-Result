from z3 import *

# Photographers
names = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']
# Bool variables for assignment to Silva (S) and Thorne (T)
S = {n: Bool(f'S_{n}') for n in names}
T = {n: Bool(f'T_{n}') for n in names}

solver = Solver()

# No photographer assigned to both ceremonies
for n in names:
    solver.add(Not(And(S[n], T[n])))

# At least two assigned to each ceremony
solver.add(Sum([If(S[n], 1, 0) for n in names]) >= 2)
solver.add(Sum([If(T[n], 1, 0) for n in names]) >= 2)

# Constraint 1: Frost and Heideck together at one ceremony (both assigned, same ceremony)
solver.add(Or(And(S['Frost'], S['Heideck']), And(T['Frost'], T['Heideck']))

# Constraint 2: If Lai and Mays both assigned, they must be to different ceremonies
both_assigned = And(Or(S['Lai'], T['Lai']), Or(S['Mays'], T['Mays']))
# Different ceremonies condition
different = Or(And(S['Lai'], T['Mays']), And(T['Lai'], S['Mays'])
solver.add(Implies(both_assigned, different))

# Constraint 3: If Gonzalez assigned to Silva, then Lai assigned to Thorne
solver.add(Implies(S['Gonzalez'], T['Lai']))

# Constraint 4: If Knutson not assigned to Thorne, then Heideck and Mays must be assigned to Thorne
solver.add(Implies(Not(T['Knutson']), And(T['Heideck'], T['Mays'])))

# Options for Thorne ceremony
options = {
    'A': ['Frost', 'Gonzalez', 'Heideck', 'Mays'],
    'B': ['Frost', 'Heideck', 'Knutson', 'Mays'],
    'C': ['Gonzalez', 'Knutson', 'Lai'],
    'D': ['Gonzalez', 'Knutson', 'Mays'],
    'E': ['Knutson', 'Mays']
}

found_options = []
for letter, th_set in [
        ("A", options['A']),
        ("B", options['B']),
        ("C", options['C']),
        ("D", options['D']),
        ("E", options['E'])
    ]:
    solver.push()
    # enforce exactly these photographers assigned to Thorne
    for n in names:
        if n in th_set:
            solver.add(T[n])
        else:
            solver.add(Not(T[n]))
    # Check if there exists a consistent Silva assignment
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine the impossible option (the one NOT in found_options)
all_letters = set(['A','B','C','D','E'])
impossible = list(all_letters - set(found_options))

if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
elif len(impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options {impossible}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible option found")