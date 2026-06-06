from z3 import *

# Five students: Jiang, Kramer, Lopez, Megregian, O'Neill
# Three plays: Sunset (S), Tamerlane (T), Undulation (U)
# Each student reviews one or more of exactly these three plays.
# So each student reviews a non-empty subset of {S, T, U}.

# We'll model each student's reviews with 3 boolean variables per student.
students = ["Jiang", "Kramer", "Lopez", "Megregian", "ONeill"]
plays = ["Sunset", "Tamerlane", "Undulation"]

# Create boolean variables: review[student][play]
# We'll use a dictionary mapping student name to list of Bool variables
review = {}
for s in students:
    review[s] = [Bool(f"{s}_{p}") for p in plays]

solver = Solver()

# Each student reviews one or more plays (non-empty subset)
for s in students:
    solver.add(Or(review[s]))

# Condition 1: Kramer and Lopez each review fewer of the plays than Megregian.
# Count how many plays each reviews.
def count_reviews(student_vars):
    return Sum([If(v, 1, 0) for v in student_vars])

kramer_count = count_reviews(review["Kramer"])
lopez_count = count_reviews(review["Lopez"])
megregian_count = count_reviews(review["Megregian"])

solver.add(kramer_count < megregian_count)
solver.add(lopez_count < megregian_count)

# Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews.
# For each play, if Jiang reviews it, then Lopez does NOT review it and Megregian does NOT review it.
for i in range(3):
    solver.add(Implies(review["Jiang"][i], Not(review["Lopez"][i])))
    solver.add(Implies(review["Jiang"][i], Not(review["Megregian"][i])))

# Condition 3: Kramer and O'Neill both review Tamerlane.
# Tamerlane is index 1 (Sunset=0, Tamerlane=1, Undulation=2)
solver.add(review["Kramer"][1] == True)
solver.add(review["ONeill"][1] == True)

# Condition 4: Exactly two of the students review exactly the same play or plays as each other.
# This means there is exactly one pair of students who have identical review sets.
# Or more precisely: the multiset of review sets has exactly one pair of identical sets (and the other three are all distinct from each other and from that pair).

# Let's define a function that checks if two students have the same review set.
def same_review(s1, s2):
    return And([review[s1][i] == review[s2][i] for i in range(3)])

# We need exactly one pair of students who are identical, and no other identities.
# Let's enumerate all pairs (10 pairs for 5 students).
student_list = students
pair_indicators = []
pair_vars = []
pair_idx = 0
for i in range(5):
    for j in range(i+1, 5):
        p = Bool(f"pair_{i}_{j}")
        pair_vars.append(p)
        solver.add(p == same_review(student_list[i], student_list[j]))
        pair_indicators.append(p)

# Exactly one pair is identical
solver.add(Sum([If(p, 1, 0) for p in pair_vars]) == 1)

# Now evaluate each answer choice.
# We need to find which option MUST be true (i.e., holds in ALL valid models).
# Since we're looking for "must be true", we can check if the negation is unsatisfiable.
# But the skeleton uses the "check each option for sat" pattern.
# For "must be true", we need: option is true in ALL models.
# So we check: is there a model where option is FALSE? If unsat, then option must be true.
# But the skeleton checks if option is SAT (possible). For "must be true", we need the option to be true in all models.
# Let's use the skeleton approach but interpret correctly:
# For "must be true", we check if the option is possible (sat). If only one option is possible... 
# Actually, for "must be true", we need to check if the negation of the option is unsat.
# Let's use the standard approach: check each option's negation.

found_options = []

# Option A: Jiang reviews more of the plays than Lopez does.
jiang_count = count_reviews(review["Jiang"])
# A: jiang_count > lopez_count
opt_a = jiang_count > lopez_count

# Option B: Megregian reviews more of the plays than Jiang does.
opt_b = megregian_count > jiang_count

# Option C: Megregian reviews more of the plays than O'Neill does.
oneill_count = count_reviews(review["ONeill"])
opt_c = megregian_count > oneill_count

# Option D: O'Neill reviews more of the plays than Jiang does.
opt_d = oneill_count > jiang_count

# Option E: O'Neill reviews more of the plays than Kramer does.
opt_e = oneill_count > kramer_count

# For "must be true", we check if the negation is unsatisfiable.
# If Not(option) is unsat, then option must be true in all models.
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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