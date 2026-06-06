% Define the available colors
color(forest).
color(olive).
color(peach).
color(turquoise).
color(white).
color(yellow).

% Define the three rugs
rug(1..3).

% A color is either used in exactly one rug or unused
{ used_in(C, R) : rug(R) } 1 :- color(C), not unused(C).
unused(C) :- color(C), not used_in(C, _).

% Exactly 5 colors are used
:- #count { C : color(C), not unused(C) } != 5.

% Constraint: In any rug in which white is used, two other colors are also used
:- used_in(white, R), #count { C : used_in(C, R), C != white } < 2.

% Constraint: In any rug in which olive is used, peach is also used
:- used_in(olive, R), not used_in(peach, R).

% Constraint: Forest and turquoise are not used together in a rug
:- used_in(forest, R), used_in(turquoise, R).

% Constraint: Peach and turquoise are not used together in a rug
:- used_in(peach, R), used_in(turquoise, R).

% Constraint: Peach and yellow are not used together in a rug
:- used_in(peach, R), used_in(yellow, R).

% Helper predicates to define the options

% Option A: forest only; turquoise only; olive, peach, and white
option(a) :-
    used_in(forest, 1), not used_in(olive, 1), not used_in(peach, 1), not used_in(turquoise, 1), not used_in(white, 1), not used_in(yellow, 1),
    used_in(turquoise, 2), not used_in(forest, 2), not used_in(olive, 2), not used_in(peach, 2), not used_in(white, 2), not used_in(yellow, 2),
    used_in(olive, 3), used_in(peach, 3), used_in(white, 3), not used_in(forest, 3), not used_in(turquoise, 3), not used_in(yellow, 3),
    #count { C : used_in(C, 3) } = 3.

% Option B: forest only; turquoise only; olive, peach, and yellow
option(b) :-
    used_in(forest, 1), not used_in(olive, 1), not used_in(peach, 1), not used_in(turquoise, 1), not used_in(white, 1), not used_in(yellow, 1),
    used_in(turquoise, 2), not used_in(forest, 2), not used_in(olive, 2), not used_in(peach, 2), not used_in(white, 2), not used_in(yellow, 2),
    used_in(olive, 3), used_in(peach, 3), used_in(yellow, 3), not used_in(forest, 3), not used_in(turquoise, 3), not used_in(white, 3),
    #count { C : used_in(C, 3) } = 3.

% Option C: peach only; turquoise only; forest, olive, and white
option(c) :-
    used_in(peach, 1), not used_in(forest, 1), not used_in(olive, 1), not used_in(turquoise, 1), not used_in(white, 1), not used_in(yellow, 1),
    used_in(turquoise, 2), not used_in(forest, 2), not used_in(olive, 2), not used_in(peach, 2), not used_in(white, 2), not used_in(yellow, 2),
    used_in(forest, 3), used_in(olive, 3), used_in(white, 3), not used_in(peach, 3), not used_in(turquoise, 3), not used_in(yellow, 3),
    #count { C : used_in(C, 3) } = 3.

% Option D: yellow only; forest and turquoise; olive and peach
option(d) :-
    used_in(yellow, 1), not used_in(forest, 1), not used_in(olive, 1), not used_in(peach, 1), not used_in(turquoise, 1), not used_in(white, 1),
    used_in(forest, 2), used_in(turquoise, 2), not used_in(olive, 2), not used_in(peach, 2), not used_in(white, 2), not used_in(yellow, 2),
    used_in(olive, 3), used_in(peach, 3), not used_in(forest, 3), not used_in(turquoise, 3), not used_in(white, 3), not used_in(yellow, 3),
    #count { C : used_in(C, 2) } = 2, #count { C : used_in(C, 3) } = 2.

% Option E: yellow only; olive and peach; turquoise and white
option(e) :-
    used_in(yellow, 1), not used_in(forest, 1), not used_in(olive, 1), not used_in(peach, 1), not used_in(turquoise, 1), not used_in(white, 1),
    used_in(olive, 2), used_in(peach, 2), not used_in(forest, 2), not used_in(turquoise, 2), not used_in(white, 2), not used_in(yellow, 2),
    used_in(turquoise, 3), used_in(white, 3), not used_in(forest, 3), not used_in(olive, 3), not used_in(peach, 3), not used_in(yellow, 3),
    #count { C : used_in(C, 2) } = 2, #count { C : used_in(C, 3) } = 2.

#show option/1.