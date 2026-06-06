% Domain: colors and rugs
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).
rug(1). rug(2). rug(3).

% Exactly 5 of 6 colors are used
{ used(C) : color(C) } 5.

% Each used color is assigned to exactly one rug
{ assigned(C, R) : rug(R) } 1 :- used(C).

% Each rug must have at least one color (rugs are woven)
has_color(R) :- assigned(_, R).
:- rug(R), not has_color(R).

% Count colors per rug
color_count(R, N) :- rug(R), N = #count { C : assigned(C, R) }.

% Solid rug: exactly one color
solid(R) :- color_count(R, 1).

% RULE 1: White rule - if white is used, its rug has at least 3 colors
:- assigned(white, R), color_count(R, N), N < 3.

% RULE 2: Olive implies peach in same rug
:- assigned(olive, R), not assigned(peach, R).

% RULE 3: Forest and turquoise not together
:- assigned(forest, R), assigned(turquoise, R).

% RULE 4: Peach and turquoise not together
:- assigned(peach, R), assigned(turquoise, R).

% RULE 5: Peach and yellow not together
:- assigned(peach, R), assigned(yellow, R).

% CONDITION: Forest and peach are together in a rug
together_fp :- assigned(forest, R), assigned(peach, R).
:- not together_fp.

% Evaluate each option condition
% A: Exactly one solid rug
cond_a :- 1 { solid(R) : rug(R) } 1.

% B: White is not used in any rug
cond_b :- not used(white).

% C: Yellow is not used in any rug
cond_c :- not used(yellow).

% D: Turquoise and white are used together in a rug
cond_d :- assigned(turquoise, R), assigned(white, R).

% E: Turquoise and yellow are used together in a rug
cond_e :- assigned(turquoise, R), assigned(yellow, R).

% Map correct answer to option/1
option(a) :- cond_a.
option(b) :- cond_b.
option(c) :- cond_c.
option(d) :- cond_d.
option(e) :- cond_e.

#show option/1.