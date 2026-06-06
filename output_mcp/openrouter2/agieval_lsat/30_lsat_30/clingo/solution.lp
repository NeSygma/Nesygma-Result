% Domain facts
baynum(1). baynum(2). baynum(3). baynum(4). baynum(5). baynum(6).
cargo(fuel). cargo(grain). cargo(livestock). cargo(machinery). cargo(produce). cargo(textiles).

% Bijection constraints: each bay gets exactly one cargo, each cargo assigned to exactly one bay
1 { bay(B, C) : cargo(C) } 1 :- baynum(B).
1 { bay(B, C) : baynum(B) } 1 :- cargo(C).

% Helper predicates for cargo positions
grain_bay(B) :- bay(B, grain).
livestock_bay(B) :- bay(B, livestock).
textiles_bay(B) :- bay(B, textiles).
produce_bay(B) :- bay(B, produce).
fuel_bay(B) :- bay(B, fuel).

% Constraints from the problem
:- grain_bay(B1), livestock_bay(B2), B1 <= B2.
:- livestock_bay(B1), textiles_bay(B2), B1 <= B2.
:- produce_bay(B1), fuel_bay(B2), B1 <= B2.
:- textiles_bay(B1), produce_bay(B2), B1 != B2+1, B1 != B2-1.

% Option selection
{opt(a); opt(b); opt(c); opt(d); opt(e)} 1.

% Enforce assignments for each option
:- opt(a), bay(1, X), X != fuel.
:- opt(a), bay(2, X), X != machinery.
:- opt(a), bay(3, X), X != textiles.

:- opt(b), bay(1, X), X != grain.
:- opt(b), bay(2, X), X != machinery.
:- opt(b), bay(3, X), X != fuel.

:- opt(c), bay(1, X), X != machinery.
:- opt(c), bay(2, X), X != livestock.
:- opt(c), bay(3, X), X != fuel.

:- opt(d), bay(1, X), X != machinery.
:- opt(d), bay(2, X), X != textiles.
:- opt(d), bay(3, X), X != fuel.

:- opt(e), bay(1, X), X != machinery.
:- opt(e), bay(2, X), X != textiles.
:- opt(e), bay(3, X), X != produce.

% Derive the chosen option
option(a) :- opt(a).
option(b) :- opt(b).
option(c) :- opt(c).
option(d) :- opt(d).
option(e) :- opt(e).

#show option/1.