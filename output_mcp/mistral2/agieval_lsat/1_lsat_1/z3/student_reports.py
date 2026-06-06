from z3 import *

# Define students as integers for indexing
students = {
    "George": 0,
    "Helen": 1,
    "Irving": 2,
    "Kyle": 3,
    "Lenore": 4,
    "Nina": 5,
    "Olivia": 6,
    "Robert": 7
}

# Days and time slots
days = ["Monday", "Tuesday", "Wednesday"]
time_slots = ["morning", "afternoon"]

# Total slots: 3 days * 2 time slots = 6 slots
# We need to assign 6 reports to these slots, leaving 6 slots empty (since only 6 reports are given)

# Create a 2D list to represent the schedule: [day][time_slot] -> student or -1 (empty)
schedule = [[Int(f"{day}_{time_slot}") for time_slot in time_slots] for day in days]

# Helper: List of all schedule variables
all_slots = [slot for day in schedule for slot in day]

# Constraints
solver = Solver()

# 1. Each slot is either -1 (empty) or a valid student index
for day in schedule:
    for slot in day:
        solver.add(Or([slot == -1, And(slot >= 0, slot < 8)]))

# 2. Exactly 6 reports are given (exactly 6 slots are not -1)
num_reports = Sum([If(s == -1, 0, 1) for s in all_slots])
solver.add(num_reports == 6)

# 3. George can only report on Tuesday
solver.add(schedule[0][0] != students["George"])
solver.add(schedule[0][1] != students["George"])
solver.add(schedule[2][0] != students["George"])
solver.add(schedule[2][1] != students["George"])

# 4. Olivia and Robert can only report in the morning
for day_idx, day in enumerate(schedule):
    for slot_idx, slot in enumerate(day):
        if time_slots[slot_idx] == "afternoon":
            solver.add(slot != students["Olivia"])
            solver.add(slot != students["Robert"])

# 5. Nina's constraint:
# If Nina reports on Monday or Tuesday, then Helen and Irving must report the next day
# If Nina reports on Wednesday, no constraint
nina_monday_morning = schedule[0][0] == students["Nina"]
nina_monday_afternoon = schedule[0][1] == students["Nina"]
nina_tuesday_morning = schedule[1][0] == students["Nina"]
nina_tuesday_afternoon = schedule[1][1] == students["Nina"]

# If Nina is on Monday, then Helen and Irving must be on Tuesday
solver.add(Implies(Or(nina_monday_morning, nina_monday_afternoon), 
                   And(
                       Or([schedule[1][0] == students["Helen"], schedule[1][1] == students["Helen"]]),
                       Or([schedule[1][0] == students["Irving"], schedule[1][1] == students["Irving"]])
                   )))

# If Nina is on Tuesday, then Helen and Irving must be on Wednesday
solver.add(Implies(Or(nina_tuesday_morning, nina_tuesday_afternoon), 
                   And(
                       Or([schedule[2][0] == students["Helen"], schedule[2][1] == students["Helen"]]),
                       Or([schedule[2][0] == students["Irving"], schedule[2][1] == students["Irving"]])
                   )))

# Base constraints are now added. Now evaluate each option.

# Define the options as constraints on the schedule
# Option A:
# Mon. morning: Helen; Mon. afternoon: Robert
# Tues. morning: Olivia; Tues. afternoon: Irving
# Wed. morning: Lenore; Wed. afternoon: Kyle
opt_a_constr = And(
    schedule[0][0] == students["Helen"],
    schedule[0][1] == students["Robert"],
    schedule[1][0] == students["Olivia"],
    schedule[1][1] == students["Irving"],
    schedule[2][0] == students["Lenore"],
    schedule[2][1] == students["Kyle"]
)

# Option B:
# Mon. morning: Irving; Mon. afternoon: Olivia
# Tues. morning: Helen; Tues. afternoon: Kyle
# Wed. morning: Nina; Wed. afternoon: Lenore
opt_b_constr = And(
    schedule[0][0] == students["Irving"],
    schedule[0][1] == students["Olivia"],
    schedule[1][0] == students["Helen"],
    schedule[1][1] == students["Kyle"],
    schedule[2][0] == students["Nina"],
    schedule[2][1] == students["Lenore"]
)

# Option C:
# Mon. morning: Lenore; Mon. afternoon: Helen
# Tues. morning: George; Tues. afternoon: Kyle
# Wed. morning: Robert; Wed. afternoon: Irving
opt_c_constr = And(
    schedule[0][0] == students["Lenore"],
    schedule[0][1] == students["Helen"],
    schedule[1][0] == students["George"],
    schedule[1][1] == students["Kyle"],
    schedule[2][0] == students["Robert"],
    schedule[2][1] == students["Irving"]
)

# Option D:
# Mon. morning: Nina; Mon. afternoon: Helen
# Tues. morning: Robert; Tues. afternoon: Irving
# Wed. morning: Olivia; Wed. afternoon: Lenore
opt_d_constr = And(
    schedule[0][0] == students["Nina"],
    schedule[0][1] == students["Helen"],
    schedule[1][0] == students["Robert"],
    schedule[1][1] == students["Irving"],
    schedule[2][0] == students["Olivia"],
    schedule[2][1] == students["Lenore"]
)

# Option E:
# Mon. morning: Olivia; Mon. afternoon: Nina
# Tues. morning: Irving; Tues. afternoon: Helen
# Wed. morning: Kyle; Wed. afternoon: George
opt_e_constr = And(
    schedule[0][0] == students["Olivia"],
    schedule[0][1] == students["Nina"],
    schedule[1][0] == students["Irving"],
    schedule[1][1] == students["Helen"],
    schedule[2][0] == students["Kyle"],
    schedule[2][1] == students["George"]
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
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