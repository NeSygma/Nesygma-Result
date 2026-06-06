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

% Define the band in slot 1
band_in_slot1(B) :- assigned(B, 1).

% Determine which bands can be in slot 1
% A band can be in slot 1 if there exists at least one valid assignment where it is in slot 1
possible_in_slot1(vegemite) :- band_in_slot1(vegemite).
possible_in_slot1(wellspring) :- band_in_slot1(wellspring).
possible_in_slot1(yardsign) :- band_in_slot1(yardsign).
possible_in_slot1(zircon) :- band_in_slot1(zircon).

% Map the correct answer to option/1
option(a) :- possible_in_slot1(yardsign), not possible_in_slot1(vegemite), not possible_in_slot1(wellspring), not possible_in_slot1(zircon).
option(b) :- possible_in_slot1(vegemite), possible_in_slot1(wellspring), not possible_in_slot1(yardsign), not possible_in_slot1(zircon).
option(c) :- possible_in_slot1(vegemite), possible_in_slot1(yardsign), not possible_in_slot1(wellspring), not possible_in_slot1(zircon).
option(d) :- possible_in_slot1(vegemite), possible_in_slot1(wellspring), possible_in_slot1(yardsign), not possible_in_slot1(zircon).
option(e) :- possible_in_slot1(vegemite), possible_in_slot1(wellspring), possible_in_slot1(yardsign), possible_in_slot1(zircon).

#show option/1.