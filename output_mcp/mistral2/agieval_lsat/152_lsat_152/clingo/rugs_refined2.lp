% Define the colors and rugs
color(forest; olive; peach; turquoise; white; yellow).
rug(r1; r2; r3).

% Exactly five colors are used
1 { used_color(C) : color(C) } 5.

% Each used color is assigned to exactly one rug
1 { assigned_color(R, C) : rug(R) } 1 :- used_color(C).

% A rug is solid if it uses exactly one color
solid(R) :- rug(R), #count { C : assigned_color(R, C) } = 1.
multicolored(R) :- rug(R), #count { C : assigned_color(R, C) } > 1.

% Constraints on color usage
% 1. In any rug in which white is used, two other colors are also used
:- assigned_color(R, white), #count { C : assigned_color(R, C) } = 1.

% 2. In any rug in which olive is used, peach is also used
:- assigned_color(R, olive), not assigned_color(R, peach).

% 3. Forest and turquoise are not used together in a rug
:- assigned_color(R, forest), assigned_color(R, turquoise).

% 4. Peach and turquoise are not used together in a rug
:- assigned_color(R, peach), assigned_color(R, turquoise).

% 5. Peach and yellow are not used together in a rug
:- assigned_color(R, peach), assigned_color(R, yellow).

% Exactly two solid rugs
2 { solid(R) : rug(R) } 2.

% Define the colors of the solid rugs
solid_color(R, C) :- solid(R), assigned_color(R, C).

% Check for invalid pairs of solid rug colors
% (A) forest and peach
invalid_a :- solid_color(R1, forest), solid_color(R2, peach), R1 != R2.

% (B) forest and yellow
invalid_b :- solid_color(R1, forest), solid_color(R2, yellow), R1 != R2.

% (C) peach and turquoise
invalid_c :- solid_color(R1, peach), solid_color(R2, turquoise), R1 != R2.

% (D) peach and yellow
invalid_d :- solid_color(R1, peach), solid_color(R2, yellow), R1 != R2.

% (E) turquoise and yellow
invalid_e :- solid_color(R1, turquoise), solid_color(R2, yellow), R1 != R2.

% Derive the answer
answer(a) :- invalid_a, not invalid_b, not invalid_c, not invalid_d, not invalid_e.
answer(b) :- invalid_b, not invalid_a, not invalid_c, not invalid_d, not invalid_e.
answer(c) :- invalid_c, not invalid_a, not invalid_b, not invalid_d, not invalid_e.
answer(d) :- invalid_d, not invalid_a, not invalid_b, not invalid_c, not invalid_e.
answer(e) :- invalid_e, not invalid_a, not invalid_b, not invalid_c, not invalid_d.

#show answer/1.