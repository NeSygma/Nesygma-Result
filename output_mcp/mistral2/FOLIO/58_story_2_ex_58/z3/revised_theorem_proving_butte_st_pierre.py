from z3 import *

# Define symbolic constants for cities and states
Billings = Int('Billings')
Butte = Int('Butte')
Helena = Int('Helena')
Missoula = Int('Missoula')
White_Sulphur_Springs = Int('White_Sulphur_Springs')
St_Pierre = Int('St_Pierre')

Montana = Int('Montana')
OtherState = Int('OtherState')  # For St Pierre's state

# Exception cities that can be in multiple states
Bristol = Int('Bristol')
Texarkana = Int('Texarkana')
Texhoma = Int('Texhoma')
Union_City = Int('Union_City')

# Function to map a city to its state
city_state = Function('city_state', IntSort(), IntSort())

# Solver for checking entailment: premises + not(conclusion)
solver_entail = Solver()

# Premises
# 1. Billings is a city in the state of Montana in U.S.
solver_entail.add(city_state(Billings) == Montana)

# 2. The state of Montana includes the cities of Butte, Helena, and Missoula.
solver_entail.add(city_state(Butte) == Montana)
solver_entail.add(city_state(Helena) == Montana)
solver_entail.add(city_state(Missoula) == Montana)

# 3. White Sulphur Springs and Butte are cities in the same state in U.S.
solver_entail.add(city_state(White_Sulphur_Springs) == city_state(Butte))

# 4. The city of St Pierre is not in the state of Montana.
solver_entail.add(city_state(St_Pierre) != Montana)

# 5. Any city in Butte is not in St Pierre.
# Interpretation: The city of Butte is not in the same state as St Pierre
solver_entail.add(city_state(Butte) != city_state(St_Pierre))

# 6. A city can only be in one state in U.S. except for Bristol, Texarkana, Texhoma and Union City.
# This means that for the exception cities, their state can be equal to other states or not.
# For non-exception cities, we do not enforce uniqueness of state assignment across cities.
# The only constraint is that a city's state is a single state (already modeled by the function).
# So no additional constraints are needed here.

# Check if premises + not(conclusion) is unsatisfiable
# Conclusion: Butte and St Pierre are in the same state
# not(conclusion): Butte and St Pierre are NOT in the same state
# Since premise 5 already states city_state(Butte) != city_state(St_Pierre),
# the not(conclusion) is already in the premises.
# So this check is essentially checking if the premises are consistent.

result_entail = solver_entail.check()

# Solver for checking contradiction: premises + conclusion
solver_contradict = Solver()

# Same premises as above
solver_contradict.add(city_state(Billings) == Montana)
solver_contradict.add(city_state(Butte) == Montana)
solver_contradict.add(city_state(Helena) == Montana)
solver_contradict.add(city_state(Missoula) == Montana)
solver_contradict.add(city_state(White_Sulphur_Springs) == city_state(Butte))
solver_contradict.add(city_state(St_Pierre) != Montana)
solver_contradict.add(city_state(Butte) != city_state(St_Pierre))

# Conclusion: Butte and St Pierre are in the same state
solver_contradict.add(city_state(Butte) == city_state(St_Pierre))

result_contradict = solver_contradict.check()

# Interpret results
print("=== Checking if premises entail the conclusion ===")
print(f"Premises + not(conclusion) satisfiable: {result_entail == sat}")

print("\n=== Checking if premises contradict the conclusion ===")
print(f"Premises + conclusion satisfiable: {result_contradict == sat}")

# Determine the status
if result_entail == unsat and result_contradict == sat:
    print("\nSTATUS: proved")
    print("CONCLUSION: False")
elif result_entail == sat and result_contradict == unsat:
    print("\nSTATUS: proved")
    print("CONCLUSION: True")
elif result_entail == sat and result_contradict == sat:
    print("\nSTATUS: proved")
    print("CONCLUSION: Uncertain")
elif result_entail == unsat and result_contradict == unsat:
    print("\nSTATUS: unknown")
    print("CONCLUSION: Inconsistent premises")
else:
    print("\nSTATUS: unknown")
    print("CONCLUSION: Inconclusive")