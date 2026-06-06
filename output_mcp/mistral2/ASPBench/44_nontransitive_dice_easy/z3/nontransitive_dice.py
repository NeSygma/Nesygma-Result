from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare dice as arrays of 6 integer variables each
A = [Int(f'A_{i}') for i in range(6)]
B = [Int(f'B_{i}') for i in range(6)]
C = [Int(f'C_{i}') for i in range(6)]

# Each face value must be in {0, 1, 2, 3, 4, 5, 6}
solver = Solver()
for die in [A, B, C]:
    for face in die:
        solver.add(face >= 0, face <= 6)

# Helper function to compute P(X > Y) > 0.5
def beats_probability(X, Y):
    # Count the number of pairs (x, y) where x > y
    count = 0
    for x in X:
        for y in Y:
            count += If(x > y, 1, 0)
    # Total pairs = 36
    # P(X > Y) > 0.5  => count > 18
    return count > 18

# Add constraints for nontransitive dominance
solver.add(beats_probability(A, B))
solver.add(beats_probability(B, C))
solver.add(beats_probability(C, A))

# Check for a satisfying assignment
result = solver.check()

if result == sat:
    model = solver.model()
    dice = {
        "A": [model.eval(face, model_completion=True) for face in A],
        "B": [model.eval(face, model_completion=True) for face in B],
        "C": [model.eval(face, model_completion=True) for face in C]
    }
    # Compute win probabilities for the found dice
    def compute_win_prob(X, Y):
        count = 0
        for x in X:
            for y in Y:
                if model.eval(x > y, model_completion=True):
                    count += 1
        return count / 36.0

    win_probabilities = {
        "A_beats_B": compute_win_prob(dice["A"], dice["B"]),
        "B_beats_C": compute_win_prob(dice["B"], dice["C"]),
        "C_beats_A": compute_win_prob(dice["C"], dice["A"])
    }
    print("STATUS: sat")
    print("dice =", dice)
    print("win_probabilities =", win_probabilities)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")