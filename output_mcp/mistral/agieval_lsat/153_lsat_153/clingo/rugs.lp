% Define the rugs and colors
rug(1..3).
color(forest; olive; peach; turquoise; white; yellow).

% Exactly 5 colors are used
1 { used(C) : color(C) } 5.

% Each used color appears in exactly one rug
1 { in_rug(C, R) : rug(R) } 1 :- used(C).

% Rugs can be solid or multicolored
{ solid(R) ; multicolored(R) } 1 :- rug(R).

% Solid rugs have exactly one color
1 { in_rug(C, R) : color(C) } 1 :- rug(R), solid(R).

% Multicolored rugs have at least 2 colors
2 { in_rug(C, R) : color(C) } :- rug(R), multicolored(R).

% Rule: If white is used in a rug, that rug must be multicolored with exactly 3 colors (white + 2 others)
:- in_rug(white, R), not multicolored(R).
:- in_rug(white, R), #count { C : in_rug(C, R) } != 3.

% Rule: If olive is used in a rug, peach must also be used in that rug
:- in_rug(olive, R), not in_rug(peach, R).

% Rule: Forest and turquoise are not used together in a rug
:- in_rug(forest, R), in_rug(turquoise, R).

% Rule: Peach and turquoise are not used together in a rug
:- in_rug(peach, R), in_rug(turquoise, R).

% Rule: Peach and yellow are not used together in a rug
:- in_rug(peach, R), in_rug(yellow, R).

% Given condition: forest and peach are used together in a rug
exists_rug_with_forest_and_peach :- in_rug(forest, R), in_rug(peach, R).
:- not exists_rug_with_forest_and_peach.

% Answer choice conditions
% (A) There is exactly one solid rug
exactly_one_solid :- #count { R : solid(R) } = 1.
option(a) :- exactly_one_solid.

% (B) White is not used in any of the rugs
white_not_used :- not used(white).
option(b) :- white_not_used.

% (C) Yellow is not used in any of the rugs
yellow_not_used :- not used(yellow).
option(c) :- yellow_not_used.

% (D) Turquoise and white are used together in a rug
turquoise_and_white_together :- in_rug(turquoise, R), in_rug(white, R).
option(d) :- turquoise_and_white_together.

% (E) Turquoise and yellow are used together in a rug
turquoise_and_yellow_together :- in_rug(turquoise, R), in_rug(yellow, R).
option(e) :- turquoise_and_yellow_together.

#show option/1.