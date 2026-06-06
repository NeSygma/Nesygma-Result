% Students
student(george). student(helen). student(irving). student(kyle). student(lenore). student(nina). student(olivia). student(robert).

% Days and times
day(mon). day(tue). day(wed).
time(m). time(a).

% Next day relation
next(mon,tue). next(tue,wed).

% Exactly one report per slot (day,time)
1 { report(S,D,T) : student(S) } 1 :- day(D), time(T).

% At most one report per student
:- report(S,D1,T1), report(S,D2,T2), (D1,T1) != (D2,T2).

% George only on Tuesday and must give a report
:- report(george, D, _), D != tue.
:- not report(george, tue, _).

% Olivia and Robert cannot be afternoon
:- report(olivia, _, a).
:- report(robert, _, a).

% Nina condition: if Nina gives a report not on Wednesday, then next day Helen morning and Irving afternoon
:- report(nina, D, _), D != wed, next(D,N), not report(helen, N, m).
:- report(nina, D, _), D != wed, next(D,N), not report(irving, N, a).

% Morning reports are exactly Helen, Kyle, Lenore (each exactly once)
1 { report(helen, D, m) : day(D) } 1.
1 { report(kyle, D, m) : day(D) } 1.
1 { report(lenore, D, m) : day(D) } 1.
% No other student can be assigned to a morning slot
:- report(S, _, m), S != helen, S != kyle, S != lenore.

% Options mapping
option(a) :- report(helen, mon, m).
option(b) :- report(irving, mon, _).
option(c) :- report(irving, wed, _).
option(d) :- report(kyle, tue, m).
option(e) :- report(kyle, wed, m).

#show option/1.