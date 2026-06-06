from z3 import *

solver = Solver()

# Boolean variables: does student X review play Y?
j_s, j_t, j_u = Bools('j_s j_t j_u')  # Jiang
k_s, k_t, k_u = Bools('k_s k_t k_u')  # Kramer
l_s, l_t, l_u = Bools('l_s l_t l_u')  # Lopez
m_s, m_t, m_u = Bools('m_s m_t m_u')  # Megregian
o_s, o_t, o_u = Bools('o_s o_t o_u')  # O'Neill

students = [
    ('J', (j_s, j_t, j_u)),
    ('K', (k_s, k_t, k_u)),
    ('L', (l_s, l_t, l_u)),
    ('M', (m_s, m_t, m_u)),
    ('O', (o_s, o_t, o_u)),
]

# Each student reviews at least one play
for name, (s, t, u) in students:
    solver.add(Or(s, t, u))

# Count helper
def play_count(s, t, u):
    return If(s, 1, 0) + If(t, 1, 0) + If(u, 1, 0)

count_j = play_count(j_s, j_t, j_u)
count_k = play_count(k_s, k_t, k_u)
count_l = play_count(l_s, l_t, l_u)
count_m = play_count(m_s, m_t, m_u)
count_o = play_count(o_s, o_t, o_u)

# Constraint 1: K and L each review fewer plays than M
solver.add(count_k < count_m)
solver.add(count_l < count_m)

# Constraint 2: Neither L nor M reviews any play J reviews (no overlap)
solver.add(Not(And(j_s, l_s)))
solver.add(Not(And(j_t, l_t)))
solver.add(Not(And(j_u, l_u)))
solver.add(Not(And(j_s, m_s)))
solver.add(Not(And(j_t, m_t)))
solver.add(Not(And(j_u, m_u)))

# Constraint 3: K and O both review Tamerlane
solver.add(k_t == True)
solver.add(o_t == True)

# Constraint 4: Exactly two students review exactly the same plays
# Define "same plays" for each pair of students
def same_plays(s1, s2):
    return And(s1[0] == s2[0], s1[1] == s2[1], s1[2] == s2[2])

pairs = []
n = len(students)
for i in range(n):
    for j in range(i+1, n):
        pairs.append(same_plays(students[i][1], students[j][1]))

# Exactly one pair has identical review sets
solver.add(Sum([If(p, 1, 0) for p in pairs]) == 1)

# Constraint 5: Exactly three students review Undulation
solver.add(Sum([If(v, 1, 0) for v in [j_u, k_u, l_u, m_u, o_u]]) == 3)

# Test each answer option
options = {
    "A": Not(m_u),    # Megregian does not review Undulation
    "B": Not(o_u),    # O'Neill does not review Undulation
    "C": j_u,         # Jiang reviews Undulation
    "D": l_t,         # Lopez reviews Tamerlane
    "E": o_s,         # O'Neill reviews Sunset
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for name, (s, t, u) in students:
            plays = []
            if is_true(m.evaluate(s)): plays.append("S")
            if is_true(m.evaluate(t)): plays.append("T")
            if is_true(m.evaluate(u)): plays.append("U")
            print(f"  {name}: {','.join(plays)}")
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")