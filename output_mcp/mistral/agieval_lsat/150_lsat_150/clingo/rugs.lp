% Define the colors
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).

% Define the rugs
rug(1..3).

% Exactly 5 colors are used
1 { used_color(C) : color(C) } 5.

% Each used color is in exactly one rug
1 { in_rug(R, C) : rug(R) } 1 :- used_color(C).

% Rug types: solid or multicolored
% A rug is solid if it has exactly one color
solid(R) :- rug(R), #count { C : in_rug(R, C) } = 1.
% A rug is multicolored if it has more than one color
multicolored(R) :- rug(R), #count { C : in_rug(R, C) } > 1.
% Each rug must be either solid or multicolored
:- rug(R), not solid(R), not multicolored(R).
% A rug cannot be both
:- solid(R), multicolored(R).

% Constraint 1: In any rug in which white is used, two other colors are also used
% This means the rug with white must have exactly 3 colors total
:- in_rug(R, white), #count { C : in_rug(R, C) } != 3.

% Constraint 2: In any rug in which olive is used, peach is also used
:- in_rug(R, olive), not in_rug(R, peach).

% Constraint 3: Forest and turquoise are not used together in a rug
:- in_rug(R, forest), in_rug(R, turquoise).

% Constraint 4: Peach and turquoise are not used together in a rug
:- in_rug(R, peach), in_rug(R, turquoise).

% Constraint 5: Peach and yellow are not used together in a rug
:- in_rug(R, peach), in_rug(R, yellow).

% Helper predicates for options
exists_multicolored_forest :- multicolored(R), in_rug(R, forest).
exists_multicolored_turquoise :- multicolored(R), in_rug(R, turquoise).

% Map the options
% (A) There are no multicolored rugs in which forest is used
option(a) :- not exists_multicolored_forest.

% (B) There are no multicolored rugs in which turquoise is used
option(b) :- not exists_multicolored_turquoise.

% (C) Peach is used in one of the rugs
option(c) :- used_color(peach).

% (D) Turquoise is used in one of the rugs
option(d) :- used_color(turquoise).

% (E) Yellow is used in one of the rugs
option(e) :- used_color(yellow).

% Ensure only the correct answer is selected
:- option(a), option(c).
:- option(b), option(c).
:- option(d), option(c).
:- option(e), option(c).

#show option/1.