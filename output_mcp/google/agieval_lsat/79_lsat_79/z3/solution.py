from z3 import *

businesses = ['O', 'P', 'R1', 'R2', 'S', 'T', 'V']
pos = {b: Int(f'pos_{b}') for b in businesses}

solver = Solver()
for b in businesses:
    solver.add(pos[b] >= 1, pos[b] <= 7)
solver.add(Distinct([pos[b] for b in businesses]))
solver.add(Or(
    And(pos['P'] == 1, Or(pos['R1'] == 7, pos['R2'] == 7)),
    And(pos['P'] == 7, Or(pos['R1'] == 1, pos['R2'] == 1))
))
solver.add(Abs(pos['R1'] - pos['R2']) >= 3)
solver.add(Or(Abs(pos['P'] - pos['O']) == 1, Abs(pos['P'] - pos['V']) == 1))
solver.add(Abs(pos['T'] - pos['V']) != 1)
solver.add(Abs(pos['O'] - pos['S']) == 1)

def get_business_at(p, model):
    for b in businesses:
        if model[pos[b]].as_long() == p:
            return b
    return None

# Define options as constraints
# Option D: a restaurant and the toy store
# This means {b1, b2} = {R1, T} or {R2, T}
def check_option(opt_name):
    solver.push()
    # Add constraint for the option
    # The pair is (O, S). Let k = min(pos[O], pos[S]).
    # The businesses on either side are at k-1 and k+2.
    # We need to check if for all valid models, the set {b(k-1), b(k+2)} matches the option.
    
    # This is tricky because the option must be true for ALL valid models.
    # Let's find all valid models and check if they all satisfy the option.
    
    all_models_satisfy = True
    while solver.check() == sat:
        m = solver.model()
        k = min(m[pos['O']].as_long(), m[pos['S']].as_long())
        
        # Check if both sides exist
        if k - 1 >= 1 and k + 2 <= 7:
            b1 = get_business_at(k - 1, m)
            b2 = get_business_at(k + 2, m)
            side_businesses = {b1, b2}
            
            # Check against options
            if opt_name == "D":
                # {R1, T} or {R2, T}
                if not (side_businesses == {'R1', 'T'} or side_businesses == {'R2', 'T'}):
                    all_models_satisfy = False
            # Add other options if needed
        else:
            # If the pair is at the end, the question might not apply or the option is invalid.
            # The question says "the businesses immediately on either side of this pair",
            # which implies both sides exist.
            pass
        
        solver.add(Or([pos[b] != m[pos[b]] for b in businesses]))
    
    solver.pop()
    return all_models_satisfy

# Check option D
if check_option("D"):
    print("STATUS: sat")
    print("answer:D")
else:
    print("STATUS: unsat")