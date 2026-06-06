% Domains
student(george). student(helen). student(irving). student(kyle). student(lenore). student(nina). student(olivia). student(robert).

time(morning). time(afternoon).

day(mon). day(tue). day(wed).

slot(mon,morning). slot(mon,afternoon).
slot(tue,morning). slot(tue,afternoon).
slot(wed,morning). slot(wed,afternoon).

% Exactly one student per slot
1 { report(S,D,T) : student(S) } 1 :- slot(D,T).

% Each student at most one report
:- report(S,D1,T1), report(S,D2,T2), (D1,T1) != (D2,T2).

% Exactly six reports total
:- 6 != #count { S,D,T : report(S,D,T) }.

% George only Tuesday and must report
:- not report(george, tue, _).
:- report(george, D, _), D != tue.

% Olivia and Robert cannot be afternoon
:- report(olivia, _, afternoon).
:- report(robert, _, afternoon).

% Nina condition: if Nina reports not on Wednesday, next day must have both Helen and Irving
next(mon,tue). next(tue,wed).
% If Nina on a day with a next day, enforce both Helen and Irving on that next day
:- report(nina, D, _), D != wed, next(D, Dnext), not report(helen, Dnext, _).
:- report(nina, D, _), D != wed, next(D, Dnext), not report(irving, Dnext, _).

% Additional condition: George, Nina, Robert give reports on different days
:- not report(nina, _, _).
:- not report(robert, _, _).
:- report(george, D, _), report(nina, D, _).
:- report(george, D, _), report(robert, D, _).
:- report(nina, D, _), report(robert, D, _).

% Option selection
1 { opt(a); opt(b); opt(c); opt(d); opt(e) } 1.

% Link options to conditions
:- opt(a), not report(helen, wed, _).
:- opt(b), not report(nina, mon, _).
:- opt(c), not report(nina, tue, _).
:- opt(d), not report(olivia, mon, _).
:- opt(e), not report(robert, wed, _).

% Show the selected option
#show opt/1.