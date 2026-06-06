% Domain
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).
rug(1). rug(2). rug(3).

{ used(C) : color(C) } 5.
{ assigned(C, R) : rug(R) } 1 :- used(C).
:- assigned(C, R), not used(C).
:- rug(R), #count{C : assigned(C, R)} = 0.

solid(R) :- rug(R), #count{C : assigned(C, R)} = 1.
multicolored(R) :- rug(R), #count{C : assigned(C, R)} > 1.
:- #count{R : solid(R)} != 2.
:- #count{R : multicolored(R)} != 1.

:- assigned(white, R), #count{C : assigned(C, R)} != 3.
:- assigned(olive, R), not assigned(peach, R).
:- assigned(forest, R), assigned(turquoise, R).
:- assigned(peach, R), assigned(turquoise, R).
:- assigned(peach, R), assigned(yellow, R).

solid_color(C) :- assigned(C, R), solid(R).

% Force pair A: forest and peach are solid
:- not solid_color(forest).
:- not solid_color(peach).

#show assigned/2.
#show solid/1.