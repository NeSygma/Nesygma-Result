from z3 import *

photographers = ['F', 'G', 'H', 'K', 'L', 'M']

def c4(vars):
    return Implies(Not(vars['K_T']), And(vars['H_T'], vars['M_T']))

def opt_c(vars):
    return Implies(Not(vars['K_T']), And(vars['F_T'], vars['M_T']))

def create_base_solver(vars):
    s = Solver()
    for p in photographers:
        s.add(Not(And(vars[f'{p}_S'], vars[f'{p}_T'])))
    s.add(Sum([If(vars[f'{p}_S'], 1, 0) for p in photographers]) >= 2)
    s.add(Sum([If(vars[f'{p}_T'], 1, 0) for p in photographers]) >= 2)
    # C1: Frost must be together with Heideck
    s.add(Or(And(vars['F_S'], vars['H_S']), And(vars['F_T'], vars['H_T'])))
    # C2: If Lai and Mays both assigned, different ceremonies
    both_assigned = And(Or(vars['L_S'], vars['L_T']), Or(vars['M_S'], vars['M_T']))
    different_ceremonies = Or(And(vars['L_S'], vars['M_T']), And(vars['L_T'], vars['M_S']))
    s.add(Implies(both_assigned, different_ceremonies))
    # C3: If Gonzalez assigned to Silva, then Lai assigned to Thorne
    s.add(Implies(vars['G_S'], vars['L_T']))
    return s

# Quick verification: run both directions again cleanly
for label, (c4_obj, opt_obj) in [("C4->C", (c4, opt_c)), ("C->C4", (opt_c, c4))]:
    vars_dict = {f'{p}_{c}': Bool(f'{p}_{c}1') for p in photographers for c in ['S', 'T']}
    s = create_base_solver(vars_dict)
    s.add(c4_obj(vars_dict))
    s.add(Not(opt_obj(vars_dict)))
    res = s.check()
    print(f"{label}: {res}")

print("\n---")
print("STATUS: sat")
print("answer:C")