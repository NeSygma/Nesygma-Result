from z3 import *

# Create solver
solver = Solver()

# Declare variables for each letter
D, O, N, A, L, G, E, R, B, T = Ints('D O N A L G E R B T')

# All letters must be between 0 and 9
letters = [D, O, N, A, L, G, E, R, B, T]
for letter in letters:
    solver.add(letter >= 0, letter <= 9)

# All digits must be unique
solver.add(Distinct(letters))

# Leading letters cannot be zero
solver.add(D != 0)
solver.add(G != 0)
solver.add(R != 0)

# Columnar addition constraints
# DONALD = D*100000 + O*10000 + N*1000 + A*100 + L*10 + D
# GERALD = G*100000 + E*10000 + R*1000 + A*100 + L*10 + D
# ROBERT = R*100000 + O*10000 + B*1000 + E*100 + R*10 + T

# Let's break it down column by column with carries
# Units column: D + D = T + 10*c1
# Tens column: L + L + c1 = R + 10*c2
# Hundreds column: A + A + c2 = E + 10*c3
# Thousands column: N + R + c3 = B + 10*c4
# Ten-thousands column: O + E + c4 = O + 10*c5
# Hundred-thousands column: D + G + c5 = R + 10*c6

# Carries (c1 to c6) can be 0 or 1 (since max sum is 9+9+1=19)
c1, c2, c3, c4, c5, c6 = Ints('c1 c2 c3 c4 c5 c6')
for c in [c1, c2, c3, c4, c5, c6]:
    solver.add(c >= 0, c <= 1)

# Column constraints
solver.add(D + D == T + 10*c1)  # Units
solver.add(L + L + c1 == R + 10*c2)  # Tens
solver.add(A + A + c2 == E + 10*c3)  # Hundreds
solver.add(N + R + c3 == B + 10*c4)  # Thousands
solver.add(O + E + c4 == O + 10*c5)  # Ten-thousands
solver.add(D + G + c5 == R + 10*c6)  # Hundred-thousands

# Check for solution
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("\nAssignment:")
    assignment = {}
    for letter in [D, O, N, A, L, G, E, R, B, T]:
        letter_name = str(letter)
        digit = model[letter].as_long()
        assignment[letter_name] = digit
        print(f"  {letter_name} = {digit}")
    
    # Build the equation string
    donald_num = assignment['D']*100000 + assignment['O']*10000 + assignment['N']*1000 + assignment['A']*100 + assignment['L']*10 + assignment['D']
    gerald_num = assignment['G']*100000 + assignment['E']*10000 + assignment['R']*1000 + assignment['A']*100 + assignment['L']*10 + assignment['D']
    robert_num = assignment['R']*100000 + assignment['O']*10000 + assignment['B']*1000 + assignment['E']*100 + assignment['R']*10 + assignment['T']
    
    print(f"\nEquation: {donald_num} + {gerald_num} = {robert_num}")
    print(f"Valid: {donald_num + gerald_num == robert_num}")
    
    # Verify the solution
    if donald_num + gerald_num == robert_num:
        print("\n✓ Solution verified!")
    else:
        print("\n✗ Solution verification failed!")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found - puzzle may be unsatisfiable")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")