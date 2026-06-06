%%% Problem Setup %%%

% Six colors available
color(forest; olive; peach; turquoise; white; yellow).

% Exactly five of the six colors will be used
{ used(C) } :- color(C).
:- not #count { C : used(C) } = 5.

% Three rugs: rug1, rug2, rug3
rug(1..3).

% Each used color is assigned to exactly one rug
{ assigned(C, R) : rug(R) } 1 :- used(C).
% A color not used is not assigned to any rug
:- assigned(C, _), not used(C).

% Each rug gets at least one color
:- rug(R), #count { C : assigned(C, R) } = 0.

% A rug is solid if it has exactly one color
solid(R) :- rug(R), #count { C : assigned(C, R) } = 1.

%%% Constraints from rules %%%

% Rule 1: In any rug in which white is used, two other colors are also used.
:- assigned(white, R), #count { C : assigned(C, R) } < 3.

% Rule 2: In any rug in which olive is used, peach is also used.
:- assigned(olive, R), not assigned(peach, R).

% Rule 3: Forest and turquoise are not used together in a rug.
:- assigned(forest, R), assigned(turquoise, R).

% Rule 4: Peach and turquoise are not used together in a rug.
:- assigned(peach, R), assigned(turquoise, R).

% Rule 5: Peach and yellow are not used together in a rug.
:- assigned(peach, R), assigned(yellow, R).

%%% Given condition: One of the rugs is solid yellow %%%
given_solid_yellow :- solid(R), assigned(yellow, R).
:- not given_solid_yellow.

%%% Evaluate each option %%%

% Option A: exactly one solid rug
exactly_one_solid :- #count { R : solid(R) } = 1.

% Option B: one rug is solid forest
solid_forest_rug :- solid(R), assigned(forest, R).

% Option C: turquoise is not used in any rug
turquoise_not_used :- not used(turquoise).

% Option D: forest and olive are used together in a rug
forest_olive_together :- assigned(forest, R), assigned(olive, R).

% Option E: peach and white are used together in a rug
peach_white_together :- assigned(peach, R), assigned(white, R).

#show assigned/2.
#show solid/1.
#show used/1.
#show exactly_one_solid/0.
#show solid_forest_rug/0.
#show turquoise_not_used/0.
#show forest_olive_together/0.
#show peach_white_together/0.