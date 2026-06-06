from z3 import *

# Photographers: Frost(F), Gonzalez(G), Heideck(H), Knutson(K), Lai(L), Mays(M)
# Ceremonies: Silva(S), Thorne(T)
# Variables: p_S = True means photographer p assigned to Silva
#            p_T = True means photographer p assigned to Thorne

photographers = ['F', 'G', 'H', 'K', 'L', 'M']

def make_solver_with_constraints(c1, c2, c3, extra_constr):
    """Build solver with constraints 1-3 and an extra constraint (either original C4 or an option)"""
    solver = Solver()
    
    # Create boolean variables
    vars = {}
    for p in photographers:
        vars[f'{p}_S'] = Bool(f'{p}_S')
        vars[f'{p}_T'] = Bool(f'{p}_T')
    
    # Each photographer at most one ceremony
    for p in photographers:
        solver.add(Not(And(vars[f'{p}_S'], vars[f'{p}_T'])))
    
    # At least 2 photographers at each ceremony
    solver.add(Sum([If(vars[f'{p}_S'], 1, 0) for p in photographers]) >= 2)
    solver.add(Sum([If(vars[f'{p}_T'], 1, 0) for p in photographers]) >= 2)
    
    # C1: Frost must be assigned together with Heideck to one of the ceremonies
    solver.add(Or(And(vars['F_S'], vars['H_S']), And(vars['F_T'], vars['H_T'])))
    
    # C2: If Lai and Mays are both assigned, they must be to different ceremonies
    # (L_S or L_T) and (M_S or M_T) -> (L_S and M_T) or (L_T and M_S)
    both_assigned = And(Or(vars['L_S'], vars['L_T']), Or(vars['M_S'], vars['M_T']))
    different_ceremonies = Or(And(vars['L_S'], vars['M_T']), And(vars['L_T'], vars['M_S']))
    solver.add(Implies(both_assigned, different_ceremonies))
    
    # C3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
    solver.add(Implies(vars['G_S'], vars['L_T']))
    
    # Add the extra constraint
    solver.add(extra_constr)
    
    return solver, vars

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
    # H and L at same ceremony: (H_S and L_S) or (H_T and L_T)
    same_ceremony = Or(And(vars['H_S'], vars['L_S']), And(vars['H_T'], vars['L_T']))
    return Implies(Not(vars['K_T']), Not(same_ceremony))

# Option E: Unless either Heideck or Mays is assigned to Thorne, Knutson must be assigned to that ceremony
def opt_e(vars):
    return Implies(Not(Or(vars['H_T'], vars['M_T'])), vars['K_T'])

options = [('A', opt_a), ('B', opt_b), ('C', opt_c), ('D', opt_d), ('E', opt_e)]

results = []
for letter, opt_func in options:
    print(f"\n=== Testing option {letter} ===")
    
    # Test 1: Is (C1 ∧ C2 ∧ C3 ∧ C4) → Option valid?
    # Check if there exists a model satisfying C1-C4 but NOT the option
    s1, vars1 = make_solver_with_constraints(True, True, True, c4(vars1))
    # Actually need to capture vars from the function - let me restructure
    pass

# Let me restructure more carefully
print("=" * 60)
print("Testing each option for equivalence to C4 under C1-C3")
print("=" * 60)

