% Colors
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).

% Rugs
rug(r1). rug(r2). rug(r3).

% Choose exactly five colors to be used
{ used(C) } :- color(C).
% Exactly five used colors
:- #count{ C : used(C) } != 5.

% Assign each used color to exactly one rug
1 { assign(C,R) : rug(R) } 1 :- used(C).
% No assignment for unused colors
:- assign(C,R), not used(C).

% Each rug must have at least one color
has_color(R) :- assign(C,R).
:- rug(R), not has_color(R).

% White rule: if white is in a rug, that rug must have at least three colors
:- assign(white,R), #count{ C : assign(C,R) } < 3.

% Olive implies peach in same rug
:- assign(olive,R), not assign(peach,R).

% Forbidden co‑occurrences
:- assign(forest,R), assign(turquoise,R).
:- assign(peach,R), assign(turquoise,R).
:- assign(peach,R), assign(yellow,R).

% Condition: forest and peach together in some rug
together_fp :- assign(forest,R), assign(peach,R).
:- not together_fp.

% Helper for solid rug (exactly one color)
solid(R) :- rug(R), #count{ C : assign(C,R) } = 1.

% Option conditions
cond_a :- #count{ R : solid(R) } = 1.
cond_b :- not used(white).
cond_c :- not used(yellow).
cond_d :- assign(turquoise,R), assign(white,R).
cond_e :- assign(turquoise,R), assign(yellow,R).

% Exactly one option must be chosen
1 { option(a); option(b); option(c); option(d); option(e) } 1.
% Link options to conditions (iff)
:- option(a), not cond_a.
:- cond_a, not option(a).
:- option(b), not cond_b.
:- cond_b, not option(b).
:- option(c), not cond_c.
:- cond_c, not option(c).
:- option(d), not cond_d.
:- cond_d, not option(d).
:- option(e), not cond_e.
:- cond_e, not option(e).

#show option/1.