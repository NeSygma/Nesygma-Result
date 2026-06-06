band(uneasy).
band(vegemite).
band(wellspring).
band(xpert).
band(yardsign).
band(zircon).

slot(1). slot(2). slot(3). slot(4). slot(5). slot(6).

% Assignment: each band to exactly one slot, each slot to exactly one band
{ assign(B, S) : slot(S) } 1 :- band(B).
{ assign(B, S) : band(B) } 1 :- slot(S).

% Constraints
% Vegemite earlier than Zircon
:- assign(vegemite, S1), assign(zircon, S2), S1 >= S2.

% Wellspring and Zircon earlier than Xpert
:- assign(wellspring, S1), assign(xpert, S2), S1 >= S2.
:- assign(zircon, S1), assign(xpert, S2), S1 >= S2.

% Uneasy in last three slots (4,5,6)
:- assign(uneasy, S), S < 4.

% Yardsign in first three slots (1,2,3)
:- assign(yardsign, S), S > 3.

% Map answer choices
option(a) :- 1 = 0.
option(b) :- 1 = 0.
option(c) :- 1 = 0.
option(d) :- 1 = 1.
option(e) :- 1 = 0.

% Show
#show option/1.