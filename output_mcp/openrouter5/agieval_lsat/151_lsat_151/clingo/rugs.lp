%% Problem: Three rugs, six colors, exactly five used, each used in only one rug.
%% Colors: forest, olive, peach, turquoise, white, yellow
%% Rugs are solid (one color) or multicolored.
%% Rules:
%% 1. If white is used in a rug, two other colors are also used (so rug with white has exactly 3 colors).
%% 2. If olive is used in a rug, peach is also used.
%% 3. Forest and turquoise not together in a rug.
%% 4. Peach and turquoise not together in a rug.
%% 5. Peach and yellow not together in a rug.
%% Given: One rug is solid peach.

%% Domain
color(forest; olive; peach; turquoise; white; yellow).
rug(1..3).

%% Each color is either used or not. Exactly 5 used.
{ used(C) } :- color(C).
:- not #count { C : used(C) } = 5.

%% Each used color is assigned to exactly one rug.
{ assigned(C, R) } :- used(C), rug(R).
:- used(C), not #count { R : assigned(C, R) } = 1.
:- assigned(C, R), not used(C).

%% A rug is solid if exactly one color is assigned to it.
solid(R) :- rug(R), #count { C : assigned(C, R) } = 1.

%% A rug is multicolored if more than one color is assigned to it.
multicolored(R) :- rug(R), #count { C : assigned(C, R) } > 1.

%% Rule 1: If white is used in a rug, exactly two other colors are also used in that rug.
:- assigned(white, R), not #count { C : assigned(C, R), C != white } = 2.

%% Rule 2: If olive is used in a rug, peach is also used in that rug.
:- assigned(olive, R), not assigned(peach, R).

%% Rule 3: Forest and turquoise not together in a rug.
:- assigned(forest, R), assigned(turquoise, R).

%% Rule 4: Peach and turquoise not together in a rug.
:- assigned(peach, R), assigned(turquoise, R).

%% Rule 5: Peach and yellow not together in a rug.
:- assigned(peach, R), assigned(yellow, R).

%% Given: One rug is solid peach.
%% That means there is a rug R such that assigned(peach, R) and solid(R).
%% solid(R) means exactly one color assigned to R, so only peach is assigned to R.
:- not #count { R : assigned(peach, R), solid(R) } >= 1.

%% Now evaluate the options.
%% (A) One of the rugs is solid forest.
option(a) :- #count { R : assigned(forest, R), solid(R) } >= 1.

%% (B) One of the rugs is solid turquoise.
option(b) :- #count { R : assigned(turquoise, R), solid(R) } >= 1.

%% (C) One of the rugs is solid yellow.
option(c) :- #count { R : assigned(yellow, R), solid(R) } >= 1.

%% (D) Forest and white are used together in a rug.
option(d) :- rug(R), assigned(forest, R), assigned(white, R).

%% (E) White and yellow are used together in a rug.
option(e) :- rug(R), assigned(white, R), assigned(yellow, R).

#show option/1.
#show assigned/2.
#show solid/1.