for letter, opt_func in options:
    print(f"\n--- Option {letter} ---")
    
    # Test direction 1: Does C4 entail the option? (C1 ^ C2 ^ C3 ^ C4 ^ NOT(option) should be UNSAT)
    s1 = Solver()
    vars1 = {}
    for p in photographers:
        vars1[f'{p}_S'] = Bool(f'{p}_S')
        vars1[f'{p}_T'] = Bool(f'{p}_T')
    
    for p in photographers:
        s1.add(Not(And(vars1[f'{p}_S'], vars1[f'{p}_T'])))
    
    s1.add(Sum([If(vars1[f'{p}_S'], 1, 0) for p in photographers]) >= 2)
    s1.add(Sum([If(vars1[f'{p}_T'], 1, 0) for p in photographers]) >= 2)
    
    s1.add(Or(And(vars1['F_S'], vars1['H_S']), And(vars1['F_T'], vars1['H_T'])))
    
    both_assigned = And(Or(vars1['L_S'], vars1['L_T']), Or(vars1['M_S'], vars1['M_T']))
    different_ceremonies = Or(And(vars1['L_S'], vars1['M_T']), And(vars1['L_T'], vars1['M_S']))
    s1.add(Implies(both_assigned, different_ceremonies))
    
    s1.add(Implies(vars1['G_S'], vars1['L_T']))
    
    # Add C4
    s1.add(Implies(Not(vars1['K_T']), And(vars1['H_T'], vars1['M_T'])))
    
    # Add NOT(option)
    s1.add(Not(opt_func(vars1)))
    
    res1 = s1.check()
    if res1 == unsat:
        dir1_holds = True
        print(f"  C4 entails option: YES (no counterexample found)")
    else:
        dir1_holds = False
        if res1 == sat:
            m = s1.model()
            print(f"  C4 entails option: NO")
            print(f"  Counterexample: ", end="")
            for p in photographers:
                for c in ['S', 'T']:
                    v = m.eval(vars1[f'{p}_{c}'])
                    if v:
                        print(f"{p}_{c} ", end="")
            print()
        else:
            print(f"  C4 entails option: UNKNOWN (result={res1})")
    
    # Test direction 2: Does the option entail C4? (C1 ^ C2 ^ C3 ^ option ^ NOT(C4) should be UNSAT)
    s2 = Solver()
    vars2 = {}
    for p in photographers:
        vars2[f'{p}_S'] = Bool(f'{p}_S')
        vars2[f'{p}_T'] = Bool(f'{p}_T')
    
    for p in photographers:
        s2.add(Not(And(vars2[f'{p}_S'], vars2[f'{p}_T'])))
    
    s2.add(Sum([If(vars2[f'{p}_S'], 1, 0) for p in photographers]) >= 2)
    s2.add(Sum([If(vars2[f'{p}_T'], 1, 0) for p in photographers]) >= 2)
    
    s2.add(Or(And(vars2['F_S'], vars2['H_S']), And(vars2['F_T'], vars2['H_T'])))
    
    both_assigned2 = And(Or(vars2['L_S'], vars2['L_T']), Or(vars2['M_S'], vars2['M_T']))
    different_ceremonies2 = Or(And(vars2['L_S'], vars2['M_T']), And(vars2['L_T'], vars2['M_S']))
    s2.add(Implies(both_assigned2, different_ceremonies2))
    
    s2.add(Implies(vars2['G_S'], vars2['L_T']))
    
    # Add option
    s2.add(opt_func(vars2))
    
    # Add NOT(C4)
    s2.add(Not(Implies(Not(vars2['K_T']), And(vars2['H_T'], vars2['M_T']))))
    
    res2 = s2.check()
    if res2 == unsat:
        dir2_holds = True
        print(f"  Option entails C4: YES (no counterexample found)")
    else:
        dir2_holds = False
        if res2 == sat:
            m = s2.model()
            print(f"  Option entails C4: NO")
            print(f"  Counterexample: ", end="")
            for p in photographers:
                for c in ['S', 'T']:
                    v = m.eval(vars2[f'{p}_{c}'])
                    if v:
                        print(f"{p}_{c} ", end="")
            print()
        else:
            print(f"  Option entails C4: UNKNOWN (result={res2})")
    
    if dir1_holds and dir2_holds:
        print(f"  => Option {letter} IS equivalent to C4 under C1-C3")
        results.append(letter)
    else:
        print(f"  => Option {letter} is NOT equivalent to C4 under C1-C3")

print(f"\n{'='*60}")
print(f"Results: Equivalent options found: {results}")
print(f"{'='*60}")

# Now for multiple choice - find which single option is equivalent
found_options = []
for letter, opt_func in options:
    # Check equivalence both ways
    s1 = Solver()
    vars1 = {}
    for p in photographers:
        vars1[f'{p}_S'] = Bool(f'{p}_S')
        vars1[f'{p}_T'] = Bool(f'{p}_T')
    
    for p in photographers:
        s1.add(Not(And(vars1[f'{p}_S'], vars1[f'{p}_T'])))
    s1.add(Sum([If(vars1[f'{p}_S'], 1, 0) for p in photographers]) >= 2)
    s1.add(Sum([If(vars1[f'{p}_T'], 1, 0) for p in photographers]) >= 2)
    s1.add(Or(And(vars1['F_S'], vars1['H_S']), And(vars1['F_T'], vars1['H_T'])))
    both_assigned = And(Or(vars1['L_S'], vars1['L_T']), Or(vars1['M_S'], vars1['M_T']))
    different_ceremonies = Or(And(vars1['L_S'], vars1['M_T']), And(vars1['L_T'], vars1['M_S']))
    s1.add(Implies(both_assigned, different_ceremonies))
    s1.add(Implies(vars1['G_S'], vars1['L_T']))
    s1.add(Implies(Not(vars1['K_T']), And(vars1['H_T'], vars1['M_T'])))  # C4
    s1.add(Not(opt_func(vars1)))  # NOT option
    
    s2 = Solver()
    vars2 = {}
    for p in photographers:
        vars2[f'{p}_S'] = Bool(f'{p}_S')
        vars2[f'{p}_T'] = Bool(f'{p}_T')
    
    for p in photographers:
        s2.add(Not(And(vars2[f'{p}_S'], vars2[f'{p}_T'])))
    s2.add(Sum([If(vars2[f'{p}_S'], 1, 0) for p in photographers]) >= 2)
    s2.add(Sum([If(vars2[f'{p}_T'], 1, 0) for p in photographers]) >= 2)
    s2.add(Or(And(vars2['F_S'], vars2['H_S']), And(vars2['F_T'], vars2['H_T'])))
    both_assigned2 = And(Or(vars2['L_S'], vars2['L_T']), Or(vars2['M_S'], vars2['M_T']))
    different_ceremonies2 = Or(And(vars2['L_S'], vars2['M_T']), And(vars2['L_T'], vars2['M_S']))
    s2.add(Implies(both_assigned2, different_ceremonies2))
    s2.add(Implies(vars2['G_S'], vars2['L_T']))
    s2.add(opt_func(vars2))  # option
    s2.add(Not(Implies(Not(vars2['K_T']), And(vars2['H_T'], vars2['M_T']))))  # NOT C4
    
    if s1.check() == unsat and s2.check() == unsat:
        found_options.append(letter)

print(f"\nFINAL RESULT:")
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")