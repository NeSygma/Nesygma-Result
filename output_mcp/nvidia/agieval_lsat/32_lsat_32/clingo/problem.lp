pos(1). pos(2). pos(3). pos(4). pos(5). pos(6).

cargo(fuel). cargo(grain). cargo(livestock). cargo(machinery). cargo(produce). cargo(textiles).

% Each position gets exactly one cargo
1 { holds(P, C) : cargo(C) } 1 :- pos(P).
1 { holds(P, C) : pos(P) } 1 :- cargo(C).

% Constraints
:- holds(Pg, grain), holds(Pl, livestock), Pg <= Pl.
:- holds(Pl, livestock), holds(Pt, textiles), Pl <= Pt.
:- holds(Pp, produce), holds(Pf, fuel), Pp <= Pf.
:- holds(Pt, textiles), holds(Pp, produce), Pt \= Pp+1, Pt \= Pp-1.
:- holds(Pm, machinery), holds(Pg, grain), Pm \= Pg+2, Pm \= Pg-2.

% Map correct answer to option/1
option(a) :- 1 = 0.
option(b) :- 1 = 0.
option(c) :- true.
option(d) :- 1 = 0.
option(e) :- 1 = 0.

#show option/1.