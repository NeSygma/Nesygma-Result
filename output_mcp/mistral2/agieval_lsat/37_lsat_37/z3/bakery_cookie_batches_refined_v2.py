from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Cookie types: 0=oatmeal, 1=peanut butter, 2=sugar

# Base constraints (independent of options)
solver = Solver()

# Days for each cookie type: 3 batches per type, all on distinct days
oatmeal_days = [Int(f'oatmeal_{i}') for i in range(3)]
peanut_butter_days = [Int(f'peanut_butter_{i}') for i in range(3)]
sugar_days = [Int(f'sugar_{i}') for i in range(3)]

# All days must be in [0, 4] (Monday to Friday)
for days in [oatmeal_days, peanut_butter_days, sugar_days]:
    for d in days:
        solver.add(d >= 0, d <= 4)

# All batches for a type must be on distinct days
def all_distinct(days):
    return And([days[i] != days[j] for i in range(len(days)) for j in range(i+1, len(days))])

solver.add(all_distinct(oatmeal_days))
solver.add(all_distinct(peanut_butter_days))
solver.add(all_distinct(sugar_days))

# At least one batch is made on Monday (day 0)
solver.add(Or([d == 0 for d in oatmeal_days] + [d == 0 for d in peanut_butter_days] + [d == 0 for d in sugar_days]))

# The second batch of oatmeal (index 1) is on the same day as the first batch of peanut butter (index 0)
solver.add(oatmeal_days[1] == peanut_butter_days[0])

# The second batch of sugar (index 1) is on Thursday (day 3)
solver.add(sugar_days[1] == 3)

# Now evaluate each option
found_options = []

# Option A
oatmeal_A = [0, 2, 3]  # Monday, Wednesday, Thursday
peanut_butter_A = [2, 3, 4]  # Wednesday, Thursday, Friday
sugar_A = [0, 3, 4]  # Monday, Thursday, Friday
solver.push()
solver.add([oatmeal_days[i] == oatmeal_A[i] for i in range(3)])
solver.add([peanut_butter_days[i] == peanut_butter_A[i] for i in range(3)])
solver.add([sugar_days[i] == sugar_A[i] for i in range(3)])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B
oatmeal_B = [0, 1, 3]  # Monday, Tuesday, Thursday
peanut_butter_B = [1, 2, 3]  # Tuesday, Wednesday, Thursday
sugar_B = [0, 3, 2]  # Monday, Thursday, Wednesday
solver.push()
solver.add([oatmeal_days[i] == oatmeal_B[i] for i in range(3)])
solver.add([peanut_butter_days[i] == peanut_butter_B[i] for i in range(3)])
solver.add([sugar_days[i] == sugar_B[i] for i in range(3)])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C
oatmeal_C = [1, 2, 3]  # Tuesday, Wednesday, Thursday
peanut_butter_C = [2, 3, 4]  # Wednesday, Thursday, Friday
sugar_C = [1, 3, 4]  # Tuesday, Thursday, Friday
solver.push()
solver.add([oatmeal_days[i] == oatmeal_C[i] for i in range(3)])
solver.add([peanut_butter_days[i] == peanut_butter_C[i] for i in range(3)])
solver.add([sugar_days[i] == sugar_C[i] for i in range(3)])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D
oatmeal_D = [0, 1, 3]  # Monday, Tuesday, Thursday
peanut_butter_D = [0, 2, 3]  # Monday, Wednesday, Thursday
sugar_D = [0, 3, 4]  # Monday, Thursday, Friday
solver.push()
solver.add([oatmeal_days[i] == oatmeal_D[i] for i in range(3)])
solver.add([peanut_butter_days[i] == peanut_butter_D[i] for i in range(3)])
solver.add([sugar_days[i] == sugar_D[i] for i in range(3)])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E
oatmeal_E = [0, 3, 4]  # Monday, Thursday, Friday
peanut_butter_E = [1, 2, 3]  # Tuesday, Wednesday, Thursday
sugar_E = [0, 3, 4]  # Monday, Thursday, Friday
solver.push()
solver.add([oatmeal_days[i] == oatmeal_E[i] for i in range(3)])
solver.add([peanut_butter_days[i] == peanut_butter_E[i] for i in range(3)])
solver.add([sugar_days[i] == sugar_E[i] for i in range(3)])
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")