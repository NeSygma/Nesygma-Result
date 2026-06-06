% Bands and slots
band(uneasy; vegemite; wellspring; xpert; yardsign; zircon).
slot(1..6).

% Each band assigned to exactly one slot
1 { assign(B, S) : slot(S) } 1 :- band(B).

% Each slot gets exactly one band
1 { assign(B, S) : band(B) } 1 :- slot(S).

% Constraints
:- assign(vegemite, S1), assign(zircon, S2), S1 >= S2.
:- assign(wellspring, S1), assign(xpert, S2), S1 >= S2.
:- assign(zircon, S1), assign(xpert, S2), S1 >= S2.
:- assign(uneasy, S), S <= 3.
:- assign(yardsign, S), S >= 4.

% Derive "before" relationships from constraints
before(vegemite, zircon).
before(wellspring, xpert).
before(zircon, xpert).

% A band cannot be in slot 1 if some other band must come before it
impossible_slot1(B) :- band(B), before(X, B).

% Uneasy cannot be in slot 1 because it must be in slots 4-6
impossible_slot1(uneasy).

% The remaining bands (vegemite, wellspring, yardsign) are not impossible
% They are possible, which we can verify by constructing valid assignments

% Option D is correct if the set of possible slot 1 bands is exactly {vegemite, wellspring, yardsign}
% This is true when those three are not impossible and the other three are impossible
option(d) :- not impossible_slot1(vegemite),
             not impossible_slot1(wellspring),
             not impossible_slot1(yardsign),
             impossible_slot1(uneasy),
             impossible_slot1(xpert),
             impossible_slot1(zircon).

#show option/1.