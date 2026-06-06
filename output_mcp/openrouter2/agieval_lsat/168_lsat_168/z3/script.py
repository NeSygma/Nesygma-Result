from z3 import *

# Declare variables for each photograph
L1, L2 = Int('L1'), Int('L2')   # Lifestyle
M1, M2 = Int('M1'), Int('M2')   # Metro
S1, S2 = Int('S1'), Int('S2')   # Sports

solver = Solver()

# Domain constraints: each photograph is taken by one of the three photographers
for v in [L1, L2, M1, M2, S1, S2]:
    solver.add(v >= 0, v <= 2)   # 0=Fuentes, 1=Gagnon, 2=Hue

# Count of photographs per photographer
count_F = Sum([If(v == 0, 1, 0) for v in [L1, L2, M1, M2, S1, S2]])
count_G = Sum([If(v == 1, 1, 0) for v in [L1, L2, M1, M2, S1, S2]])
count_H = Sum([If(v == 2, 1, 0) for v in [L1, L2, M1, M2, S1, S2]])

# Each photographer appears at least once and at most three times
solver.add(count_F >= 1, count_F <= 3)
solver.add(count_G >= 1, count_G <= 3)
solver.add(count_H >= 1, count_H <= 3)

# None of Gagnon's photographs can be in the Sports section
solver.add(Sum([If(S1 == 1, 1, 0), If(S2 == 1, 1, 0)]) == 0)

# Number of Hue's photographs in Lifestyle equals number of Fuentes photographs in Sports
count_L_H = Sum([If(L1 == 2, 1, 0), If(L2 == 2, 1, 0)])
count_S_F = Sum([If(S1 == 0, 1, 0), If(S2 == 0, 1, 0)])
solver.add(count_L_H == count_S_F)

# At least one photographer appears in both Lifestyle and Metro
count_L_F = Sum([If(L1 == 0, 1, 0), If(L2 == 0, 1, 0)])
count_L_G = Sum([If(L1 == 1, 1, 0), If(L2 == 1, 1, 0)])
count_L_H = Sum([If(L1 == 2, 1, 0), If(L2 == 2, 1, 0)])

count_M_F = Sum([If(M1 == 0, 1, 0), If(M2 == 0, 1, 0)])
count_M_G = Sum([If(M1 == 1, 1, 0), If(M2 == 1, 1, 0)])
count_M_H = Sum([If(M1 == 2, 1, 0), If(M2 == 2, 1, 0)])

solver.add(Or(
    And(count_L_F >= 1, count_M_F >= 1),
    And(count_L_G >= 1, count_M_G >= 1),
    And(count_L_H >= 1, count_M_H >= 1)
))

# Define constraints for each option
opt_a_constr = And(
    L1 == 0, L2 == 0,          # Lifestyle: both Fuentes
    M1 == 0, M2 == 2,          # Metro: Fuentes and Hue
    S1 == 1, S2 == 2           # Sports: Gagnon and Hue
)

opt_b_constr = And(
    L1 == 0, L2 == 1,          # Lifestyle: Fuentes and Gagnon
    M1 == 0, M2 == 1,          # Metro: Fuentes and Gagnon
    S1 == 2, S2 == 2           # Sports: both Hue
)

opt_c_constr = And(
    L1 == 0, L2 == 0,          # Lifestyle: both Fuentes
    M1 == 1, M2 == 1,          # Metro: both Gagnon
    S1 == 2, S2 == 2           # Sports: both Hue
)

opt_d_constr = And(
    L1 == 1, L2 == 1,          # Lifestyle: both Gagnon
    M1 == 0, M2 == 1,          # Metro: Fuentes and Gagnon
    S1 == 0, S2 == 2           # Sports: Fuentes and Hue
)

opt_e_constr = And(
    L1 == 1, L2 == 2,          # Lifestyle: Gagnon and Hue
    M1 == 2, M2 == 2,          # Metro: both Hue
    S1 == 0, S2 == 2           # Sports: Fuentes and Hue
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr),
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
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