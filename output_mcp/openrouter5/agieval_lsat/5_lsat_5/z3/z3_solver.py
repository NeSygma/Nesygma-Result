from z3 import *

# Eight students: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
# Map names to indices for easier reference
G, H, I, K, L, N, O, R = range(8)

# Days: Monday=0, Tuesday=1, Wednesday=2
# Times: morning=0, afternoon=1

# We need to assign each student to a (day, time) slot, but exactly 6 give reports.
# So we have 6 slots: (Mon morning, Mon afternoon, Tue morning, Tue afternoon, Wed morning, Wed afternoon)
# We'll use a variable for each slot indicating which student gives the report there.

# Slot variables: slot[day][time] = student index (0-7)
slot = [[Int(f"slot_{d}_{t}") for t in range(2)] for d in range(3)]

solver = Solver()

# Domain: each slot gets a student index 0..7
for d in range(3):
    for t in range(2):
        solver.add(slot[d][t] >= 0, slot[d][t] <= 7)

# Exactly 6 reports given, so exactly 2 students do NOT give a report.
# All slots must be distinct (each student gives at most one report)
all_slots = [slot[d][t] for d in range(3) for t in range(2)]
solver.add(Distinct(all_slots))

# Condition 1: Tuesday is the only day on which George can give a report.
# George can only be on Tuesday (day=1). He cannot be on Monday or Wednesday.
for d in [0, 2]:
    for t in range(2):
        solver.add(slot[d][t] != G)

# Condition 2: Neither Olivia nor Robert can give an afternoon report.
# So Olivia and Robert cannot be in any afternoon slot (t=1).
for d in range(3):
    solver.add(slot[d][1] != O)
    solver.add(slot[d][1] != R)

# Condition 3: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is given on Wednesday.
# Nina gives a report means Nina is in some slot.
# If Nina is on Monday (day 0), then on Tuesday (day 1) Helen AND Irving must give reports.
# If Nina is on Tuesday (day 1), then on Wednesday (day 2) Helen AND Irving must give reports.
# If Nina is on Wednesday (day 2), no constraint.

# We need to encode: For each day d where Nina could be, if Nina is on day d and d != 2,
# then on day d+1, both Helen and Irving must be present.

for d in range(2):  # Monday or Tuesday
    # If Nina is on day d (in either morning or afternoon slot)
    nina_on_day_d = Or([slot[d][t] == N for t in range(2)])
    # Then on day d+1, both Helen and Irving must give reports
    helen_on_next = Or([slot[d+1][t] == H for t in range(2)])
    irving_on_next = Or([slot[d+1][t] == I for t in range(2)])
    solver.add(Implies(nina_on_day_d, And(helen_on_next, irving_on_next)))

# Given condition: Kyle gives the afternoon report on Tuesday.
# Tuesday is day 1, afternoon is t=1.
solver.add(slot[1][1] == K)

# Given condition: Helen gives the afternoon report on Wednesday.
# Wednesday is day 2, afternoon is t=1.
solver.add(slot[2][1] == H)

# Now evaluate each option.
# Each option gives the morning reports on Monday, Tuesday, Wednesday respectively.
# Morning is t=0.

options = {
    "A": [I, L, N],  # Irving, Lenore, Nina
    "B": [L, G, I],  # Lenore, George, Irving
    "C": [N, I, L],  # Nina, Irving, Lenore
    "D": [R, G, I],  # Robert, George, Irving
    "E": [R, I, L]   # Robert, Irving, Lenore
}

found_options = []
for letter, morning_list in options.items():
    solver.push()
    # Add constraints for this option: morning slots
    solver.add(slot[0][0] == morning_list[0])  # Monday morning
    solver.add(slot[1][0] == morning_list[1])  # Tuesday morning
    solver.add(slot[2][0] == morning_list[2])  # Wednesday morning
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