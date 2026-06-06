from z3 import *

photographers = ['F', 'G', 'H', 'K', 'L', 'M']

# Original constraint C4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it
def c4(vars):
    return Implies(Not(vars['K_T']), And(vars['H_T'], vars['M_T']))

# Option A: If Knutson is assigned to Silva, then Heideck and Mays cannot both be assigned to that ceremony
def opt_a(vars):
    return Implies(vars['K_S'], Not(And(vars['H_S'], vars['M_S'])))

# Option B: If Knutson is assigned to Silva, then Lai must also be assigned to that ceremony
def opt_b(vars):
    return Implies(vars['K_S'], vars['L_S'])

# Option C: Unless Knutson is assigned to Thorne, both Frost and Mays must be assigned to that ceremony
def opt_c(vars):
    return Implies(Not(vars['K_T']), And(vars['F_T'], vars['M_T']))

# Option D: Unless Knutson is assigned to Thorne, Heideck cannot be assigned to the same ceremony as Lai
def opt_d(vars):
    same_ceremony = Or(And(vars['H_S'], vars['L_S']), And(vars['H_T'], vars['L_T']))
    return Implies(Not(vars['K_T']), Not(same_ceremony))

# Option E: Unless either Heideck or Mays is assigned to Thorne, Knutson must be assigned to that ceremony
def opt_e(vars):
    return Implies(Not(Or(vars['H_T'], vars['M_T'])), vars['K_T'])

options = [('A', opt_a), ('B', opt_b), ('C', opt_c), ('D', opt_d), ('E', opt_e)]

def create_base_solver(vars):
    s = Solver()
    for p in photographers:
        s.add(Not(And(vars[f'{p}_S'], vars[f'{p}_T'])))
    s.add(Sum([If(vars[f'{p}_S'], 1, 0) for p in photographers]) >= 2)
    s.add(Sum([If(vars[f'{p}_T'], 1, 0) for p in photographers]) >= 2)
    # C1
    s.add(Or(And(vars['F_S'], vars['H_S']), And(vars['F_T'], vars['H_T'])))
    # C2
    both_assigned = And(Or(vars['L_S'], vars['L_T']), Or(vars['M_S'], vars['M_T']))
    different_ceremonies = Or(And(vars['L_S'], vars['M_T']), And(vars['L_T'], vars['M_S']))
    s.add(Implies(both_assigned, different_ceremonies))
    # C3
    s.add(Implies(vars['G_S'], vars['L_T']))
    return s

found_options = []

for letter, opt_func in options:
    # Test direction 1: Does C4 entail option? i.e., is (C1^C2^C3^C4^NOT(option)) UNSAT?
    vars1 = {f'{p}_{c}': Bool(f'{p}_{c}') for p in photographers for c in ['S', 'T']}
    s1 = create_base_solver(vars1)
    s1.add(c4(vars1))
    s1.add(Not(opt_func(vars1)))
    
    # Test direction 2: Does option entail C4? i.e., is (C1^C2^C3^option^NOT(C4)) UNSAT?
    vars2 = {f'{p}_{c}': Bool(f'{p}_{c}') for p in photographers for c in ['S', 'T']}
    s2 = create_base_solver(vars2)
    s2.add(opt_func(vars2))
    s2.add(Not(c4(vars2)))
    
    res1 = s1.check()
    res2 = s2.check()
    
    print(f"Option {letter}: C4->option={res1 == unsat}, option->C4={res2 == unsat}")
    
    if res1 == unsat and res2 == unsat:
        found_options.append(letter)
        print(f"  => EQUIVALENT!")
    else:
        if res1 == sat:
            m = s1.model()
            print(f"  Counterexample to C4->option: ", end="")
            for p in photographers:
                for c in ['S', 'T']:
                    if m.eval(vars1[f'{p}_{c}']):
                        print(f"{p}_{c} ", end="")
            print()
        if res2 == sat:
            m = s2.model()
            print(f"  Counterexample to option->C4: ", end="")
            for p in photographers:
                for c in ['S', 'T']:
                    if m.eval(vars2[f'{p}_{c}']):
                        print(f"{p}_{c} ", end="")
            print()

print(f"\n{'='*60}")
print(f"FINAL RESULT:")
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")