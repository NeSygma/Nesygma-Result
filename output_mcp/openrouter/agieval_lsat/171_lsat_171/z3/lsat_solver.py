from z3 import *

solver = Solver()
# Variables for Gagnon and Hue counts per section
G_L = Int('G_L')
G_M = Int('G_M')
# G_S is forced to 0
H_L = Int('H_L')
H_M = Int('H_M')
H_S = Int('H_S')

# Add non-negativity
solver.add(G_L >= 0, G_M >= 0)
solver.add(H_L >= 0, H_M >= 0, H_S >= 0)

# Section totals: each section has 2 photos total
# We'll define Fuentes counts per option later via constraints
# For now, create placeholders for Fuentes counts as Ints (will be constrained later)
F_L = Int('F_L')
F_M = Int('F_M')
F_S = Int('F_S')
solver.add(F_L >= 0, F_M >= 0, F_S >= 0)

# Section sum constraints (to be added after Fuentes counts are set)
# We'll add them later inside each option block because they depend on Fuentes values.

# Photographer total constraints (1 to 3) for each photographer
# For Gagnon total (G_L + G_M + G_S) where G_S = 0
solver.add(G_L + G_M >= 1, G_L + G_M <= 3)
# For Hue total
solver.add(H_L + H_M + H_S >= 1, H_L + H_M + H_S <= 3)
# For Fuentes total
solver.add(F_L + F_M + F_S >= 1, F_L + F_M + F_S <= 3)

# Gagnon cannot be in Sports
# G_S = 0 already implicit (no variable)

# Hue_L = Fuentes_S
solver.add(H_L == F_S)

# Existence condition: there exists a photographer with at least one in L and at least one in M
exist_cond = Or(And(F_L >= 1, F_M >= 1), And(G_L >= 1, G_M >= 1), And(H_L >= 1, H_M >= 1))
solver.add(exist_cond)

# Define option constraints as functions returning list of constraints for each option

def option_constraints(FL, FM, FS):
    # set Fuentes counts
    cons = [F_L == FL, F_M == FM, F_S == FS]
    # Section totals: each section sum to 2
    cons.append(F_L + G_L + H_L == 2)  # Lifestyle
    cons.append(F_M + G_M + H_M == 2)  # Metro
    cons.append(F_S + 0 + H_S == 2)   # Sports (G_S = 0)
    return cons

# Build option constraints
opt_a_constr = And(*option_constraints(1,1,1))
opt_b_constr = And(*option_constraints(1,0,2))
opt_c_constr = And(*option_constraints(2,0,1))
opt_d_constr = And(*option_constraints(0,1,2))
opt_e_constr = And(*option_constraints(0,2,1))

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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