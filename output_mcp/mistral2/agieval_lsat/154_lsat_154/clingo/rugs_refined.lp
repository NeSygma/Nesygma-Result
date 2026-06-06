% Define the colors and rugs
color(forest; olive; peach; turquoise; white; yellow).
rug(r1; r2; r3).

% Exactly five colors are used (one color is not used)
1 { used_color(C) : color(C) } 5.

% Assign colors to rugs
% Each rug can have 1 or more colors assigned to it
1 { assigned_color(R, C) : color(C) } 3 :- rug(R).

% Ensure that exactly five colors are used in total
:- { assigned_color(R, C) : rug(R), color(C) } != 5.

% Each color used is assigned to exactly one rug
:- assigned_color(R1, C), assigned_color(R2, C), R1 != R2, used_color(C).

% Solid rug: exactly one color assigned to it
solid_rug(R) :- rug(R), #count{ C : assigned_color(R, C) } = 1.

% Multicolored rug: two or more colors assigned to it
multicolored_rug(R) :- rug(R), #count{ C : assigned_color(R, C) } >= 2.

% Constraints on color usage in rugs
% 1. In any rug in which white is used, two other colors are also used.
:- assigned_color(R, white), #count{ C : assigned_color(R, C) } < 3.

% 2. In any rug in which olive is used, peach is also used.
:- assigned_color(R, olive), not assigned_color(R, peach).

% 3. Forest and turquoise are not used together in a rug.
:- assigned_color(R, forest), assigned_color(R, turquoise).

% 4. Peach and turquoise are not used together in a rug.
:- assigned_color(R, peach), assigned_color(R, turquoise).

% 5. Peach and yellow are not used together in a rug.
:- assigned_color(R, peach), assigned_color(R, yellow).

% Additional constraint: One of the rugs is solid yellow
% Assign yellow to one rug and ensure it is solid
1 { solid_yellow_rug(R) : rug(R) } 1.
assigned_color(solid_yellow_rug, yellow).
solid_rug(solid_yellow_rug).

% Define the options for the question
% (A) There is exactly one solid color rug.
exactly_one_solid :- #count{ R : solid_rug(R) } = 1.
option(a) :- exactly_one_solid.

% (B) One of the rugs is solid forest.
solid_forest_rug :- solid_rug(R), assigned_color(R, forest).
option(b) :- solid_forest_rug.

% (C) Turquoise is not used in any of the rugs.
turquoise_not_used :- not assigned_color(_, turquoise).
option(c) :- turquoise_not_used.

% (D) Forest and olive are used together in a rug.
forest_and_olive_together :- rug(R), assigned_color(R, forest), assigned_color(R, olive).
option(d) :- forest_and_olive_together.

% (E) Peach and white are used together in a rug.
peach_and_white_together :- rug(R), assigned_color(R, peach), assigned_color(R, white).
option(e) :- peach_and_white_together.

#show option/1.