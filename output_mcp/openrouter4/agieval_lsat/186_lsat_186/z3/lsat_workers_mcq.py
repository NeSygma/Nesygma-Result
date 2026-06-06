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
solver.add(Implies(m[0], l[0]))
solver.add(Implies(m[1], l[1]))

# Constraint 2: If Smith is a member, Taylor must also be
solver.add(Implies(m[2], m[3]))

# Constraint 3: If Wells is a member, neither Ruiz nor Verma can be
solver.add(Implies(m[5], And(Not(m[1]), Not(m[4]))))

# Given: Taylor is the project leader
solver.add(l[3] == True)

# Given: Wells is a project member
solver.add(m[5] == True)

# The third member is whoever is a member besides Taylor (3) and Wells (5)
# We need to check each answer option
# The answer states "the third project member must be either X or Y"
# This means the set of possibilities for the third member is exactly {X, Y}
# Let's find all possible third members first by enumeration

# Check each option: does it represent that the third member can only be those two?
# We'll test if an option is correct by checking if, given the constraints,
# the third member being X or Y is always true (i.e., no solution violates it).
# More directly: check if any solution exists where the third member is NOT X and NOT Y.
# If no such solution, the option is correct.

# Actually, for the skeleton, let's test each pair by checking:
# Does there exist a solution where the third member is X? (should be sat)
# Does there exist a solution where the third member is Y? (should be sat)
# Does there exist a solution where the third member is neither X nor Y? (should be unsat)
# If all three hold, that pair is the answer.

# For simplicity, let me just enumerate and find possible third members first.
# Then match to answer choices.

found_options = []

# Option A: third member is Quinn or Smith
opt_a = Or(m[0], m[2])  # but we need "third member is Quinn or Smith" — meaning the third (non-Taylor, non-Wells) member is Quinn or Smith
# So: exactly three members: Taylor, Wells, and one of {Quinn, Smith}
# And (m[3] and m[5] are already true via given constraints)
# So opt_a means: m[0] or m[2] is the third member
# Actually, we need to also ensure the total is 3 members.
# Let's just use the constraint: the third member (person != Taylor and != Wells who is a member) is either Quinn or Smith.

# Define the third member condition more formally:
# The person who is a member, not Taylor, not Wells, is in {X, Y}

# Option A: third member in {Quinn(X=0), Smith(X=2)}
solver.push()
# Third member must be either Quinn or Smith
# But we also need to ensure we don't have more than 3 members.
# Since we already have constraints enforcing exactly 3 members, m[3]=True, m[5]=True,
# the third member is the only other True member.
# So "third member is Quinn or Smith" means: (m[0] or m[2]) AND NOT (any other besides 3,5,0,2 is a member)
# But the solver already has exactly 3 members and m[3]=m[5]=True, so automatically
# the third member is whoever else is True.
# So we add: (m[0] or m[2]) ... but we must ensure no OTHER person (besides 0 and 2) is the third member.
# Actually, "the third member must be either Quinn or Smith" means:
# If the third member is not Quinn and not Smith, it's impossible.
# So: Not(m[0]) and Not(m[2]) should be unsat.
# Let's test: is there a solution where the third member is NOT Quinn AND NOT Smith?
# Add constraint that third member is neither Quinn nor Smith.
# That means: all members except Taylor and Wells are neither Quinn nor Smith.
solver.push()
solver.add(Not(m[0]))  # Quinn is not a member
solver.add(Not(m[2]))  # Smith is not a member
if solver.check() == sat:
    # There IS a solution where the third member is neither Quinn nor Smith -> option A is wrong
    pass
solver.pop()
solver.pop()

# Let me just enumerate the possible third members systematically.

# Find all possible third members
possible_third = []
while solver.check() == sat:
    model = solver.model()
    third_candidates = []
    for i in range(N):
        if i != 3 and i != 5 and model.eval(m[i]):
            third_candidates.append(i)
    if len(third_candidates) == 1:
        possible_third.append(third_candidates[0])
    # Block this solution
    solver.add(Or([m[i] != model.eval(m[i]) for i in range(N)]))

# The solver is now exhausted; rebuild fresh for MCQ
from z3 import *

solver = Solver()

m = [Bool(f'm_{i}') for i in range(N)]
l = [Bool(f'l_{i}') for i in range(N)]

solver.add(Sum([If(m[i], 1, 0) for i in range(N)]) == 3)
solver.add(Sum([If(l[i], 1, 0) for i in range(N)]) == 1)
for i in range(N):
    solver.add(Implies(l[i], m[i]))
solver.add(Implies(m[0], l[0]))
solver.add(Implies(m[1], l[1]))
solver.add(Implies(m[2], m[3]))
solver.add(Implies(m[5], And(Not(m[1]), Not(m[4]))))
solver.add(l[3] == True)
solver.add(m[5] == True)

# Now find all solutions to determine the possible third members
possible_thirds = []
while solver.check() == sat:
    model = solver.model()
    for i in range(N):
        if i != 3 and i != 5 and model.eval(m[i]):
            possible_thirds.append(i)
    solver.add(Or([m[i] != model.eval(m[i]) for i in range(N)]))

print(f"Possible third members (indices): {possible_thirds}")
print(f"Possible third members (names): {[['Quinn','Ruiz','Smith','Taylor','Verma','Wells','Xue'][i] for i in possible_thirds]}")