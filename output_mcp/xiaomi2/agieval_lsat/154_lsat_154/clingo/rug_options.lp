% Colors
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).

% Rugs
rug(1). rug(2). rug(3).

% Each color is used in at most one rug.
{ used(R, C) : rug(R) } 1 :- color(C).

% Each rug uses at least one color.
1 { used(R, C) : color(C) } :- rug(R).

% Exactly five colors are used.
used_color(C) :- used(_, C).
:- #count{ C : used_color(C) } != 5.

% Solid rug definition: exactly one color
num_colors(R, N) :- rug(R), N = #count{ C : used(R, C) }.
solid(R) :- num_colors(R, 1).

% Condition: one rug is solid yellow.
some_solid_yellow :- rug(R), solid(R), used(R, yellow).
:- not some_solid_yellow.

% Rules:
% 1. White rule: if white used in R, then at least 3 colors in R.
:- used(R, white), num_colors(R, N), N < 3.

% 2. Olive implies peach in same rug.
:- used(R, olive), not used(R, peach).

% 3. Forest and turquoise not together.
:- used(R, forest), used(R, turquoise).

% 4. Peach and turquoise not together.
:- used(R, peach), used(R, turquoise).

% 5. Peach and yellow not together.
:- used(R, peach), used(R, yellow).

% ===== Check each option =====

% A: There is exactly one solid color rug.
exactly_one_solid :- #count{ R : solid(R) } = 1.

% B: One of the rugs is solid forest.
solid_forest :- rug(R), solid(R), used(R, forest).

% C: Turquoise is not used in any of the rugs.
no_turquoise :- not used_color(turquoise).

% D: Forest and olive are used together in a rug.
forest_olive_together :- rug(R), used(R, forest), used(R, olive).

% E: Peach and white are used together in a rug.
peach_white_together :- rug(R), used(R, peach), used(R, white).

#show exactly_one_solid.
#show solid_forest.
#show no_turquoise.
#show forest_olive_together.
#show peach_white_together.