% Define rugs and colors
rug(r1; r2; r3).
color(forest; olive; peach; turquoise; white; yellow).

% Assign colors to rugs: each color is used in exactly one rug
1 { used_in(C, R) : rug(R) } 1 :- color(C).

% Enforce the condition: forest and peach are used together in a rug
% If both forest and peach are used, they must be in the same rug
:- used_in(forest, R1), used_in(peach, R2), R1 != R2.

% Count the number of colors in each rug
color_count(R, N) :- N = #count{ C : used_in(C, R) }, rug(R).

% Define solid and multicolored rugs
solid(R) :- color_count(R, 1), rug(R).
multicolored(R) :- color_count(R, N), N > 1, rug(R).

% Constraints:
% 1. If white is used in a rug, two other colors must also be used in that rug
:- used_in(white, R), color_count(R, N), N < 3.

% 2. If olive is used in a rug, peach must also be used in that rug
:- used_in(olive, R), not used_in(peach, R).

% 3. Forest and turquoise cannot be used together in a rug
:- used_in(forest, R), used_in(turquoise, R).

% 4. Peach and turquoise cannot be used together in a rug
:- used_in(peach, R), used_in(turquoise, R).

% 5. Peach and yellow cannot be used together in a rug
:- used_in(peach, R), used_in(yellow, R).

% 6. Exactly 5 colors are used (one color is not used)
exactly_five_colors :- #count{ C : color(C), used_in(C, _) } = 5.
:- not exactly_five_colors.

% Define conditions for each option
% (A) There is exactly one solid rug
exactly_one_solid :- #count{ R : solid(R) } = 1.
option(a) :- exactly_one_solid.

% (B) White is not used in any of the rugs
white_not_used :- not used_in(white, _).
option(b) :- white_not_used.

% (C) Yellow is not used in any of the rugs
yellow_not_used :- not used_in(yellow, _).
option(c) :- yellow_not_used.

% (D) Turquoise and white are used together in a rug
turquoise_and_white_together :- used_in(turquoise, R), used_in(white, R).
option(d) :- turquoise_and_white_together.

% (E) Turquoise and yellow are used together in a rug
turquoise_and_yellow_together :- used_in(turquoise, R), used_in(yellow, R).
option(e) :- turquoise_and_yellow_together.

% Show the answer
#show option/1.