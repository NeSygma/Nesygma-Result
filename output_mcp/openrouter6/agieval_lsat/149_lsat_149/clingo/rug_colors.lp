% Colors
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).

% Rugs
rug(rug1). rug(rug2). rug(rug3).

% Color usage: color_used_in(C, R) means color C is used in rug R.
% We will define this per scenario.

% Scenario selection
{ scenario(a); scenario(b); scenario(c); scenario(d); scenario(e) } 1.

% Option A: forest only; turquoise only; olive, peach, white
color_used_in(forest, rug1) :- scenario(a).
color_used_in(turquoise, rug2) :- scenario(a).
color_used_in(olive, rug3) :- scenario(a).
color_used_in(peach, rug3) :- scenario(a).
color_used_in(white, rug3) :- scenario(a).

% Option B: forest only; turquoise only; olive, peach, yellow
color_used_in(forest, rug1) :- scenario(b).
color_used_in(turquoise, rug2) :- scenario(b).
color_used_in(olive, rug3) :- scenario(b).
color_used_in(peach, rug3) :- scenario(b).
color_used_in(yellow, rug3) :- scenario(b).

% Option C: peach only; turquoise only; forest, olive, white
color_used_in(peach, rug1) :- scenario(c).
color_used_in(turquoise, rug2) :- scenario(c).
color_used_in(forest, rug3) :- scenario(c).
color_used_in(olive, rug3) :- scenario(c).
color_used_in(white, rug3) :- scenario(c).

% Option D: yellow only; forest and turquoise; olive and peach
color_used_in(yellow, rug1) :- scenario(d).
color_used_in(forest, rug2) :- scenario(d).
color_used_in(turquoise, rug2) :- scenario(d).
color_used_in(olive, rug3) :- scenario(d).
color_used_in(peach, rug3) :- scenario(d).

% Option E: yellow only; olive and peach; turquoise and white
color_used_in(yellow, rug1) :- scenario(e).
color_used_in(olive, rug2) :- scenario(e).
color_used_in(peach, rug2) :- scenario(e).
color_used_in(turquoise, rug3) :- scenario(e).
color_used_in(white, rug3) :- scenario(e).

% Derived: a color is used if it appears in any rug
used(C) :- color_used_in(C, _).

% Constraint: each color used appears in exactly one rug
:- color_used_in(C, R1), color_used_in(C, R2), R1 != R2.

% Constraint: exactly five colors are used
:- #count{C : used(C)} != 5.

% Rule 1: If white in a rug, then that rug has exactly three colors
:- color_used_in(white, R), #count{C : color_used_in(C, R)} != 3.

% Rule 2: If olive in a rug, then peach in that rug
:- color_used_in(olive, R), not color_used_in(peach, R).

% Rule 3: Forest and turquoise not together
:- color_used_in(forest, R), color_used_in(turquoise, R).

% Rule 4: Peach and turquoise not together
:- color_used_in(peach, R), color_used_in(turquoise, R).

% Rule 5: Peach and yellow not together
:- color_used_in(peach, R), color_used_in(yellow, R).

% Derive the correct option based on the selected scenario
option(a) :- scenario(a).
option(b) :- scenario(b).
option(c) :- scenario(c).
option(d) :- scenario(d).
option(e) :- scenario(e).

#show option/1.