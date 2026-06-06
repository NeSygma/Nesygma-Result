from z3 import *

# We have 3 kinds: Oatmeal (O), Peanut Butter (P), Sugar (S)
# Each kind has 3 batches (1st, 2nd, 3rd)
# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4

# The question: "If one kind of cookie's first batch is made on the same day as another kind of cookie's third batch, then which one of the following could be false?"
# This means: given the condition holds, which option is NOT necessarily true?
# i.e., which option CAN be false (its negation is satisfiable)?

# Let's test each option: can it be false while the condition holds?

O = [Int(f'O_{i}') for i in range(3)]
P = [Int(f'P_{i}') for i in range(3)]
S = [Int(f'S_{i}') for i in range(3)]
all_batches = O + P + S

found_options = []

for letter in ["A", "B", "C", "D", "E"]:
    s = Solver()
    
    # Domain
    for b in all_batches:
        s.add(b >= 0, b <= 4)
    
    # No two batches of same kind on same day
    s.add(Distinct(O))
    s.add(Distinct(P))
    s.add(Distinct(S))
    
    # At least one batch on Monday
    s.add(Or([b == 0 for b in all_batches]))
    
    # Second oatmeal = first peanut butter
    s.add(O[1] == P[0])
    
    # Second sugar on Thursday (day 3)
    s.add(S[1] == 3)
    
    # Condition: one kind's first batch = another kind's third batch
    first_batch = [O[0], P[0], S[0]]
    third_batch = [O[2], P[2], S[2]]
    
    condition = Or([
        And(i != j, first_batch[i] == third_batch[j])
        for i in range(3) for j in range(3)
    ])
    s.add(condition)
    
    # Add the NEGATION of the option (to see if it CAN be false)
    if letter == "A":
        # Negation of "at least one batch on each day"
        s.add(Not(And([Or([b == d for b in all_batches]) for d in range(5)])))
    elif letter == "B":
        # Negation of "at least two batches on Wednesday (day 2)"
        s.add(Sum([If(b == 2, 1, 0) for b in all_batches]) < 2)
    elif letter == "C":
        # Negation of "exactly one batch on Monday (day 0)"
        s.add(Sum([If(b == 0, 1, 0) for b in all_batches]) != 1)
    elif letter == "D":
        # Negation of "exactly two batches on Tuesday (day 1)"
        s.add(Sum([If(b == 1, 1, 0) for b in all_batches]) != 2)
    elif letter == "E":
        # Negation of "exactly one batch on Friday (day 4)"
        s.add(Sum([If(b == 4, 1, 0) for b in all_batches]) != 1)
    
    res = s.check()
    print(f"Option {letter} negation: {res}")
    if res == sat:
        found_options.append(letter)
        m = s.model()
        print(f"  O: {m[O[0]]}, {m[O[1]]}, {m[O[2]]}")
        print(f"  P: {m[P[0]]}, {m[P[1]]}, {m[P[2]]}")
        print(f"  S: {m[S[0]]}, {m[S[1]]}, {m[S[2]]}")

print(f"\nFound options (can be false): {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")