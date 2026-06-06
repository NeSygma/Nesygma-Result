% Colors
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).

% Rugs
rug(1). rug(2). rug(3).

% Exactly 5 colors are used (one is unused)
used(C) :- color(C), not unused(C).
unused(C) :- color(C), not used(C).
1 { unused(C) : color(C) } 1.  % Exactly one color is unused

% Each used color appears in exactly one rug
1 { in_rug(C, R) : rug(R) } 1 :- used(C).

% Rule 1: If white is used in a rug, that rug must have exactly 3 colors total
:- in_rug(white, R), #count{C : in_rug(C, R)} != 3.

% Rule 2: If olive is used in a rug, peach must also be used in that same rug
:- in_rug(olive, R), not in_rug(peach, R).

% Rule 3: Forest and turquoise cannot be together in a rug
:- in_rug(forest, R), in_rug(turquoise, R).

% Rule 4: Peach and turquoise cannot be together in a rug
:- in_rug(peach, R), in_rug(turquoise, R).

% Rule 5: Peach and yellow cannot be together in a rug
:- in_rug(peach, R), in_rug(yellow, R).

% --- Evaluate each answer choice ---

% Option A: forest only; turquoise only; olive, peach, and white
% This means: Rug1: forest, Rug2: turquoise, Rug3: olive+peach+white
option_a :-
    in_rug(forest, 1), #count{C : in_rug(C, 1)} = 1,
    in_rug(turquoise, 2), #count{C : in_rug(C, 2)} = 1,
    in_rug(olive, 3), in_rug(peach, 3), in_rug(white, 3), #count{C : in_rug(C, 3)} = 3,
    used(forest), used(turquoise), used(olive), used(peach), used(white),
    not used(yellow).

% Option B: forest only; turquoise only; olive, peach, and yellow
% This means: Rug1: forest, Rug2: turquoise, Rug3: olive+peach+yellow
option_b :-
    in_rug(forest, 1), #count{C : in_rug(C, 1)} = 1,
    in_rug(turquoise, 2), #count{C : in_rug(C, 2)} = 1,
    in_rug(olive, 3), in_rug(peach, 3), in_rug(yellow, 3), #count{C : in_rug(C, 3)} = 3,
    used(forest), used(turquoise), used(olive), used(peach), used(yellow),
    not used(white).

% Option C: peach only; turquoise only; forest, olive, and white
% This means: Rug1: peach, Rug2: turquoise, Rug3: forest+olive+white
option_c :-
    in_rug(peach, 1), #count{C : in_rug(C, 1)} = 1,
    in_rug(turquoise, 2), #count{C : in_rug(C, 2)} = 1,
    in_rug(forest, 3), in_rug(olive, 3), in_rug(white, 3), #count{C : in_rug(C, 3)} = 3,
    used(peach), used(turquoise), used(forest), used(olive), used(white),
    not used(yellow).

% Option D: yellow only; forest and turquoise; olive and peach
% This means: Rug1: yellow, Rug2: forest+turquoise, Rug3: olive+peach
option_d :-
    in_rug(yellow, 1), #count{C : in_rug(C, 1)} = 1,
    in_rug(forest, 2), in_rug(turquoise, 2), #count{C : in_rug(C, 2)} = 2,
    in_rug(olive, 3), in_rug(peach, 3), #count{C : in_rug(C, 3)} = 2,
    used(yellow), used(forest), used(turquoise), used(olive), used(peach),
    not used(white).

% Option E: yellow only; olive and peach; turquoise and white
% This means: Rug1: yellow, Rug2: olive+peach, Rug3: turquoise+white
option_e :-
    in_rug(yellow, 1), #count{C : in_rug(C, 1)} = 1,
    in_rug(olive, 2), in_rug(peach, 2), #count{C : in_rug(C, 2)} = 2,
    in_rug(turquoise, 3), in_rug(white, 3), #count{C : in_rug(C, 3)} = 2,
    used(yellow), used(olive), used(peach), used(turquoise), used(white),
    not used(forest).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.