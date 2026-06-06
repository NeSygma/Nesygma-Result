% Colors and rugs
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).
rug(1). rug(2). rug(3).

% Each color can be assigned to at most one rug (0 or 1 assignment)
{ assigned(C, R) : rug(R) } :- color(C).

% Each rug must have at least one color
:- rug(R), #count{C : assigned(C, R)} = 0.

% A color is used if it is assigned to some rug
used(C) :- assigned(C, R).

% Exactly five colors are used
:- #count{C : used(C)} != 5.

% Rule 1: If white is used in a rug, that rug must have at least two other colors
:- assigned(white, R), #count{C : assigned(C, R), C != white} < 2.

% Rule 2: If olive is used in a rug, peach must also be used in that rug
:- assigned(olive, R), not assigned(peach, R).

% Rule 3: Forest and turquoise cannot be together in a rug
:- assigned(forest, R), assigned(turquoise, R).

% Rule 4: Peach and turquoise cannot be together in a rug
:- assigned(peach, R), assigned(turquoise, R).

% Rule 5: Peach and yellow cannot be together in a rug
:- assigned(peach, R), assigned(yellow, R).

% Condition: One rug is solid peach (only peach and no other color)
solid_peach(R) :- assigned(peach, R), #count{C : assigned(C, R)} = 1.
:- not { solid_peach(R) : rug(R) } >= 1.

% Helper: A rug is solid in color C if it has exactly one color and that color is C
solid_color(R, C) :- assigned(C, R), #count{C2 : assigned(C2, R)} = 1.

% Conditions for answer choices
cond_a :- solid_color(R, forest).
cond_b :- solid_color(R, turquoise).
cond_c :- solid_color(R, yellow).
cond_d :- assigned(forest, R), assigned(white, R).
cond_e :- assigned(white, R), assigned(yellow, R).

% Allow the solver to choose which condition to try to falsify
{ falsify(a) }.
{ falsify(b) }.
{ falsify(c) }.
{ falsify(d) }.
{ falsify(e) }.

% If we choose to falsify a condition, it must be false in the model
:- falsify(a), cond_a.
:- falsify(b), cond_b.
:- falsify(c), cond_c.
:- falsify(d), cond_d.
:- falsify(e), cond_e.

% Show relevant atoms
#show falsify/1.
#show cond_a/0.
#show cond_b/0.
#show cond_c/0.
#show cond_d/0.
#show cond_e/0.
#show assigned/2.