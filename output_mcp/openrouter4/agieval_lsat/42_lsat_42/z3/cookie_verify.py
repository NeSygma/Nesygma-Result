from z3 import *

# Let me also check: Could Option D be false? Let me print a model where D is false if one exists.
# Also let me double-check the chronological ordering constraint.

solver = Solver()

# Days: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4
# Kinds: Oatmeal=0, Peanut Butter=1, Sugar=2

batch = [[Int(f"b_{k}_{b}") for b in range(3)] for k in range(3)]

for k in range(3):
    for b in range(3):
        solver.add(batch[k][b] >= 0, batch[k][b] <= 4)

# No two batches of same kind on same day
for k in range(3):
    solver.add(Distinct(batch[k]))

# Chronological: 1st before 2nd before 3rd
for k in range(3):
    solver.add(batch[k][0] < batch[k][1])
    solver.add(batch[k][1] < batch[k][2])

# At least one batch on Monday
solver.add(Or([batch[k][b] == 0 for k in range(3) for b in range(3)]))

# Second oatmeal = first peanut butter
solver.add(batch[0][1] == batch[1][0])

# Second sugar on Thursday (day 3)
solver.add(batch[2][1] == 3)

# CONDITION: one kind's first = another kind's third
cond = Or([And(k1 != k2, batch[k1][0] == batch[k2][2]) for k1 in range(3) for k2 in range(3)])
solver.add(cond)

def count_day(day):
    return Sum([If(batch[k][b] == day, 1, 0) for k in range(3) for b in range(3)])

# Verify each option could-be-false scenario more carefully
# Option D false: exactly two batches on Tuesday is FALSE
# i.e., count_day(1) != 2
solver.push()
solver.add(count_day(1) != 2)
r = solver.check()
print(f"Option D could be false? {r}")
if r == sat:
    m = solver.model()
    kind_names = ["Oatmeal", "PeanutButter", "Sugar"]
    for k in range(3):
        for b in range(3):
            print(f"  {kind_names[k]} batch #{b+1} -> day {m[batch[k][b]]}")
    for d in range(5):
        cnt = sum(1 for k in range(3) for b in range(3) if m[batch[k][b]].as_long() == d)
        print(f"  Day {d}: {cnt} batches")
solver.pop()

# Option A false: some day has 0 batches
solver.push()
solver.add(Or([count_day(d) == 0 for d in range(5)]))
r = solver.check()
print(f"\nOption A could be false? {r}")
if r == sat:
    m = solver.model()
    kind_names = ["Oatmeal", "PeanutButter", "Sugar"]
    for k in range(3):
        for b in range(3):
            print(f"  {kind_names[k]} batch #{b+1} -> day {m[batch[k][b]]}")
    for d in range(5):
        cnt = sum(1 for k in range(3) for b in range(3) if m[batch[k][b]].as_long() == d)
        print(f"  Day {d}: {cnt} batches")
solver.pop()

# Option B false: less than 2 batches on Wednesday
solver.push()
solver.add(count_day(2) < 2)
r = solver.check()
print(f"\nOption B could be false? {r}")
if r == sat:
    m = solver.model()
    kind_names = ["Oatmeal", "PeanutButter", "Sugar"]
    for k in range(3):
        for b in range(3):
            print(f"  {kind_names[k]} batch #{b+1} -> day {m[batch[k][b]]}")
    for d in range(5):
        cnt = sum(1 for k in range(3) for b in range(3) if m[batch[k][b]].as_long() == d)
        print(f"  Day {d}: {cnt} batches")
solver.pop()

# Option C false: not exactly 1 batch on Monday
solver.push()
solver.add(count_day(0) != 1)
r = solver.check()
print(f"\nOption C could be false? {r}")
if r == sat:
    m = solver.model()
    kind_names = ["Oatmeal", "PeanutButter", "Sugar"]
    for k in range(3):
        for b in range(3):
            print(f"  {kind_names[k]} batch #{b+1} -> day {m[batch[k][b]]}")
    for d in range(5):
        cnt = sum(1 for k in range(3) for b in range(3) if m[batch[k][b]].as_long() == d)
        print(f"  Day {d}: {cnt} batches")
solver.pop()

# Option E false: not exactly 1 batch on Friday
solver.push()
solver.add(count_day(4) != 1)
r = solver.check()
print(f"\nOption E could be false? {r}")
if r == sat:
    m = solver.model()
    kind_names = ["Oatmeal", "PeanutButter", "Sugar"]
    for k in range(3):
        for b in range(3):
            print(f"  {kind_names[k]} batch #{b+1} -> day {m[batch[k][b]]}")
    for d in range(5):
        cnt = sum(1 for k in range(3) for b in range(3) if m[batch[k][b]].as_long() == d)
        print(f"  Day {d}: {cnt} batches")
solver.pop()