from z3 import *

solver = Solver()

# Workers: 0=Quinn, 1=Ruiz, 2=Smith, 3=Taylor, 4=Verma, 5=Wells, 6=Xue
N = 7
m = [Bool(f'm_{i}') for i in range(N)]  # member
l = [Bool(f'l_{i}') for i in range(N)]  # leader

# Exactly 3 members
solver.add(Sum([If(m[i], 1, 0) for i in range(N)]) == 3)

# Exactly 1 leader
solver.add(Sum([If(l[i], 1, 0) for i in range(N)]) == 1)

# Leader implies member
for i in range(N):
    solver.add(Implies(l[i], m[i]))

# Constraint 1: Quinn or Ruiz can be a member only if leading
# If Quinn is a member, Quinn must be leader
solver.add(Implies(m[0], l[0]))
# If Ruiz is a member, Ruiz must be leader
solver.add(Implies(m[1], l[1]))

# Constraint 2: If Smith is a member, Taylor must also be
solver.add(Implies(m[2], m[3]))

# Constraint 3: If Wells is a member, neither Ruiz nor Verma can be
solver.add(Implies(m[5], And(Not(m[1]), Not(m[4]))))

# Given: Taylor is the project leader
solver.add(l[3] == True)

# Given: Wells is a project member
solver.add(m[5] == True)

# Let's enumerate all possible solutions to see who the third member can be
# The three members are Taylor (index 3), Wells (index 5), and one more person
# Let's find all solutions by blocking

solutions = []
all_vars = m  # We care about member assignments

while solver.check() == sat:
    model = solver.model()
    # Get the member assignment
    member_vals = [model.eval(m[i]) for i in range(N)]
    # Get the leader assignment
    leader_vals = [model.eval(l[i]) for i in range(N)]
    
    sol = {
        'members': tuple(member_vals),
        'leaders': tuple(leader_vals)
    }
    solutions.append(sol)
    
    # Block this exact member assignment
    solver.add(Or([m[i] != model.eval(m[i]) for i in range(N)]))

print(f"Number of solutions: {len(solutions)}")

# Extract the third member (the one who is a member besides Taylor and Wells)
worker_names = ['Quinn', 'Ruiz', 'Smith', 'Taylor', 'Verma', 'Wells', 'Xue']
for sol in solutions:
    members = []
    for i in range(N):
        if sol['members'][i]:
            members.append(worker_names[i])
    leaders = []
    for i in range(N):
        if sol['leaders'][i]:
            leaders.append(worker_names[i])
    third = [w for w in members if w not in ['Taylor', 'Wells']]
    print(f"Members: {members}, Leader: {leaders[0]}, Third: {third[0] if third else '???'}")