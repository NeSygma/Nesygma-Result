% Define slots and bands
slot(1..6).
band(uneasy; vegemite; wellspring; xpert; yardsign; zircon).

% Assignment constraints: each band in exactly one slot
1 { assigned(Band, Slot) : slot(Slot) } 1 :- band(Band).
1 { assigned(Band, Slot) : band(Band) } 1 :- slot(Slot).

% Problem constraints:
% 1. Vegemite performs earlier than Zircon
:- assigned(vegemite, S1), assigned(zircon, S2), S1 >= S2.

% 2. Wellspring and Zircon each perform earlier than Xpert
:- assigned(wellspring, S1), assigned(xpert, S2), S1 >= S2.
:- assigned(zircon, S1), assigned(xpert, S2), S1 >= S2.

% 3. Uneasy performs in one of the last three slots (4, 5, or 6)
:- assigned(uneasy, S), S < 4.

% 4. Yardsign performs in one of the first three slots (1, 2, or 3)
:- assigned(yardsign, S), S > 3.

% Check if a band can be in slot 5 by allowing it to be assigned to slot 5
% and ensuring all constraints are satisfied
{ band_in_slot5(Band) : band(Band) }.

% If a band is in slot 5, enforce that it is assigned to slot 5
assigned(Band, 5) :- band_in_slot5(Band).

% Check if the assignment is valid (no constraints violated)
valid_assignment :-
    not violated_constraints.

violated_constraints :-
    assigned(vegemite, S1), assigned(zircon, S2), S1 >= S2.
violated_constraints :-
    assigned(wellspring, S1), assigned(xpert, S2), S1 >= S2.
violated_constraints :-
    assigned(zircon, S1), assigned(xpert, S2), S1 >= S2.
violated_constraints :-
    assigned(uneasy, S), S < 4.
violated_constraints :-
    assigned(yardsign, S), S > 3.

% The band that can be in slot 5 is the one for which there exists a valid assignment
can_be_in_slot5(uneasy)   :- valid_assignment, assigned(uneasy, 5).
can_be_in_slot5(vegemite) :- valid_assignment, assigned(vegemite, 5).
can_be_in_slot5(wellspring) :- valid_assignment, assigned(wellspring, 5).
can_be_in_slot5(xpert)     :- valid_assignment, assigned(xpert, 5).
can_be_in_slot5(zircon)    :- valid_assignment, assigned(zircon, 5).

% The band that CANNOT be in slot 5 is the one for which can_be_in_slot5(Band) is false
% We map the correct answer to option/1 based on this.

% Option A: Uneasy cannot be in slot 5
option(a) :- band(uneasy), not can_be_in_slot5(uneasy).

% Option B: Vegemite cannot be in slot 5
option(b) :- band(vegemite), not can_be_in_slot5(vegemite).

% Option C: Wellspring cannot be in slot 5
option(c) :- band(wellspring), not can_be_in_slot5(wellspring).

% Option D: Xpert cannot be in slot 5
option(d) :- band(xpert), not can_be_in_slot5(xpert).

% Option E: Zircon cannot be in slot 5
option(e) :- band(zircon), not can_be_in_slot5(zircon).

% Ensure only one option is selected
:- option(X), option(Y), X != Y.

#show option/1.