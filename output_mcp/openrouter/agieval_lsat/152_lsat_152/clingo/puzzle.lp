% Colors
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).

% Rugs
rug(1..3).

% Exactly one option considered
1 { consider(a); consider(b); consider(c); consider(d); consider(e) } 1.

% Forced solid colors per option
forced_solid(forest) :- consider(a).
forced_solid(peach) :- consider(a).

forced_solid(forest) :- consider(b).
forced_solid(yellow) :- consider(b).

forced_solid(peach) :- consider(c).
forced_solid(turquoise) :- consider(c).

forced_solid(peach) :- consider(d).
forced_solid(yellow) :- consider(d).

forced_solid(turquoise) :- consider(e).
forced_solid(yellow) :- consider(e).

% Choose which colors are used (exactly 5)
5 { used(C) : color(C) } 5.

% Each used color assigned to exactly one rug
1 { in(C,R) : rug(R) } 1 :- used(C).

% Define solid_color: a color is solid if its rug has exactly one color
solid_color(C) :- used(C), in(C,R), #count{D : in(D,R)} = 1.

% Enforce forced solid colors are used and solid
:- forced_solid(C), not used(C).
:- forced_solid(C), not solid_color(C).

% No other solid colors besides forced ones
:- used(C), solid_color(C), not forced_solid(C).

% Count solid rugs (should be exactly 2)
solid_rug(R) :- rug(R), #count{C : in(C,R)} = 1.
% Violation if not exactly two solid rugs
violation_solid_count :- #count{R : solid_rug(R)} != 2.

% White rule: if white used, its rug must have exactly 3 colors
violation_white :- used(white), in(white,R), #count{C : in(C,R)} != 3.

% Olive rule: if olive used, peach must be in same rug
violation_olive :- used(olive), in(olive,R), not in(peach,R).

% Forbidden co-occurrences
violation_ft :- in(forest,R), in(turquoise,R).
violation_pt :- in(peach,R), in(turquoise,R).
violation_py :- in(peach,R), in(yellow,R).

% Bad if any violation
bad :- violation_solid_count.
bad :- violation_white.
bad :- violation_olive.
bad :- violation_ft.
bad :- violation_pt.
bad :- violation_py.

% Minimize bad to prefer consistent models
#minimize { 1 : bad }.

% Option derived if bad holds in optimal model for that considered option
option(a) :- consider(a), bad.
option(b) :- consider(b), bad.
option(c) :- consider(c), bad.
option(d) :- consider(d), bad.
option(e) :- consider(e), bad.

#show option/1.