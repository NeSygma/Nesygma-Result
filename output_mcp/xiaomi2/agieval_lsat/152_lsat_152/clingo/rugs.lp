% Domain
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).
rug(1). rug(2). rug(3).

% Exactly 5 of 6 colors are used
{ used(C) : color(C) } 5.

% Each used color assigned to exactly one rug
{ assigned(C, R) : rug(R) } 1 :- used(C).
:- assigned(C, R), not used(C).

% Each rug has at least one color
:- rug(R), not has_color(R).
has_color(R) :- assigned(_, R).

% Exactly 2 solid rugs, 1 multicolored rug
solid(R) :- rug(R), #count{C : assigned(C, R)} = 1.
multicolored(R) :- rug(R), #count{C : assigned(C, R)} > 1.
:- #count{R : solid(R)} != 2.
:- #count{R : multicolored(R)} != 1.

% Rule 1: If white is used in a rug, two other colors are also used (3 total)
:- assigned(white, R), #count{C : assigned(C, R)} != 3.

% Rule 2: If olive is used in a rug, peach is also used in that rug
:- assigned(olive, R), not assigned(peach, R).

% Rule 3: Forest and turquoise not together
:- assigned(forest, R), assigned(turquoise, R).

% Rule 4: Peach and turquoise not together
:- assigned(peach, R), assigned(turquoise, R).

% Rule 5: Peach and yellow not together
:- assigned(peach, R), assigned(yellow, R).

% Identify the two solid rug colors
solid_color(C) :- assigned(C, R), solid(R).

% Check each option: can those two colors be the solid rug colors?
% We need to find which pair is IMPOSSIBLE

% Option A: forest and peach are solid
possible_a :- solid_color(forest), solid_color(peach).
% Option B: forest and yellow are solid
possible_b :- solid_color(forest), solid_color(yellow).
% Option C: peach and turquoise are solid
possible_c :- solid_color(peach), solid_color(turquoise).
% Option D: peach and yellow are solid
possible_d :- solid_color(peach), solid_color(yellow).
% Option E: turquoise and yellow are solid
possible_e :- solid_color(turquoise), solid_color(yellow).

% The answer is the option that is NOT possible (CANNOT be)
option(a) :- not possible_a.
option(b) :- not possible_b.
option(c) :- not possible_c.
option(d) :- not possible_d.
option(e) :- not possible_e.

#show option/1.