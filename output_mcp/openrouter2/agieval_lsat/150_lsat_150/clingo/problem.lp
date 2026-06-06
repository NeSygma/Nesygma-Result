% Facts
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).
rug(r1). rug(r2). rug(r3).

% Exactly 5 colors used
5 { used(C) : color(C) } 5.

% Each used color assigned to exactly one rug
{ assign(C, R) : rug(R) } 1 :- used(C).

% No assignment for unused colors
:- assign(C, R), not used(C).

% Each rug has at least one color
assigned_to(R) :- assign(_, R).
:- rug(R), not assigned_to(R).

% Constraints
:- assign(white, R), #count{C : assign(C, R)} < 3.
:- assign(olive, R), not assign(peach, R).
:- assign(forest, R), assign(turquoise, R).
:- assign(peach, R), assign(turquoise, R).
:- assign(peach, R), assign(yellow, R).

% Peach must be used
:- not used(peach).

% Option mapping
option(c) :- used(peach).

#show option/1.