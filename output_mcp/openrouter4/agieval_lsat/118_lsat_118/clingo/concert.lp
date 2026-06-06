% Bands and slots
band(uneasy; vegemite; wellspring; xpert; yardsign; zircon).
slot(1..6).

% Each band gets exactly one slot
1 { assign(B, S) : slot(S) } 1 :- band(B).

% Each slot gets exactly one band
1 { assign(B, S) : band(B) } 1 :- slot(S).

% --- Constraints ---
% Vegemite earlier than Zircon
:- assign(vegemite, S1), assign(zircon, S2), S1 >= S2.

% Wellspring earlier than Xpert
:- assign(wellspring, S1), assign(xpert, S2), S1 >= S2.

% Zircon earlier than Xpert
:- assign(zircon, S1), assign(xpert, S2), S1 >= S2.

% Uneasy in last three slots (4,5,6)
:- assign(uneasy, S), S < 4.

% Yardsign in first three slots (1,2,3)
:- assign(yardsign, S), S > 3.

% Given condition: Vegemite in slot 3
assign(vegemite, 3).

% --- Show all assignments ---
#show assign/2.

% --- Define each option's truth condition ---
% (A) Uneasy earlier than Xpert
option_holds(a) :- assign(uneasy, S1), assign(xpert, S2), S1 < S2.
% (B) Wellspring earlier than Zircon
option_holds(b) :- assign(wellspring, S1), assign(zircon, S2), S1 < S2.
% (C) Xpert earlier than Uneasy
option_holds(c) :- assign(xpert, S1), assign(uneasy, S2), S1 < S2.
% (D) Yardsign earlier than Wellspring
option_holds(d) :- assign(yardsign, S1), assign(wellspring, S2), S1 < S2.
% (E) Zircon earlier than Uneasy
option_holds(e) :- assign(zircon, S1), assign(uneasy, S2), S1 < S2.

#show option_holds/1.