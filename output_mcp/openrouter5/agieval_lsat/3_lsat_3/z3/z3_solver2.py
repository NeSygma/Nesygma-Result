from z3 import *

# Students: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
n = len(students)  # 8

# Days: Monday=0, Tuesday=1, Wednesday=2
# Times: morning=0, afternoon=1
# day=3 means "no report"

day = [Int(f"day_{s}") for s in students]
time = [Int(f"time_{s}") for s in students]

solver = Solver()

# Domain constraints
for i in range(n):
    solver.add(Or([day[i] == d for d in [0, 1, 2, 3]]))  # 3 = no report
    solver.add(Or([time[i] == t for t in [0, 1]]))

# Exactly six students give reports (day != 3)
solver.add(Sum([If(day[i] != 3, 1, 0) for i in range(n)]) == 6)

# Exactly two reports each day (Monday, Tuesday, Wednesday)
for d in range(3):
    solver.add(Sum([If(day[i] == d, 1, 0) for i in range(n)]) == 2)

# Exactly one morning and one afternoon each day
for d in range(3):
    solver.add(Sum([If(And(day[i] == d, time[i] == 0), 1, 0) for i in range(n)]) == 1)
    solver.add(Sum([If(And(day[i] == d, time[i] == 1), 1, 0) for i in range(n)]) == 1)

# Tuesday is the only day on which George can give a report.
# George = index 0
solver.add(Implies(day[0] != 3, day[0] == 1))
solver.add(day[0] != 0)
solver.add(day[0] != 2)

# Neither Olivia nor Robert can give an afternoon report.
# Olivia = index 6, Robert = index 7
solver.add(Implies(day[6] != 3, time[6] == 0))
solver.add(Implies(day[7] != 3, time[7] == 0))

# If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is given on Wednesday.
# Nina = index 5, Helen = index 1, Irving = index 2
solver.add(Implies(And(day[5] != 3, day[5] != 2),
                   And(day[1] == day[5] + 1, day[2] == day[5] + 1)))

# Now evaluate each option.
# The question: "Which one of the following is a pair of students who, if they give reports on the same day as each other, must give reports on Wednesday?"
# So for each option (pair), we need to check: if the pair gives reports on the same day, does that force them to be on Wednesday?
# We check this by: add constraint that they are on the same day, and see if that forces day=2 for both.

# Option A: George and Lenore
# Option B: Helen and Nina
# Option C: Irving and Robert
# Option D: Kyle and Nina
# Option E: Olivia and Kyle

# For each option, we need to check: if they are on the same day, is it NECESSARILY Wednesday?
# We can test this by: add constraint that they are on the same day, and check if there exists a model where that day is NOT Wednesday.
# If no such model exists (unsat), then they MUST be on Wednesday.

# Let's define indices
G, H, I, K, L, N, O, R = range(8)

options = [
    ("A", [G, L]),
    ("B", [H, N]),
    ("C", [I, R]),
    ("D", [K, N]),
    ("E", [O, K])
]

found_options = []

for letter, pair in options:
    s1, s2 = pair
    solver.push()
    # They give reports on the same day
    solver.add(day[s1] != 3)
    solver.add(day[s2] != 3)
    solver.add(day[s1] == day[s2])
    # Check if they could be on a day other than Wednesday
    solver.add(day[s1] != 2)  # not Wednesday
    result = solver.check()
    if result == unsat:
        # No model where they are on the same day but NOT Wednesday
        # So if they are on the same day, they MUST be on Wednesday
        found_options.append(letter)
    solver.pop()

print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")