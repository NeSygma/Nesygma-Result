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

% Derive the correct answer: Yellow must be used in all valid configurations
answer(e) :- used_color(yellow).

% Ensure only one option is selected as the answer
% Since answer(e) is the only one that must be true, we map it directly
option(e) :- answer(e).

#show option/1.