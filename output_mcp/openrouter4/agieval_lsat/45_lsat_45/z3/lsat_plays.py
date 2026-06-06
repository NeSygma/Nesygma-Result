from z3 import *

solver = Solver()

# Students and plays
students = ['Jiang', 'Kramer', 'Lopez', 'Megregian', "O'Neill"]
plays = ['Sunset', 'Tamerlane', 'Undulation']

# Review variables: review[student][play]
review = {}
for s in students:
    review[s] = {}
    for p in plays:
        review[s][p] = Bool(f'review_{s}_{p}')

# Constraint 1: Kramer and Lopez each review fewer plays than Megregian
count_reviewed = {}
for s in students:
    count_reviewed[s] = Sum([If(review[s][p], 1, 0) for p in plays])

solver.add(count_reviewed['Kramer'] < count_reviewed['Megregian'])
solver.add(count_reviewed['Lopez'] < count_reviewed['Megregian'])

# Constraint 2: Neither Lopez nor Megregian reviews any play Jiang reviews
for p in plays:
    solver.add(Implies(review['Jiang'][p], Not(review['Lopez'][p])))
    solver.add(Implies(review['Jiang'][p], Not(review['Megregian'][p])))

# Constraint 3: Kramer and O'Neill both review Tamerlane
solver.add(review['Kramer']['Tamerlane'] == True)
solver.add(review["O'Neill"]['Tamerlane'] == True)

# Constraint 4: Exactly two students review exactly the same plays as each other
# i.e., exactly one pair of students have identical review sets
student_indices = list(range(len(students)))
pair_same = []
for i in range(len(students)):
    for j in range(i+1, len(students)):
        si = students[i]
        sj = students[j]
        same = And([review[si][p] == review[sj][p] for p in plays])
        pair_same.append(same)

# Exactly one pair has same reviews
solver.add(Sum([If(same, 1, 0) for same in pair_same]) == 1)

# Additional constraint: Exactly three students review Undulation
solver.add(Sum([If(review[s]['Undulation'], 1, 0) for s in students]) == 3)

# Now evaluate each option
options = {
    "A": Not(review['Megregian']['Undulation']),  # Megregian does not review Undulation
    "B": Not(review["O'Neill"]['Undulation']),     # O'Neill does not review Undulation
    "C": review['Jiang']['Undulation'],            # Jiang reviews Undulation
    "D": review['Lopez']['Tamerlane'],             # Lopez reviews Tamerlane
    "E": review["O'Neill"]['Sunset']               # O'Neill reviews Sunset
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
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