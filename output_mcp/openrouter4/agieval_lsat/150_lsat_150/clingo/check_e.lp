color(forest;olive;peach;turquoise;white;yellow).
rug(1..3).

% Which colors are used (exactly 5)
{ used(C) } :- color(C).
:- not 5 { used(C) } 5.

% Assign each used color to exactly one rug
1 { assign(C,R) : rug(R) } 1 :- used(C).

% Each rug has at least one color
:- rug(R), #count{C : assign(C,R)} = 0.

% Constraints
:- assign(white,R), #count{C : assign(C,R), C != white} < 2.
:- assign(olive,R), not assign(peach,R).
:- assign(forest,R), assign(turquoise,R).
:- assign(peach,R), assign(turquoise,R).
:- assign(peach,R), assign(yellow,R).

% Force yellow to NOT be used
:- used(yellow).

#show assign/2.
#show used/1.