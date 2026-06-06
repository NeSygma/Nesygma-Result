from z3 import *

# We have 6 lab assistants: Julio, Kevin, Lan, Nessa, Olivia, Rebecca
# 3 days: Wednesday, Thursday, Friday
# Each day has a morning and afternoon session
# So we have 6 slots: 0=WedAM, 1=WedPM, 2=ThuAM, 3=ThuPM, 4=FriAM, 5=FriPM

J, K, L, N, O, R = Ints('J K L N O R')

solver = Solver()

# Each assistant gets a distinct slot 0-5
solver.add(Distinct(J, K, L, N, O, R))
for v in [J, K, L, N, O, R]:
    solver.add(v >= 0, v <= 5)

# Helper functions using Z3 expressions
# day(slot) = slot // 2  (0=Wed, 1=Thu, 2=Fri)
# time(slot) = slot % 2  (0=morning, 1=afternoon)

# Constraint 1: Kevin and Rebecca must lead sessions on the same day
# day(K) == day(R)  =>  K//2 == R//2
solver.add(K / 2 == R / 2)

# Constraint 2: Lan and Olivia cannot lead sessions on the same day
solver.add(L / 2 != O / 2)

# Constraint 3: Nessa must lead an afternoon session
# time(N) == 1  =>  N % 2 == 1
solver.add(N % 2 == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's
# day(J) < day(O)  =>  J//2 < O//2
solver.add(J / 2 < O / 2)

# Now define each option as a constraint that the assignment matches that option
# Option A: Wednesday: Rebecca, Kevin | Thursday: Julio, Lan | Friday: Nessa, Olivia
# Slot 0 (WedAM)=Rebecca, Slot1 (WedPM)=Kevin, Slot2 (ThuAM)=Julio, Slot3 (ThuPM)=Lan, Slot4 (FriAM)=Nessa, Slot5 (FriPM)=Olivia
opt_a = And(R==0, K==1, J==2, L==3, N==4, O==5)

# Option B: Wednesday: Olivia, Nessa | Thursday: Julio, Lan | Friday: Kevin, Rebecca
opt_b = And(O==0, N==1, J==2, L==3, K==4, R==5)

# Option C: Wednesday: Lan, Kevin | Thursday: Rebecca, Julio | Friday: Olivia, Nessa
opt_c = And(L==0, K==1, R==2, J==3, O==4, N==5)

# Option D: Wednesday: Kevin, Rebecca | Thursday: Julio, Nessa | Friday: Olivia, Lan
opt_d = And(K==0, R==1, J==2, N==3, O==4, L==5)

# Option E: Wednesday: Julio, Lan | Thursday: Olivia, Nessa | Friday: Rebecca, Kevin
opt_e = And(J==0, L==1, O==2, N==3, R==4, K==5)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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