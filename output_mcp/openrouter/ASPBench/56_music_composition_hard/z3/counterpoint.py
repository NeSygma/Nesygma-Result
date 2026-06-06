from z3 import *

# Parameters
T = 8  # time steps
# Allowed pitch classes for C major
scale_pcs = {0,2,4,5,7,9,11}
# Allowed harmonic intervals (semitones)
allowed_intervals = {3,4,7,8,9,12,15,16}
# V-chord notes (MIDI numbers for G4=67, B4=71, D4=62) - but could be other octaves within range
V_notes = {67,71,62}

# Create variables
soprano = [Int(f'sop_{t}') for t in range(T)]
alto = [Int(f'alt_{t}') for t in range(T)]

solver = Solver()

# Voice ranges
for t in range(T):
    solver.add(soprano[t] >= 60, soprano[t] <= 81)  # C4 to A5
    solver.add(alto[t] >= 52, alto[t] <= 72)      # E3 to C5
    # Scale membership
    solver.add(Or([soprano[t] % 12 == pc for pc in scale_pcs]))
    solver.add(Or([alto[t] % 12 == pc for pc in scale_pcs]))
    # Voice crossing
    solver.add(soprano[t] > alto[t])
    # Harmonic interval allowed
    interval = soprano[t] - alto[t]
    solver.add(Or([interval == iv for iv in allowed_intervals]))

# Starting notes
solver.add(alto[0] == 60)  # C4
solver.add(Or(soprano[0] == 64, soprano[0] == 67))  # E4 or G4

# Cadence at time 7 (index 6)
for t in [6]:
    solver.add(Or([soprano[t] == v for v in V_notes]))
    solver.add(Or([alto[t] == v for v in V_notes]))
    # still ensure soprano > alto (already added)

# Final resolution at time 8 (index 7)
solver.add(soprano[7] == 72)  # C5
solver.add(alto[7] == 60)    # C4

# Melodic leaps <= perfect fifth (7 semitones)
for t in range(T-1):
    solver.add(Abs(soprano[t+1] - soprano[t]) <= 7)
    solver.add(Abs(alto[t+1] - alto[t]) <= 7)

# No parallel perfect fifths or octaves between consecutive steps
for t in range(T-1):
    int1 = soprano[t] - alto[t]
    int2 = soprano[t+1] - alto[t+1]
    # forbid both being 7 (perfect fifth) consecutively
    solver.add(Not(And(int1 == 7, int2 == 7)))
    # forbid both being 12 (octave) consecutively
    solver.add(Not(And(int1 == 12, int2 == 12)))

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Helper to convert MIDI to note name
    note_names = {0:"C",1:"C#",2:"D",3:"D#",4:"E",5:"F",6:"F#",7:"G",8:"G#",9:"A",10:"A#",11:"B"}
    for t in range(T):
        sop_val = m[soprano[t]].as_long()
        alt_val = m[alto[t]].as_long()
        interval = sop_val - alt_val
        sop_name = note_names[sop_val % 12] + str(sop_val // 12 - 1)  # MIDI octave: C4=60 => 60//12=5, 5-1=4
        alt_name = note_names[alt_val % 12] + str(alt_val // 12 - 1)
        print(f"time {t+1}: soprano_note = {sop_name}, alto_note = {alt_name}, harmonic_interval_semitones = {interval}")
else:
    print("STATUS: unsat")