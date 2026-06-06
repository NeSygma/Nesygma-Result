% Bands
band(uneasy; vegemite; wellspring; xpert; yardsign; zircon).
slot(1..6).

% Each band assigned to exactly one slot
1 { assign(B, S) : slot(S) } 1 :- band(B).

% Each slot gets exactly one band
1 { assign(B, S) : band(B) } 1 :- slot(S).

% Constraint 1: Vegemite earlier than Zircon
:- assign(vegemite, S1), assign(zircon, S2), S1 >= S2.

% Constraint 2: Wellspring earlier than Xpert
:- assign(wellspring, S1), assign(xpert, S2), S1 >= S2.

% Constraint 3: Zircon earlier than Xpert
:- assign(zircon, S1), assign(xpert, S2), S1 >= S2.

% Constraint 4: Uneasy in last three slots (4,5,6)
:- assign(uneasy, S), S <= 3.

% Constraint 5: Yardsign in first three slots (1,2,3)
:- assign(yardsign, S), S >= 4.

#show assign/2.