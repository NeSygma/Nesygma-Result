from z3 import *

# Define variables
IW, IV = Int('IW'), Int('IV')
SW, SV = Int('SW'), Int('SV')
TW, TV = Int('TW'), Int('TV')

# Base constraints
s = Solver()
for v in [IW, IV, SW, SV, TW, TV]:
    s.add(v >= 1, v <= 3)
s.add(IW <= IV)
s.add(SW <= SV)
s.add(TW <= TV)
s.add(IV < SV)
s.add(IV < TV)
s.add(SW < TW)
s.add(TW < TV)

# Q: If Truvest's website target is shorter than its voicemail target (TW < TV)
# This is already in the base constraints (TW < TV).
# Wait, let me re-read: "If Truvest's website target is shorter than its voicemail target"
# My base constraints already had TW < TV. Let me check if that was implied.
# "None of the clients can have a website target that is longer than its voicemail target."
# This means TW <= TV.
# The question adds the condition TW < TV.

# Let's re-evaluate the base constraints.
# "None of the clients can have a website target that is longer than its voicemail target."
# IW <= IV, SW <= SV, TW <= TV.
# "Image's voicemail target must be shorter than the other clients' voicemail targets."
# IV < SV, IV < TV.
# "Solide's website target must be shorter than Truvest's website target."
# SW < TW.

# The question adds: "If Truvest's website target is shorter than its voicemail target"
# So TW < TV.

# Let's re-run the check with the specific condition TW < TV.

s = Solver()
for v in [IW, IV, SW, SV, TW, TV]:
    s.add(v >= 1, v <= 3)
s.add(IW <= IV)
s.add(SW <= SV)
s.add(TW <= TV)
s.add(IV < SV)
s.add(IV < TV)
s.add(SW < TW)
s.add(TW < TV) # The condition

options = {
    "A": IV == 2,
    "B": IW == 2,
    "C": IW == 1,
    "D": SW == 2,
    "E": SW == 1
}

found_options = []
for letter, constr in options.items():
    s.push()
    s.add(Not(constr))
    if s.check() == unsat:
        found_options.append(letter)
    s.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")