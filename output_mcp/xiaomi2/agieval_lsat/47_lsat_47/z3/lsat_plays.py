from z3 import *

solver = Solver()

# Boolean variables: does student X review play Y?
j_s, j_t, j_u = Bools('j_s j_t j_u')  # Jiang
k_s, k_t, k_u = Bools('k_s k_t k_u')  # Kramer
l_s, l_t, l_u = Bools('l_s l_t l_u')  # Lopez
m_s, m_t, m_u = Bools('m_s m_t m_u')  # Megregian
o_s, o_t, o_u = Bools('o_s o_t o_u')  # O'Neill

# Each student reviews at least one play
solver.add(Or(j_s, j_t, j_u))
solver.add(Or(k_s, k_t, k_u))
solver.add(Or(l_s, l_t, l_u))
solver.add(Or(m_s, m_t, m_u))
solver.add(Or(o_s, o_t, o_u))

# Play counts per student
count_j = If(j_s, 1, 0) + If(j_t, 1, 0) + If(j_u, 1, 0)
count_k = If(k_s, 1, 0) + If(k_t, 1, 0) + If(k_u, 1, 0)
count_l = If(l_s, 1, 0) + If(l_t, 1, 0) + If(l_u, 1, 0)
count_m = If(m_s, 1, 0) + If(m_t, 1, 0) + If(m_u, 1, 0)
count_o = If(o_s, 1, 0) + If(o_t, 1, 0) + If(o_u, 1, 0)

# Condition 1: Kramer reviews fewer plays than Megregian
solver.add(count_k < count_m)

# Condition 2: Lopez reviews fewer plays than Megregian
solver.add(count_l < count_m)

# Condition 3: Neither Lopez nor Megregian reviews any play Jiang reviews
solver.add(Implies(j_s, And(Not(l_s), Not(m_s))))
solver.add(Implies(j_t, And(Not(l_t), Not(m_t))))
solver.add(Implies(j_u, And(Not(l_u), Not(m_u))))

# Condition 4: Kramer and O'Neill both review Tamerlane
solver.add(k_t)
solver.add(o_t)

# Condition 5: Exactly two students review exactly the same plays
# Define "same plays" for each of the 10 pairs
def same(a_s, a_t, a_u, b_s, b_t, b_u):
    return And(a_s == b_s, a_t == b_t, a_u == b_u)

pair_same = [
    same(j_s, j_t, j_u, k_s, k_t, k_u),  # JK
    same(j_s, j_t, j_u, l_s, l_t, l_u),  # JL
    same(j_s, j_t, j_u, m_s, m_t, m_u),  # JM
    same(j_s, j_t, j_u, o_s, o_t, o_u),  # JO
    same(k_s, k_t, k_u, l_s, l_t, l_u),  # KL
    same(k_s, k_t, k_u, m_s, m_t, m_u),  # KM
    same(k_s, k_t, k_u, o_s, o_t, o_u),  # KO
    same(l_s, l_t, l_u, m_s, m_t, m_u),  # LM
    same(l_s, l_t, l_u, o_s, o_t, o_u),  # LO
    same(m_s, m_t, m_u, o_s, o_t, o_u),  # MO
]
solver.add(Sum([If(p, 1, 0) for p in pair_same]) == 1)

# Additional condition: Jiang does not review Tamerlane
solver.add(Not(j_t))

# Answer choices (what "must be true")
options = [
    ("A", j_s),      # Jiang reviews Sunset
    ("B", l_u),      # Lopez reviews Undulation
    ("C", m_s),      # Megregian reviews Sunset
    ("D", m_t),      # Megregian reviews Tamerlane
    ("E", o_u),      # O'Neill reviews Undulation
]

# For "must be true": check if negation is unsatisfiable
found_options = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    result = solver.check()
    if result == unsat:
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

# Also enumerate all valid models for verification
print("\n--- All valid models ---")
all_vars = [j_s, j_t, j_u, k_s, k_t, k_u, l_s, l_t, l_u, m_s, m_t, m_u, o_s, o_t, o_u]
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {}
    for v in all_vars:
        sol[str(v)] = is_true(m.evaluate(v, model_completion=True))
    solutions.append(sol)
    solver.add(Or([v != m.evaluate(v, model_completion=True) for v in all_vars]))

print(f"Total solutions: {len(solutions)}")
for i, sol in enumerate(solutions):
    def get_plays(prefix):
        plays = []
        if sol[f'{prefix}_s']: plays.append('S')
        if sol[f'{prefix}_t']: plays.append('T')
        if sol[f'{prefix}_u']: plays.append('U')
        return plays
    print(f"  Sol {i+1}: J={get_plays('j')} K={get_plays('k')} L={get_plays('l')} M={get_plays('m')} O={get_plays('o')}")