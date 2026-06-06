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

% Define multicolored rug: a rug with at least 2 colors
multicolored(R) :- rug(R), #count{C : assign(C,R)} >= 2.

% Negation atoms for each option
neg_a :- multicolored(R), assign(forest,R).
neg_b :- multicolored(R), assign(turquoise,R).
neg_c :- not used(peach).
neg_d :- not used(turquoise).
neg_e :- not used(yellow).

% Option labels
option_labels(a;b;c;d;e).

% Choose one option to test its negation
1 { test_neg(X) : option_labels(X) } 1.

% Enforce the negation condition for the tested option
:- test_neg(a), not neg_a.
:- test_neg(b), not neg_b.
:- test_neg(c), not neg_c.
:- test_neg(d), not neg_d.
:- test_neg(e), not neg_e.

% Output which test_neg is possible
#show test_neg/1.