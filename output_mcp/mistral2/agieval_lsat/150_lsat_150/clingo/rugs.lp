% Define the colors and rugs
color(forest; olive; peach; turquoise; white; yellow).
rug(1..3).

% Each color used is in exactly one rug
1 { assigned_color(R, C) : rug(R) } 1 :- color(C).

% Exactly five colors are used (one color is not used)
used_color(C) :- color(C), assigned_color(R, C).
unused_color(C) :- color(C), not used_color(C).
:- #count{ C : unused_color(C) } != 1.

% A rug is solid if it uses exactly one color, multicolored otherwise
solid(R) :- rug(R), #count{ C : assigned_color(R, C) } = 1.
multicolored(R) :- rug(R), #count{ C : assigned_color(R, C) } > 1.

% Rules:
% 1. In any rug in which white is used, two other colors are also used (total 3 colors).
:- assigned_color(R, white), #count{ C : assigned_color(R, C) } != 3.

% 2. In any rug in which olive is used, peach is also used.
:- assigned_color(R, olive), not assigned_color(R, peach).

% 3. Forest and turquoise are not used together in a rug.
:- assigned_color(R, forest), assigned_color(R, turquoise).

% 4. Peach and turquoise are not used together in a rug.
:- assigned_color(R, peach), assigned_color(R, turquoise).

% 5. Peach and yellow are not used together in a rug.
:- assigned_color(R, peach), assigned_color(R, yellow).

% --- Multiple Choice Answer Mapping ---
% (A) There are no multicolored rugs in which forest is used.
% This means: If forest is used in a rug, that rug is not multicolored.
option(a) :- not forest_in_multicolored.
forest_in_multicolored :- assigned_color(R, forest), multicolored(R).

% (B) There are no multicolored rugs in which turquoise is used.
% This means: If turquoise is used in a rug, that rug is not multicolored.
option(b) :- not turquoise_in_multicolored.
turquoise_in_multicolored :- assigned_color(R, turquoise), multicolored(R).

% (C) Peach is used in one of the rugs.
option(c) :- used_color(peach).

% (D) Turquoise is used in one of the rugs.
option(d) :- used_color(turquoise).

% (E) Yellow is used in one of the rugs.
option(e) :- used_color(yellow).

#show option/1.