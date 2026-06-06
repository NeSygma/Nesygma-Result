from z3 import *

solver = Solver()

# Sessions: 0=WM, 1=WA, 2=TM, 3=TA, 4=FM, 5=FA
# Assistants: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
# Day: session // 2 => 0=Wed, 1=Thu, 2=Fri
# Afternoon: session % 2 == 1

sessions = [Int(f'session_{i}') for i in range(6)]
for s in sessions:
    solver.add(s >= 0, s <= 5)
solver.add(Distinct(sessions))

# Constraint 1: Kevin (1) and Rebecca (5) same day
solver.add(sessions[1] / 2 == sessions[5] / 2)

# Constraint 2: Lan (2) and Olivia (4) different day
solver.add(sessions[2] / 2 != sessions[4] / 2)

# Constraint 3: Nessa (3) must lead an afternoon session
solver.add(Or(sessions[3] == 1, sessions[3] == 3, sessions[3] == 5))

# Constraint 4: Julio (0) earlier day than Olivia (4)
solver.add(sessions[0] / 2 < sessions[4] / 2)

# Given: Julio leads Thursday afternoon (session 3)
solver.add(sessions[0] == 3)

# Enumerate ALL valid solutions
decision_vars = sessions[1:]  # Kevin, Lan, Nessa, Olivia, Rebecca
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = tuple(int(str(m.eval(v, model_completion=True))) for v in decision_vars)
    solutions.append(sol)
    # Block this solution
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

session_names = ['WM', 'WA', 'TM', 'TA', 'FM', 'FA']
names = ['Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']

print(f"Total valid solutions: {len(solutions)}")
for i, sol in enumerate(solutions):
    print(f"  Solution {i+1}: " + ", ".join(f"{names[j]}={session_names[sol[j]]}" for j in range(5)))

# For each assistant (other than Julio), check if session is uniquely determined
determined_count = 0
for idx in range(5):
    vals = sorted(set(sol[idx] for sol in solutions))
    is_det = len(vals) == 1
    if is_det:
        determined_count += 1
    print(f"  {names[idx]}: possible = {[session_names[v] for v in vals]}, determined = {is_det}")

print(f"\nNumber of uniquely determined assistants (excluding Julio): {determined_count}")

# Match to answer choice
answer_map = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}
if determined_count in answer_map:
    print("STATUS: sat")
    print(f"answer:{answer_map[determined_count]}")
else:
    print("STATUS: unsat")
    print(f"Refine: determined count = {determined_count} not in options")