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

% Find the minimum slot for Wellspring
% We use a minimization statement to find the smallest possible slot for Wellspring
#minimize { Slot : assignment(wellspring, Slot) }.

% Derive the answer slot for Wellspring
answer_slot(S) :- assignment(wellspring, S), S = #min{ T : assignment(wellspring, T) }.

% Map the answer slot to the answer choices
option(a) :- answer_slot(2).
option(b) :- answer_slot(3).
option(c) :- answer_slot(4).
option(d) :- answer_slot(5).
option(e) :- answer_slot(6).

#show option/1.