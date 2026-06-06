% Domains
slot(1..6).
band(uneasy; vegemite; wellspring; xpert; yardsign; zircon).

% Assign each band to exactly one slot
1 { assignment(Band, Slot) : slot(Slot) } 1 :- band(Band).

% Each slot has exactly one band
1 { assignment(Band, Slot) : band(Band) } 1 :- slot(Slot).

% Constraint 1: Vegemite performs earlier than Zircon
:- assignment(vegemite, S1), assignment(zircon, S2), S1 >= S2.

% Constraint 2: Wellspring and Zircon each perform earlier than Xpert
:- assignment(wellspring, S1), assignment(xpert, S2), S1 >= S2.
:- assignment(zircon, S1), assignment(xpert, S2), S1 >= S2.

% Constraint 3: Uneasy performs in one of the last three slots
:- assignment(uneasy, S), S < 4.

% Constraint 4: Yardsign performs in one of the first three slots
:- assignment(yardsign, S), S > 3.

% Additional constraint from the question: Zircon performs earlier than Yardsign
:- assignment(zircon, S1), assignment(yardsign, S2), S1 >= S2.

% Derive the slot for each band for easier reference
slot_assignment(Band, Slot) :- assignment(Band, Slot).

% Determine the earliest possible slot for Wellspring
% We want to find the minimum slot number for Wellspring that satisfies all constraints
% Since we're looking for the earliest possible slot, we can derive it directly

% The question asks: which one of the following is the earliest slot in which Wellspring could perform?
% So we need to check if Wellspring can be in slot 2, 3, 4, 5, or 6

% Let's derive the possible slots for Wellspring
possible_slot_for_wellspring(2) :- slot_assignment(wellspring, 2).
possible_slot_for_wellspring(3) :- slot_assignment(wellspring, 3).
possible_slot_for_wellspring(4) :- slot_assignment(wellspring, 4).
possible_slot_for_wellspring(5) :- slot_assignment(wellspring, 5).
possible_slot_for_wellspring(6) :- slot_assignment(wellspring, 6).

% Find the minimum slot for Wellspring
min_wellspring_slot(S) :- S = #min { Slot : slot_assignment(wellspring, Slot) }.

% Map the answer choices to the derived slot
% The earliest slot Wellspring could perform is the minimum slot
option(a) :- min_wellspring_slot(2).
option(b) :- min_wellspring_slot(3).
option(c) :- min_wellspring_slot(4).
option(d) :- min_wellspring_slot(5).
option(e) :- min_wellspring_slot(6).

#show option/1.