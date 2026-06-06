% Colors
color(forest; olive; peach; turquoise; white; yellow).

% We have 3 rugs
rug(1..3).

% Choices
choice(a; b; c; d; e).

% For each choice, define the two solid colors
solid_color(a, forest).
solid_color(a, peach).

solid_color(b, forest).
solid_color(b, yellow).

solid_color(c, peach).
solid_color(c, turquoise).

solid_color(d, peach).
solid_color(d, yellow).

solid_color(e, turquoise).
solid_color(e, yellow).

% For each choice, the remaining colors are the 6 colors minus the two solid colors
remaining_color(Ch, C) :- choice(Ch), color(C), not solid_color(Ch, C).

% For each choice, we pick exactly 3 of the remaining colors for the multicolored rug
% (since exactly 5 colors used total, 2 are solid, so 3 go to multicolored)
{ multi_color(Ch, C) : remaining_color(Ch, C) } = 3 :- choice(Ch).

% Now check constraints for each choice:

% Rule 1: If white is used in a rug, two other colors are also used.
% White cannot be a solid color (solid rug has only 1 color)
:- solid_color(Ch, white).

% If white is in the multicolored rug, it has 3 colors total, so fine automatically.

% Rule 2: If olive is in a rug, peach is also in that rug.
% Olive cannot be a solid color
:- solid_color(Ch, olive).

% For multicolored rug:
:- choice(Ch), multi_color(Ch, olive), not multi_color(Ch, peach).

% Rule 3: Forest and turquoise not together in a rug.
:- choice(Ch), multi_color(Ch, forest), multi_color(Ch, turquoise).

% Rule 4: Peach and turquoise not together in a rug.
:- choice(Ch), multi_color(Ch, peach), multi_color(Ch, turquoise).

% Rule 5: Peach and yellow not together in a rug.
:- choice(Ch), multi_color(Ch, peach), multi_color(Ch, yellow).

% A choice is possible if there exists a valid selection of multi_colors
possible(Ch) :- choice(Ch), multi_color(Ch, _).

% Which choices are NOT possible?
impossible(Ch) :- choice(Ch), not possible(Ch).

% Map to answer
option(a) :- impossible(a).
option(b) :- impossible(b).
option(c) :- impossible(c).
option(d) :- impossible(d).
option(e) :- impossible(e).

% We need exactly one option
:- #count{ Ch : option(Ch) } != 1.

#show option/1.