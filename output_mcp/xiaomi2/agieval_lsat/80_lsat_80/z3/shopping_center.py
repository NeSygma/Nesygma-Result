from z3 import *

# 7 businesses, each assigned to a space 1-7
# O=Optometrist, P=Pharmacy, R1=Restaurant1, R2=Restaurant2, S=ShoeStore, T=ToyStore, V=Veterinarian
O, P, R1, R2, S, T, V = Ints('O P R1 R2 S T V')
businesses = [O, P, R1, R2, S, T, V]

def base_constraints():
    """Return list of base constraints for the problem."""
    cons = []
    # Each business in a distinct space 1-7
    for b in businesses:
        cons.append(And(b >= 1, b <= 7))
    cons.append(Distinct(businesses))
    
    # Constraint 1: Pharmacy at one end, one restaurant at the other end
    cons.append(Or(
        And(P == 1, Or(R1 == 7, R2 == 7)),
        And(P == 7, Or(R1 == 1, R2 == 1))
    ))
    
    # Constraint 2: Two restaurants separated by at least 2 other businesses
    cons.append(Abs(R1 - R2) >= 3)
    
    # Constraint 3: Pharmacy next to optometrist or veterinarian
    cons.append(Or(Abs(P - O) == 1, Abs(P - V) == 1))
    
    # Constraint 4: Toy store cannot be next to veterinarian
    cons.append(Abs(T - V) != 1)
    
    # Constraint 5: Shoe store in space 4
    cons.append(S == 4)
    
    return cons

# Define the options as constraints
# (A) The optometrist is next to a restaurant
opt_a = Or(Abs(O - R1) == 1, Abs(O - R2) == 1)
# (B) The pharmacy is next to the veterinarian
opt_b = Abs(P - V) == 1
# (C) A restaurant is next to the toy store
opt_c = Or(Abs(R1 - T) == 1, Abs(R2 - T) == 1)
# (D) The shoe store is next to the toy store
opt_d = Abs(S - T) == 1
# (E) The shoe store is next to the veterinarian
opt_e = Abs(S - V) == 1

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

# For "must be true" questions: check if negation of each option is UNSAT
# If negation is UNSAT, the option must be true in all valid configurations
must_be_true = []

for letter, opt_constr in options:
    s = Solver()
    s.add(base_constraints())
    s.add(Not(opt_constr))  # Try to find a valid config where option is FALSE
    result = s.check()
    if result == unsat:
        # The option must be true (no counterexample exists)
        must_be_true.append(letter)
        print(f"Option {letter}: MUST BE TRUE (negation is UNSAT)")
    elif result == sat:
        print(f"Option {letter}: NOT necessarily true (counterexample found)")
        m = s.model()
        print(f"  Counterexample: O={m[O]}, P={m[P]}, R1={m[R1]}, R2={m[R2]}, S={m[S]}, T={m[T]}, V={m[V]}")
    else:
        print(f"Option {letter}: UNKNOWN")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")