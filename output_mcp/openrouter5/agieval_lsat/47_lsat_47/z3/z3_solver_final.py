from z3 import *

# Students: Jiang, Kramer, Lopez, Megregian, O'Neill
# Plays: Sunset (S), Tamerlane (T), Undulation (U)
# Each student reviews one or more of exactly three plays.
# So each student reviews a non-empty subset of {S, T, U}.

students = ["Jiang", "Kramer", "Lopez", "Megregian", "ONeill"]
plays = ["Sunset", "Tamerlane", "Undulation"]

# Create Boolean variables: e.g., Jiang_Sunset, Jiang_Tamerlane, etc.
vars_dict = {}
for s in students:
    for p in plays:
        v = Bool(f"{s}_{p}")
        vars_dict[(s, p)] = v

solver = Solver()

# Each student reviews one or more plays (non-empty subset)
for s in students:
    solver.add(Or([vars_dict[(s, p)] for p in plays]))

# Condition 1: Kramer and Lopez each review fewer of the plays than Megregian.
def count_reviewed(student):
    return Sum([If(vars_dict[(student, p)], 1, 0) for p in plays])

solver.add(count_reviewed("Kramer") < count_reviewed("Megregian"))
solver.add(count_reviewed("Lopez") < count_reviewed("Megregian"))

# Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews.
for p in plays:
    solver.add(Implies(vars_dict[("Jiang", p)], Not(vars_dict[("Lopez", p)])))
    solver.add(Implies(vars_dict[("Jiang", p)], Not(vars_dict[("Megregian", p)])))

# Condition 3: Kramer and O'Neill both review Tamerlane.
solver.add(vars_dict[("Kramer", "Tamerlane")])
solver.add(vars_dict[("ONeill", "Tamerlane")])

# Condition 4: Exactly two of the students review exactly the same play or plays as each other.
student_list = students
pair_same = {}
for i in range(len(student_list)):
    for j in range(i+1, len(student_list)):
        s1 = student_list[i]
        s2 = student_list[j]
        same = Bool(f"same_{s1}_{s2}")
        solver.add(same == And([vars_dict[(s1, p)] == vars_dict[(s2, p)] for p in plays]))
        pair_same[(s1, s2)] = same

solver.add(Sum([If(pair_same[(s1, s2)], 1, 0) for s1, s2 in pair_same]) == 1)

# Additional condition from the question: Jiang does NOT review Tamerlane.
solver.add(Not(vars_dict[("Jiang", "Tamerlane")]))

# For "must be true", we check if the negation is possible.
# If Not(option) is unsat, then option must be true.
found_options = []
for letter, constr in [("A", vars_dict[("Jiang", "Sunset")]),
                        ("B", vars_dict[("Lopez", "Undulation")]),
                        ("C", vars_dict[("Megregian", "Sunset")]),
                        ("D", vars_dict[("Megregian", "Tamerlane")]),
                        ("E", vars_dict[("ONeill", "Undulation")])]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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