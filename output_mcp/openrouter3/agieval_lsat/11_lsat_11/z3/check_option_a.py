from z3 import *

# Check option A specifically
solver = Solver()

FN = Int('FN')  # 0-3
RN = Int('RN')  # 0-3
FP = Int('FP')  # 0-2
RP = Int('RP')  # 0-1

solver.add(FN >= 0, FN <= 3)
solver.add(RN >= 0, RN <= 3)
solver.add(FP >= 0, FP <= 2)
solver.add(RP >= 0, RP <= 1)

total = FN + RN + FP + RP
solver.add(total >= 5, total <= 6)

solver.add(FN + FP <= 4)  # No more than 4 French works
solver.add(FN + RN >= 3, FN + RN <= 4)  # At least 3 but no more than 4 novels
solver.add(FN >= RN)  # At least as many French novels as Russian novels
solver.add(Implies(FP == 2, RP == 0))  # If both French plays selected, then Russian play not selected

# Option A: No Russian novels and exactly one play are selected
solver.add(RN == 0)
solver.add(FP + RP == 1)

result = solver.check()
if result == sat:
    print("Option A is possible!")
    m = solver.model()
    print(f"FN={m[FN]}, RN={m[RN]}, FP={m[FP]}, RP={m[RP]}")
    print(f"Total={m[FN]+m[RN]+m[FP]+m[RP]}")
else:
    print("Option A is NOT possible (as expected)")
    print("This confirms A is the exception")