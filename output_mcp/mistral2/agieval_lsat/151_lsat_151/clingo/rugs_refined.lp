% Define the colors and rugs
color(forest; olive; peach; turquoise; white; yellow).
rug(rug1; rug2; rug3).

% Exactly five colors are used in total
1 { used_color(C) : color(C) } 5.

% Assign colors to rugs
% A rug can have multiple colors if it is multicolored, or one color if solid
{ assign_color(R, C) : color(C) } :- rug(R).

% Each color used is in only one rug
:- assign_color(R1, C), assign_color(R2, C), R1 != R2, used_color(C).

% Each rug is either solid or multicolored
% Solid: exactly one color
solid(R) :- rug(R), 1 = { assign_color(R, C) : color(C) }.
multicolored(R) :- rug(R), not solid(R).

% In any rug in which white is used, two other colors are also used
:- assign_color(R, white), not 2 = { assign_color(R, C) : color(C), C != white }.

% In any rug in which olive is used, peach is also used
:- assign_color(R, olive), not assign_color(R, peach).

% Forest and turquoise are not used together in a rug
:- assign_color(R, forest), assign_color(R, turquoise).

% Peach and turquoise are not used together in a rug
:- assign_color(R, peach), assign_color(R, turquoise).

% Peach and yellow are not used together in a rug
:- assign_color(R, peach), assign_color(R, yellow).

% Assume one of the rugs is solid peach
:- not 1 = { R : solid(R), assign_color(R, peach) }.

% Define the answer choices as conditions
% (A) One of the rugs is solid forest
option(a) :- solid(rug1), assign_color(rug1, forest).
option(a) :- solid(rug2), assign_color(rug2, forest).
option(a) :- solid(rug3), assign_color(rug3, forest).

% (B) One of the rugs is solid turquoise
option(b) :- solid(rug1), assign_color(rug1, turquoise).
option(b) :- solid(rug2), assign_color(rug2, turquoise).
option(b) :- solid(rug3), assign_color(rug3, turquoise).

% (C) One of the rugs is solid yellow
option(c) :- solid(rug1), assign_color(rug1, yellow).
option(c) :- solid(rug2), assign_color(rug2, yellow).
option(c) :- solid(rug3), assign_color(rug3, yellow).

% (D) Forest and white are used together in a rug
option(d) :- assign_color(R, forest), assign_color(R, white).

% (E) White and yellow are used together in a rug
option(e) :- assign_color(R, white), assign_color(R, yellow).

#show option/1.