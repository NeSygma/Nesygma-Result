% Define the entities
rug(r1; r2; r3).
color(forest; olive; peach; turquoise; white; yellow).

% Exactly 5 colors are used (one unused)
1 { used(C) : color(C) } 5.
unused(C) :- color(C), not used(C).

% Each color is used in exactly one rug
1 { assigned_color(R, C) : color(C) } 1 :- used(C).

% Rug types: solid or multicolored
solid(R) :- assigned_color(R, _), not multicolored(R).
multicolored(R) :- assigned_color(R, _), #count { C : assigned_color(R, C) } > 1.

% Constraints on color usage
% 1. White must be in a multicolored rug with exactly 3 colors (including white)
:- used(white), solid(R), assigned_color(R, white).
:- used(white), multicolored(R), assigned_color(R, white), #count { C : assigned_color(R, C) } != 3.

% 2. If olive is used, peach must also be used in the same rug
:- used(olive), assigned_color(R, olive), not assigned_color(R, peach).

% 3. Forest and turquoise not together in the same rug
:- assigned_color(R, forest), assigned_color(R, turquoise).

% 4. Peach and turquoise not together in the same rug
:- assigned_color(R, peach), assigned_color(R, turquoise).

% 5. Peach and yellow not together in a rug
:- assigned_color(R, peach), assigned_color(R, yellow).

% The given condition: one rug is solid yellow
:- not 1 { R : solid(R), assigned_color(R, yellow) } 1.

% Define the answer choices as possibilities
% A) There is exactly one solid color rug
exactly_one_solid :- #count { R : solid(R) } = 1.

% B) One of the rugs is solid forest
solid_forest :- solid(R), assigned_color(R, forest).

% C) Turquoise is not used in any of the rugs
no_turquoise :- not used(turquoise).

% D) Forest and olive are used together in a rug
forest_and_olive_together :- assigned_color(R, forest), assigned_color(R, olive).

% E) Peach and white are used together in a rug
peach_and_white_together :- assigned_color(R, peach), assigned_color(R, white).

% Map to options
option(a) :- exactly_one_solid.
option(b) :- solid_forest.
option(c) :- no_turquoise.
option(d) :- forest_and_olive_together.
option(e) :- peach_and_white_together.

#show option/1.