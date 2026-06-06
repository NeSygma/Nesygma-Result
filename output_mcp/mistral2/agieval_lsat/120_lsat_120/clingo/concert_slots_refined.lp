% Define the bands and slots
band(uneasy).
band(vegemite).
band(wellspring).
band(xpert).
band(yardsign).
band(zircon).

slot(1..6).

% Assign each band to a unique slot
1 { assigned(B, S) : slot(S) } 1 :- band(B).
:- slot(S), band(B1), band(B2), B1 != B2, assigned(B1, S), assigned(B2, S).

% Constraints
% 1. Vegemite performs in an earlier slot than Zircon
:- assigned(vegemite, S1), assigned(zircon, S2), S1 >= S2.

% 2. Wellspring and Zircon each perform in an earlier slot than Xpert
:- assigned(wellspring, S1), assigned(xpert, S2), S1 >= S2.
:- assigned(zircon, S1), assigned(xpert, S2), S1 >= S2.

% 3. Uneasy performs in one of the last three slots
:- assigned(uneasy, S), S < 4.

% 4. Yardsign performs in one of the first three slots
:- assigned(yardsign, S), S > 3.

% Check for each band if it can be in slot 1
% We use a choice rule to allow Clingo to explore assignments where a specific band is in slot 1
{ band_in_slot1(B) : band(B) } 1.

% Ensure that the assignment is valid under the constraints
:- band_in_slot1(B), not assigned(B, 1).

% Define valid_assignment as a constraint satisfaction check
valid_assignment :-
    assigned(vegemite, S1), assigned(zircon, S2), S1 < S2,
    assigned(wellspring, S3), assigned(xpert, S4), S3 < S4,
    assigned(zircon, S5), assigned(xpert, S6), S5 < S6,
    assigned(uneasy, S7), S7 >= 4,
    assigned(yardsign, S8), S8 =< 3.

% If valid_assignment holds, then the band_in_slot1(B) is a possible candidate for slot 1
possible_in_slot1(B) :- band_in_slot1(B), valid_assignment.

% Map the correct answer to option/1
option(a) :- possible_in_slot1(yardsign), not possible_in_slot1(vegemite), not possible_in_slot1(wellspring), not possible_in_slot1(zircon).
option(b) :- possible_in_slot1(vegemite), possible_in_slot1(wellspring), not possible_in_slot1(yardsign), not possible_in_slot1(zircon).
option(c) :- possible_in_slot1(vegemite), possible_in_slot1(yardsign), not possible_in_slot1(wellspring), not possible_in_slot1(zircon).
option(d) :- possible_in_slot1(vegemite), possible_in_slot1(wellspring), possible_in_slot1(yardsign), not possible_in_slot1(zircon).
option(e) :- possible_in_slot1(vegemite), possible_in_slot1(wellspring), possible_in_slot1(yardsign), possible_in_slot1(zircon).

#show possible_in_slot1/1.
#show option/1.