% Slots are numbered 1 to 6
slot(1..6).

% Bands
band(uneasy). band(vegemite). band(wellspring). band(xpert). band(yardsign). band(zircon).

% Each band performs in exactly one slot
1 { performs(B, S) : slot(S) } 1 :- band(B).

% Each slot has exactly one band
1 { performs(B, S) : band(B) } 1 :- slot(S).

% Constraints:
% 1. Vegemite performs in an earlier slot than Zircon
:- performs(vegemite, S1), performs(zircon, S2), S1 >= S2.

% 2. Wellspring and Zircon each perform in an earlier slot than Xpert
:- performs(wellspring, S1), performs(xpert, S2), S1 >= S2.
:- performs(zircon, S1), performs(xpert, S2), S1 >= S2.

% 3. Uneasy performs in one of the last three slots
:- performs(uneasy, S), S <= 3.

% 4. Yardsign performs in one of the first three slots
:- performs(yardsign, S), S > 3.

% Check if slot 5 can be assigned to each band
% We want to find which band CANNOT be in slot 5

% Define the slot 5 assignment for each band
slot5_uneasy :- performs(uneasy, 5).
slot5_vegemite :- performs(vegemite, 5).
slot5_wellspring :- performs(wellspring, 5).
slot5_xpert :- performs(xpert, 5).
slot5_yardsign :- performs(yardsign, 5).
slot5_zircon :- performs(zircon, 5).

% Map the correct answer to option/1
% We want to find which band CANNOT be in slot 5
% So we check for which band it is impossible to have performs(Band, 5) while satisfying all constraints

% To determine which band cannot be in slot 5, we check for each band if it is possible to assign it to slot 5
% If it is impossible, then that band cannot be in slot 5

% We will use the following logic:
% For each band, if it is impossible to assign it to slot 5 while satisfying all constraints, then option(X) should be true for that band

% We will use a choice rule to allow Clingo to explore possibilities and constraints to rule out invalid assignments

% Define which bands can be in slot 5
possible_slot5_uneasy   :- slot5_uneasy.
possible_slot5_vegemite :- slot5_vegemite.
possible_slot5_wellspring :- slot5_wellspring.
possible_slot5_xpert   :- slot5_xpert.
possible_slot5_yardsign :- slot5_yardsign.
possible_slot5_zircon  :- slot5_zircon.

% If a band cannot be in slot 5, it means there is no valid assignment where it is in slot 5
% So we derive the negation of possible_slot5_X for the band that cannot be in slot 5

% Since we want to find which band CANNOT be in slot 5, we will check for each band if it is impossible to assign it to slot 5
% We will use constraints to rule out assignments that violate the constraints

% To find which band cannot be in slot 5, we will check for each band if it is possible to assign it to slot 5
% If it is not possible, then that band cannot be in slot 5

% We will use the following approach:
% For each band, assume it is in slot 5 and check if the constraints are satisfied
% If not, then that band cannot be in slot 5

% We will use integrity constraints to rule out invalid assignments

% Rule out assignments where Uneasy is in slot 5 and constraints are violated
:- performs(uneasy, 5), not possible_slot5_uneasy.

% Rule out assignments where Vegemite is in slot 5 and constraints are violated
:- performs(vegemite, 5), not possible_slot5_vegemite.

% Rule out assignments where Wellspring is in slot 5 and constraints are violated
:- performs(wellspring, 5), not possible_slot5_wellspring.

% Rule out assignments where Xpert is in slot 5 and constraints are violated
:- performs(xpert, 5), not possible_slot5_xpert.

% Rule out assignments where Yardsign is in slot 5 and constraints are violated
:- performs(yardsign, 5), not possible_slot5_yardsign.

% Rule out assignments where Zircon is in slot 5 and constraints are violated
:- performs(zircon, 5), not possible_slot5_zircon.

% Now, we want to find which band CANNOT be in slot 5
% We will use the following logic:
% If a band cannot be in slot 5, then there is no valid assignment where it is in slot 5
% So we will derive option(X) for the band that cannot be in slot 5

% We will use the following rules to map the answer

% If Uneasy cannot be in slot 5, then option(a) is true
option(a) :- not possible_slot5_uneasy, band(uneasy).

% If Vegemite cannot be in slot 5, then option(b) is true
option(b) :- not possible_slot5_vegemite, band(vegemite).

% If Wellspring cannot be in slot 5, then option(c) is true
option(c) :- not possible_slot5_wellspring, band(wellspring).

% If Xpert cannot be in slot 5, then option(d) is true
option(d) :- not possible_slot5_xpert, band(xpert).

% If Zircon cannot be in slot 5, then option(e) is true
option(e) :- not possible_slot5_zircon, band(zircon).

% Yardsign is allowed in slot 5, so it is not an option

#show option/1.