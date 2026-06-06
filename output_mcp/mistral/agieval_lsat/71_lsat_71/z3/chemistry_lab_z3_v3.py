from z3 import *

# Lab assistants: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca

# Base constraints:
# 1. Each assistant is assigned to exactly one session (Distinct)
# 2. Kevin (1) and Rebecca (5) must be on the same day
# 3. Lan (2) and Olivia (4) cannot be on the same day
# 4. Nessa (3) must be in an afternoon session
# 5. Julio (0) must be on an earlier day than Olivia (4)

found_options = []

# Option A: Wednesday: Rebecca, Kevin; Thursday: Julio, Lan; Friday: Nessa, Olivia
# Sessions: [5, 1, 0, 2, 3, 4]
solver_A = Solver()
s_A = [5, 1, 0, 2, 3, 4]
s_A_vars = [Int(f"s_A_{i}") for i in range(6)]
for i in range(6):
    solver_A.add(s_A_vars[i] == s_A[i])
solver_A.add(Distinct(s_A_vars))

# Kevin (1) and Rebecca (5) same day
solver_A.add(Or([
    And(s_A_vars[0] == 5, s_A_vars[1] == 1, 0 == 0),
    And(s_A_vars[0] == 1, s_A_vars[1] == 5, 0 == 0),
    And(s_A_vars[2] == 5, s_A_vars[3] == 1, 1 == 1),
    And(s_A_vars[2] == 1, s_A_vars[3] == 5, 1 == 1),
    And(s_A_vars[4] == 5, s_A_vars[5] == 1, 2 == 2),
    And(s_A_vars[4] == 1, s_A_vars[5] == 5, 2 == 2)
]))

