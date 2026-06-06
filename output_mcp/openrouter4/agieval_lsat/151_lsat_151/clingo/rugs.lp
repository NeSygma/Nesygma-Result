% Domain
rug(1..3).
color(forest; olive; peach; turquoise; white; yellow).

% Choice: each color used in at most one rug
{ used(R, C) : rug(R) } 1 :- color(C).

% Exactly 5 of 6 colors are used
:- #count { C : used(_, C) } != 5.

% Each rug must have at least one color (rug exists even if solid)
% No need to enforce; a rug with no colors would be unused, which is fine? Actually each rug is woven, so each rug must have at least one color.
:- rug(R), #count { C : used(R, C) } = 0.

% Given: one of the rugs is solid peach
solid_peach_rug(R) :- used(R, peach), #count { C : used(R, C) } = 1.
:- #count { R : solid_peach_rug(R) } != 1.

% Rule 1: In any rug in which white is used, two other colors are also used.
% i.e., white rug must have at least 3 colors total.
:- used(R, white), #count { C : used(R, C), C != white } < 2.

% Rule 2: In any rug in which olive is used, peach is also used.
:- used(R, olive), not used(R, peach).

% Rule 3: Forest and turquoise are not used together in a rug.
:- used(R, forest), used(R, turquoise).

% Rule 4: Peach and turquoise are not used together in a rug.
:- used(R, peach), used(R, turquoise).

% Rule 5: Peach and yellow are not used together in a rug.
:- used(R, peach), used(R, yellow).

% --- Derive which option must be true ---

% Option A: One of the rugs is solid forest.
solid_forest_rug(R) :- used(R, forest), #count { C : used(R, C) } = 1.

% Option B: One of the rugs is solid turquoise.
solid_turquoise_rug(R) :- used(R, turquoise), #count { C : used(R, C) } = 1.

% Option C: One of the rugs is solid yellow.
solid_yellow_rug(R) :- used(R, yellow), #count { C : used(R, C) } = 1.

% Option D: Forest and white are used together in a rug.
forest_white_together :- used(R, forest), used(R, white).

% Option E: White and yellow are used together in a rug.
white_yellow_together :- used(R, white), used(R, yellow).

% Map options (we'll output all that hold in this model; we need to see which holds in ALL models)
option(a) :- solid_forest_rug(R).
option(b) :- solid_turquoise_rug(R).
option(c) :- solid_yellow_rug(R).
option(d) :- forest_white_together.
option(e) :- white_yellow_together.

#show option/1.
#show used/2.