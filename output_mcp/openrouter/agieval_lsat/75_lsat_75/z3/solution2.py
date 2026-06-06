from z3 import *

assistants = ['Julio','Kevin','Rebecca','Lan','Nessa','Olivia']
day = {a: Int(f'day_{a}') for a in assistants}
time = {a: Int(f'time_{a}') for a in assistants}

base_solver = Solver()
for a in assistants:
    base_solver.add(day[a] >= 0, day[a] <= 2)
    base_solver.add(time[a] >= 0, time[a] <= 1)
# distinct slots
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        a1 = assistants[i]
        a2 = assistants[j]
        base_solver.add(Or(day[a1] != day[a2], time[a1] != time[a2]))
# constraints
base_solver.add(day['Kevin'] == day['Rebecca'])
base_solver.add(day['Lan'] != day['Olivia'])
base_solver.add(time['Nessa'] == 1)
base_solver.add(day['Julio'] < day['Olivia'])
base_solver.add(day['Julio'] == 1, time['Julio'] == 1)  # Thursday afternoon (day 1)

# enumerate all models
possible = {a: set() for a in assistants}
while base_solver.check() == sat:
    m = base_solver.model()
    for a in assistants:
        possible[a].add((m[day[a]].as_long(), m[time[a]].as_long()))
    # block this model
    block = []
    for a in assistants:
        block.append(day[a] != m[day[a]])
        block.append(time[a] != m[time[a]])
    base_solver.add(Or(block))

unique_count = sum(1 for a in assistants if a!='Julio' and len(possible[a])==1)
# print for debugging
# print('unique_count', unique_count)
# print(possible)

# option constraints
opt_a = BoolVal(unique_count == 1)
opt_b = BoolVal(unique_count == 2)
opt_c = BoolVal(unique_count == 3)
opt_d = BoolVal(unique_count == 4)
opt_e = BoolVal(unique_count == 5)

opt_solver = Solver()
found_options = []
for letter, constr in [("A",opt_a),("B",opt_b),("C",opt_c),("D",opt_d),("E",opt_e)]:
    opt_solver.push()
    opt_solver.add(constr)
    if opt_solver.check() == sat:
        found_options.append(letter)
    opt_solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")