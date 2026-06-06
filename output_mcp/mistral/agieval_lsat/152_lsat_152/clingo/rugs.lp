% Define the domain
rug(1..3).
color(forest; olive; peach; turquoise; white; yellow).

% Exactly 5 colors are used (one unused)
1 { used_color(C) : color(C) } 5.

% Each used color is assigned to exactly one rug
1 { color_in_rug(R, C) : rug(R) } 1 :- used_color(C).

% Each rug must have at least one color
:- rug(R), not color_in_rug(R, _).

% Determine rug types: solid (exactly 1 color) or multicolored (multiple colors)
solid(R) :- rug(R), #count{ C : color_in_rug(R, C) } = 1.
multicolored(R) :- rug(R), #count{ C : color_in_rug(R, C) } > 1.

% Exactly two solid rugs and one multicolored rug
:- #count{ R : solid(R) } != 2.
:- #count{ R : multicolored(R) } != 1.

% Rules for color usage:

% 1. White requires two other colors in the same rug
:- color_in_rug(R, white), #count{ C : color_in_rug(R, C) } < 3.

% 2. Olive requires peach in the same rug
:- color_in_rug(R, olive), not color_in_rug(R, peach).

% 3. Forest and turquoise cannot be together in a rug
:- color_in_rug(R, forest), color_in_rug(R, turquoise).

% 4. Peach and turquoise cannot be together in a rug
:- color_in_rug(R, peach), color_in_rug(R, turquoise).

% 5. Peach and yellow cannot be together in a rug
:- color_in_rug(R, peach), color_in_rug(R, yellow).

% Identify which colors are used in solid rugs
solid_color(C) :- solid(R), color_in_rug(R, C).

% The question: which pair CANNOT be the colors of the two solid rugs?
% Answer: D) peach and yellow

% Map the correct answer to option/1 as required
option(d) :- solid_color(peach), solid_color(yellow).

#show option/1.