% Define the slots
slot(1..6).

% Define the bands
band(uneasy).
band(vegemite).
band(wellspring).
band(xpert).
band(yardsign).
band(zircon).

% Each band is assigned to exactly one slot
1 { assigned(Band, Slot) : slot(Slot) } 1 :- band(Band).

% Each slot has exactly one band
1 { assigned(Band, Slot) : band(Band) } 1 :- slot(Slot).

% Vegemite performs in an earlier slot than Zircon
:- assigned(vegemite, S1), assigned(zircon, S2), S1 >= S2.

% Wellspring performs in an earlier slot than Xpert
:- assigned(wellspring, S1), assigned(xpert, S2), S1 >= S2.

% Zircon performs in an earlier slot than Xpert
:- assigned(zircon, S1), assigned(xpert, S2), S1 >= S2.

% Uneasy performs in one of the last three slots (4,5,6)
:- assigned(uneasy, S), S < 4.

% Yardsign performs in one of the first three slots (1,2,3)
:- assigned(yardsign, S), S > 3.

% Zircon performs immediately before Wellspring
% This ensures Wellspring is in the slot immediately after Zircon
:- assigned(zircon, S1), assigned(wellspring, S2), S2 != S1 + 1.

% Map the correct answer to option/1
% Zircon must be in slot 3 given the constraints
option(e) :- assigned(zircon, 3).

#show option/1.