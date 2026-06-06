% Define the colors and rugs
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).
rug(1..3).

% Allow colors to be used in rugs (choice rule)
{ used_in(C, R) : color(C), rug(R) }.

% Exactly 5 colors are used
:- not #count { C, R : used_in(C, R) } = 5.

% A rug is solid if it has exactly one color
solid(R) :- rug(R), #count { C : used_in(C, R) } = 1.

% A rug is multicolored if it has more than one color
multicolored(R) :- rug(R), #count { C : used_in(C, R) } > 1.

% Rule: In any rug in which white is used, two other colors are also used (so total 3 colors)
:- used_in(white, R), #count { C : used_in(C, R) } != 3.

% Rule: In any rug in which olive is used, peach is also used
:- used_in(olive, R), not used_in(peach, R).

% Rule: Forest and turquoise are not used together in a rug
:- used_in(forest, R), used_in(turquoise, R).

% Rule: Peach and turquoise are not used together in a rug
:- used_in(peach, R), used_in(turquoise, R).

% Rule: Peach and yellow are not used together in a rug
:- used_in(peach, R), used_in(yellow, R).

% Specific condition: One of the rugs is solid peach
% This means peach is used in exactly one rug, and that rug has only peach
1 { used_in(peach, R) : rug(R) } 1.

% The solid peach rug must be solid and contain only peach
:- used_in(peach, R), #count { C : used_in(C, R) } > 1.

% Map the answer choices to conditions
% (A) One of the rugs is solid forest
option(a) :- solid(R), used_in(forest, R).

% (B) One of the rugs is solid turquoise
option(b) :- solid(R), used_in(turquoise, R).

% (C) One of the rugs is solid yellow
option(c) :- solid(R), used_in(yellow, R).

% (D) Forest and white are used together in a rug
option(d) :- used_in(forest, R), used_in(white, R).

% (E) White and yellow are used together in a rug
option(e) :- used_in(white, R), used_in(yellow, R).

% Show the answer
#show option/1.