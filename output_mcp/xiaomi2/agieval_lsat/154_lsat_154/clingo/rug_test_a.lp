% Colors
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).

% Rugs
rug(1). rug(2). rug(3).

% Each color is used in at most one rug.
{ used(R, C) : rug(R) } 1 :- color(C).

% Each rug uses at least one color.
1 { used(R, C) : color(C) } :- rug(R).

% Exactly five colors are used.
used_color(C) :- used(R, C).
:- #count{ C : used_color(C) } != 5.

% Solid rug definition
solid(R) :- used(R, C), #count{ C2 : used(R, C2) } = 1.

% Condition: one rug is solid yellow.
:- not some_solid_yellow.
some_solid_yellow :- rug(R), solid(R), used(R, yellow).

% Rules:
% 1. White rule: if white used in R, then at least 3 colors in R.
:- used(R, white), #count{ C : used(R, C) } < 3.

% 2. Olive implies peach in same rug.
:- used(R, olive), not used(R, peach).

% 3. Forest and turquoise not together.
:- used(R, forest), used(R, turquoise).

% 4. Peach and turquoise not together.
:- used(R, peach), used(R, turquoise).

% 5. Peach and yellow not together.
:- used(R, peach), used(R, yellow).

% Test Option A: exactly one solid rug
holds_a :- #count{ R : solid(R) } = 1.
:- not holds_a.

#show used/2.
#show solid/1.
#show holds_a/0.