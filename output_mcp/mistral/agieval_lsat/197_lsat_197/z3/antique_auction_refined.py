from z3 import *

# Declare the antiques and days
antiques = ["harmonica", "lamp", "mirror", "sundial", "table", "vase"]
days = range(1, 7)  # June 1st to June 6th

# Create a dictionary to map each antique to its auction day
auction_day = {a: Int(f"{a}_day") for a in antiques}

# Create the solver
solver = Solver()

# Constraint 1: The sundial is not auctioned on June 1st
solver.add(auction_day["sundial"] != 1)

# Constraint 2: If the harmonica is auctioned earlier than the lamp, then the mirror is also auctioned earlier than the lamp
solver.add(Implies(
    auction_day["harmonica"] < auction_day["lamp"],
    auction_day["mirror"] < auction_day["lamp"]
))

# Constraint 3: The sundial is auctioned earlier than the mirror and earlier than the vase
solver.add(auction_day["sundial"] < auction_day["mirror"])
solver.add(auction_day["sundial"] < auction_day["vase"])

# Constraint 4: The table is auctioned earlier than the harmonica or earlier than the vase, but not both
solver.add(
    Xor(
        And(
            auction_day["table"] < auction_day["harmonica"],
            Not(auction_day["table"] < auction_day["vase"])
        ),
        And(
            auction_day["table"] < auction_day["vase"],
            Not(auction_day["table"] < auction_day["harmonica"])
        )
    )
)

# All antiques are auctioned on distinct days
solver.add(Distinct(list(auction_day.values())))

# Evaluate each option
found_options = []

# Option A: The table is auctioned on June 2nd and the lamp is auctioned on June 3rd
solver.push()
solver.add(auction_day["table"] == 2)
solver.add(auction_day["lamp"] == 3)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The sundial is auctioned on June 2nd and the vase is auctioned on June 3rd
solver.push()
solver.add(auction_day["sundial"] == 2)
solver.add(auction_day["vase"] == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: The mirror is auctioned on June 3rd and the sundial is auctioned on June 4th
solver.push()
solver.add(auction_day["mirror"] == 3)
solver.add(auction_day["sundial"] == 4)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The vase is auctioned on June 4th and the sundial is auctioned on June 5th
solver.push()
solver.add(auction_day["vase"] == 4)
solver.add(auction_day["sundial"] == 5)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The sundial is auctioned on June 4th and the table is auctioned on June 5th
solver.push()
solver.add(auction_day["sundial"] == 4)
solver.add(auction_day["table"] == 5)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")