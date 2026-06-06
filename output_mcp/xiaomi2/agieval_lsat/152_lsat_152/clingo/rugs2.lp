% Domain
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).
rug(1). rug(2). rug(3).

% Exactly 5 of 6 colors are used
{ used(C) : color(C) } 5.

% Each used color assigned to exactly one rug
{ assigned(C, R) : rug(R) } 1 :- used(C).
:- assigned(C, R), not used(C).

% Each rug has at least one color
:- rug(R), #count{C : assigned(C, R)} = 0.

% Exactly 2 solid rugs (1 color each), 1 multicolored rug (3 colors)
solid(R) :- rug(R), #count{C : assigned(C, R)} = 1.
multicolored(R) :- rug(R), #count{C : assigned(C, R)} > 1.
:- #count{R : solid(R)} != 2.
:- #count{R : multicolored(R)} != 1.

% Rule 1: If white is used in a rug, two other colors also used (3 total)
:- assigned(white, R), #count{C : assigned(C, R)} != 3.

% Rule 2: If olive is used in a rug, peach is also used in that rug
:- assigned(olive, R), not assigned(peach, R).

% Rule 3: Forest and turquoise not together
:- assigned(forest, R), assigned(turquoise, R).

% Rule 4: Peach and turquoise not together
:- assigned(peach, R), assigned(turquoise, R).

% Rule 5: Peach and yellow not together
:- assigned(peach, R), assigned(yellow, R).

% Collect solid colors
solid_color(C) :- assigned(C, R), solid(R).

% Show solid color pairs for analysis
solid_pair(C1, C2) :- solid_color(C1), solid_color(C2), C1 < C2.

#show solid_pair/2.