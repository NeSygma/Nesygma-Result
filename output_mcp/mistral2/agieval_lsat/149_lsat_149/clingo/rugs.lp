% Define colors and rugs
color(forest; olive; peach; turquoise; white; yellow).
rug(rug1; rug2; rug3).

% Exactly one color is unused
1 { unused_color(C) : color(C) } 1.

% Each color is used in exactly one rug
1 { color_in_rug(R, C) : rug(R) } 1 :- color(C), not unused_color(C).

% Rugs are either solid or multicolored (exclusive)
solid(R) :- rug(R), 1 = { color_in_rug(R, _) }.
multicolored(R) :- rug(R), 1 < { color_in_rug(R, _) }.
:- rug(R), solid(R), multicolored(R).

% If white is used in a rug, that rug must have exactly 2 other colors (3 total)
:- color_in_rug(R, white), not (2 = #count { C : color_in_rug(R, C), C != white }).

% If olive is used in a rug, peach must also be used in that rug
:- color_in_rug(R, olive), not color_in_rug(R, peach).

% Forest and turquoise cannot be used together in a rug
:- color_in_rug(R, forest), color_in_rug(R, turquoise).

% Peach and turquoise cannot be used together in a rug
:- color_in_rug(R, peach), color_in_rug(R, turquoise).

% Peach and yellow cannot be used together in a rug
:- color_in_rug(R, peach), color_in_rug(R, yellow).

% --- Map the correct answer to option/1 ---
% Option A: forest only; turquoise only; olive, peach, and white
option(a) :-
    unused_color(yellow),
    color_in_rug(rug1, forest), solid(rug1),
    color_in_rug(rug2, turquoise), solid(rug2),
    color_in_rug(rug3, olive),
    color_in_rug(rug3, peach),
    color_in_rug(rug3, white),
    multicolored(rug3).

% Option B: forest only; turquoise only; olive, peach, and yellow
option(b) :-
    unused_color(white),
    color_in_rug(rug1, forest), solid(rug1),
    color_in_rug(rug2, turquoise), solid(rug2),
    color_in_rug(rug3, olive),
    color_in_rug(rug3, peach),
    color_in_rug(rug3, yellow),
    multicolored(rug3).

% Option C: peach only; turquoise only; forest, olive, and white
option(c) :-
    unused_color(yellow),
    color_in_rug(rug1, peach), solid(rug1),
    color_in_rug(rug2, turquoise), solid(rug2),
    color_in_rug(rug3, forest),
    color_in_rug(rug3, olive),
    color_in_rug(rug3, white),
    multicolored(rug3).

% Option D: yellow only; forest and turquoise; olive and peach
option(d) :-
    unused_color(white),
    color_in_rug(rug1, yellow), solid(rug1),
    color_in_rug(rug2, forest),
    color_in_rug(rug2, turquoise),
    multicolored(rug2),
    color_in_rug(rug3, olive),
    color_in_rug(rug3, peach),
    multicolored(rug3).

% Option E: yellow only; olive and peach; turquoise and white
option(e) :-
    unused_color(forest),
    color_in_rug(rug1, yellow), solid(rug1),
    color_in_rug(rug2, olive),
    color_in_rug(rug2, peach),
    multicolored(rug2),
    color_in_rug(rug3, turquoise),
    color_in_rug(rug3, white),
    multicolored(rug3).

% Show the answer
#show option/1.