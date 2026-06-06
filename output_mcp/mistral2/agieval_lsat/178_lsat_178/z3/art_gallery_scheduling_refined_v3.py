from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare days and shifts
Days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
Shifts = ["first", "second"]

# Declare students
Students = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]

# Create a 2D list of symbolic variables: student assigned to (day, shift)
# We use a dictionary of dictionaries for clarity
assignment = {s: {d: {sh: Bool(f"{s}_{d}_{sh}") for sh in Shifts} for d in Days} for s in Students}

# Global constraints
solver = Solver()

# 1. Each student works exactly two shifts
for s in Students:
    total_shifts = Sum([If(assignment[s][d][sh], 1, 0) for d in Days for sh in Shifts])
    solver.add(total_shifts == 2)

# 2. No student works both shifts of any day
for s in Students:
    for d in Days:
        solver.add(Not(And(assignment[s][d]["first"], assignment[s][d]["second"])))

# 3. On two consecutive days, Louise works the second shift
# Louise must work the second shift on exactly two days, and at least one pair of those days must be consecutive
louise_second_days = [
    If(assignment["Louise"][d]["second"], 1, 0) for d in Days
]
solver.add(Sum(louise_second_days) == 2)

# Ensure at least one pair of consecutive days where Louise works the second shift
consecutive_louise_second = [
    And(assignment["Louise"][Days[i]]["second"], assignment["Louise"][Days[i+1]]["second"]) for i in range(len(Days)-1)
]
solver.add(Or(consecutive_louise_second))

# 4. On two nonconsecutive days, Grecia works the first shift
# Grecia must work the first shift on exactly two days, and those days must be nonconsecutive
nonconsecutive_days = []
for i in range(len(Days)):
    for j in range(i+2, len(Days)):
        nonconsecutive_days.append(
            And(assignment["Grecia"][Days[i]]["first"], assignment["Grecia"][Days[j]]["first"])
        )
solver.add(Sum([If(assignment["Grecia"][d]["first"], 1, 0) for d in Days]) == 2)
solver.add(Or(nonconsecutive_days))

# 5. Katya works on Tuesday and Friday
# Katya must work at least one shift on Tuesday and at least one shift on Friday
solver.add(Or([assignment["Katya"]["Tuesday"][sh] for sh in Shifts]))
solver.add(Or([assignment["Katya"]["Friday"][sh] for sh in Shifts]))

# 6. Hakeem and Joe work on the same day as each other at least once
# There exists a day where both Hakeem and Joe work at least one shift
solver.add(Or([
    And(
        Or([assignment["Hakeem"][d][sh] for sh in Shifts]),
        Or([assignment["Joe"][d][sh] for sh in Shifts])
    ) for d in Days
]))

# 7. Grecia and Louise never work on the same day as each other
for d in Days:
    solver.add(Not(Or(
        And([assignment["Grecia"][d][sh] for sh in Shifts]),
        And([assignment["Louise"][d][sh] for sh in Shifts])
    )))

# 8. If there is at least one day on which Grecia and Joe both work at the gallery
# This is a conditional constraint for the question
solver.add(Or([
    And(
        Or([assignment["Grecia"][d][sh] for sh in Shifts]),
        Or([assignment["Joe"][d][sh] for sh in Shifts])
    ) for d in Days
]))

# Now, evaluate the multiple choice options one by one
found_options = []

# Option A: Grecia works the first shift on Tuesday
solver.push()
solver.add(assignment["Grecia"]["Tuesday"]["first"])
if solver.check() == sat:
    found_options.append("A")
    solver.pop()
else:
    solver.pop()

# Option B: Hakeem works the second shift on Monday
solver.push()
solver.add(assignment["Hakeem"]["Monday"]["second"])
if solver.check() == sat:
    found_options.append("B")
    solver.pop()
else:
    solver.pop()

# Option C: Hakeem works the second shift on Wednesday
solver.push()
solver.add(assignment["Hakeem"]["Wednesday"]["second"])
if solver.check() == sat:
    found_options.append("C")
    solver.pop()
else:
    solver.pop()

# Option D: Joe works the first shift on Wednesday
solver.push()
solver.add(assignment["Joe"]["Wednesday"]["first"])
if solver.check() == sat:
    found_options.append("D")
    solver.pop()
else:
    solver.pop()

# Option E: Joe works the first shift on Thursday
solver.push()
solver.add(assignment["Joe"]["Thursday"]["first"])
if solver.check() == sat:
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