# Lan (2) and Olivia (4) not same day
solver_A.add(Not(Or([
    And(s_A_vars[i] == 2, s_A_vars[j] == 4, i // 2 == j // 2)
    for i in range(6) for j in range(6) if i != j
])))

# Nessa (3) must be in an afternoon session
solver_A.add(Or([s_A_vars[i] == 3 and i % 2 == 1 for i in range(6)]))

# Julio (0) must be on an earlier day than Olivia (4)
solver_A.add(Or([
    And(s_A_vars[i] == 0, s_A_vars[j] == 4, i // 2 < j // 2)
    for i in range(6) for j in range(6) if i != j
]))

if solver_A.check() == sat:
    found_options.append("A")

# Option B: Wednesday: Olivia, Nessa; Thursday: Julio, Lan; Friday: Kevin, Rebecca
# Sessions: [4, 3, 0, 2, 1, 5]
solver_B = Solver()
s_B = [4, 3, 0, 2, 1, 5]
s_B_vars = [Int(f"s_B_{i}") for i in range(6)]
for i in range(6):
    solver_B.add(s_B_vars[i] == s_B[i])
solver_B.add(Distinct(s_B_vars))

# Kevin (1) and Rebecca (5) same day
solver_B.add(Or([
    And(s_B_vars[0] == 5, s_B_vars[1] == 1, 0 == 0),
    And(s_B_vars[0] == 1, s_B_vars[1] == 5, 0 == 0),
    And(s_B_vars[2] == 5, s_B_vars[3] == 1, 1 == 1),
    And(s_B_vars[2] == 1, s_B_vars[3] == 5, 1 == 1),
    And(s_B_vars[4] == 5, s_B_vars[5] == 1, 2 == 2),
    And(s_B_vars[4] == 1, s_B_vars[5] == 5, 2 == 2)
]))

# Lan (2) and Olivia (4) not same day
solver_B.add(Not(Or([
    And(s_B_vars[i] == 2, s_B_vars[j] == 4, i // 2 == j // 2)
    for i in range(6) for j in range(6) if i != j
])))

# Nessa (3) must be in an afternoon session
solver_B.add(Or([s_B_vars[i] == 3 and i % 2 == 1 for i in range(6)]))

# Julio (0) must be on an earlier day than Olivia (4)
solver_B.add(Or([
    And(s_B_vars[i] == 0, s_B_vars[j] == 4, i // 2 < j // 2)
    for i in range(6) for j in range(6) if i != j
]))

if solver_B.check() == sat:
    found_options.append("B")

# Option C: Wednesday: Lan, Kevin; Thursday: Rebecca, Julio; Friday: Olivia, Nessa
# Sessions: [2, 1, 5, 0, 4, 3]
solver_C = Solver()
s_C = [2, 1, 5, 0, 4, 3]
s_C_vars = [Int(f"s_C_{i}") for i in range(6)]
for i in range(6):
    solver_C.add(s_C_vars[i] == s_C[i])
solver_C.add(Distinct(s_C_vars))

# Kevin (1) and Rebecca (5) same day
solver_C.add(Or([
    And(s_C_vars[0] == 5, s_C_vars[1] == 1, 0 == 0),
    And(s_C_vars[0] == 1, s_C_vars[1] == 5, 0 == 0),
    And(s_C_vars[2] == 5, s_C_vars[3] == 1, 1 == 1),
    And(s_C_vars[2] == 1, s_C_vars[3] == 5, 1 == 1),
    And(s_C_vars[4] == 5, s_C_vars[5] == 1, 2 == 2),
    And(s_C_vars[4] == 1, s_C_vars[5] == 5, 2 == 2)
]))

# Lan (2) and Olivia (4) not same day
solver_C.add(Not(Or([
    And(s_C_vars[i] == 2, s_C_vars[j] == 4, i // 2 == j // 2)
    for i in range(6) for j in range(6) if i != j
])))

# Nessa (3) must be in an afternoon session
solver_C.add(Or([s_C_vars[i] == 3 and i % 2 == 1 for i in range(6)]))

# Julio (0) must be on an earlier day than Olivia (4)
solver_C.add(Or([
    And(s_C_vars[i] == 0, s_C_vars[j] == 4, i // 2 < j // 2)
    for i in range(6) for j in range(6) if i != j
]))

if solver_C.check() == sat:
    found_options.append("C")

# Option D: Wednesday: Kevin, Rebecca; Thursday: Julio, Nessa; Friday: Olivia, Lan
# Sessions: [1, 5, 0, 3, 4, 2]
solver_D = Solver()
s_D = [1, 5, 0, 3, 4, 2]
s_D_vars = [Int(f"s_D_{i}") for i in range(6)]
for i in range(6):
    solver_D.add(s_D_vars[i] == s_D[i])
solver_D.add(Distinct(s_D_vars))

# Kevin (1) and Rebecca (5) same day
solver_D.add(Or([
    And(s_D_vars[0] == 5, s_D_vars[1] == 1, 0 == 0),
    And(s_D_vars[0] == 1, s_D_vars[1] == 5, 0 == 0),
    And(s_D_vars[2] == 5, s_D_vars[3] == 1, 1 == 1),
    And(s_D_vars[2] == 1, s_D_vars[3] == 5, 1 == 1),
    And(s_D_vars[4] == 5, s_D_vars[5] == 1, 2 == 2),
    And(s_D_vars[4] == 1, s_D_vars[5] == 5, 2 == 2)
]))

# Lan (2) and Olivia (4) not same day
solver_D.add(Not(Or([
    And(s_D_vars[i] == 2, s_D_vars[j] == 4, i // 2 == j // 2)
    for i in range(6) for j in range(6) if i != j
])))

# Nessa (3) must be in an afternoon session
solver_D.add(Or([s_D_vars[i] == 3 and i % 2 == 1 for i in range(6)]))

# Julio (0) must be on an earlier day than Olivia (4)
solver_D.add(Or([
    And(s_D_vars[i] == 0, s_D_vars[j] == 4, i // 2 < j // 2)
    for i in range(6) for j in range(6) if i != j
]))

if solver_D.check() == sat:
    found_options.append("D")

# Option E: Wednesday: Julio, Lan; Thursday: Olivia, Nessa; Friday: Rebecca, Kevin
# Sessions: [0, 2, 4, 3, 5, 1]
solver_E = Solver()
s_E = [0, 2, 4, 3, 5, 1]
s_E_vars = [Int(f"s_E_{i}") for i in range(6)]
for i in range(6):
    solver_E.add(s_E_vars[i] == s_E[i])
solver_E.add(Distinct(s_E_vars))

# Kevin (1) and Rebecca (5) same day
solver_E.add(Or([
    And(s_E_vars[0] == 5, s_E_vars[1] == 1, 0 == 0),
    And(s_E_vars[0] == 1, s_E_vars[1] == 5, 0 == 0),
    And(s_E_vars[2] == 5, s_E_vars[3] == 1, 1 == 1),
    And(s_E_vars[2] == 1, s_E_vars[3] == 5, 1 == 1),
    And(s_E_vars[4] == 5, s_E_vars[5] == 1, 2 == 2),
    And(s_E_vars[4] == 1, s_E_vars[5] == 5, 2 == 2)
]))

# Lan (2) and Olivia (4) not same day
solver_E.add(Not(Or([
    And(s_E_vars[i] == 2, s_E_vars[j] == 4, i // 2 == j // 2)
    for i in range(6) for j in range(6) if i != j
])))

# Nessa (3) must be in an afternoon session
solver_E.add(Or([s_E_vars[i] == 3 and i % 2 == 1 for i in range(6)]))

# Julio (0) must be on an earlier day than Olivia (4)
solver_E.add(Or([
    And(s_E_vars[i] == 0, s_E_vars[j] == 4, i // 2 < j // 2)
    for i in range(6) for j in range(6) if i != j
]))

if solver_E.check() == sat:
    found_options.append("E")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")