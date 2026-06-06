% Students
student(george). student(helen). student(irving). student(kyle). student(lenore). student(nina). student(olivia). student(robert).

% Days and slots
day(mon). day(tue). day(wed).
slot(morning). slot(afternoon).

% Next day relation
next(mon,tue). next(tue,wed).

% Exactly one report per day-slot
1 { report(S,D,SL) : student(S) } 1 :- day(D), slot(SL).

% A student cannot appear in two different slots (morning/afternoon) on same day
:- report(S,D,SL1), report(S,D,SL2), SL1 != SL2.
% A student cannot appear on two different days
:- report(S,D1,_), report(S,D2,_), D1 != D2.

% Fixed assignments
report(kyle, tue, afternoon).
report(helen, wed, afternoon).
report(george, tue, morning). % George only on Tuesday, must be morning (afternoon taken)

% Olivia and Robert cannot be afternoon
:- report(olivia, D, afternoon).
:- report(robert, D, afternoon).

% George only on Tuesday (already enforced by uniqueness, but add explicit constraint)
:- report(george, D, _), D != tue.

% Nina condition: if Nina reports not on Wednesday, next day must have both Helen and Irving (any slot)
:- report(nina, D, _), D != wed, next(D, DN), not report(helen, DN, _).
:- report(nina, D, _), D != wed, next(D, DN), not report(irving, DN, _).

% Helper for morning reports
morning(S,D) :- report(S,D,morning).

% Option definitions (morning reports for Mon, Tue, Wed respectively)
option(a) :- morning(irving, mon), morning(lenore, tue), morning(nina, wed).
option(b) :- morning(lenore, mon), morning(george, tue), morning(irving, wed).
option(c) :- morning(nina, mon), morning(irving, tue), morning(lenore, wed).
option(d) :- morning(robert, mon), morning(george, tue), morning(irving, wed).
option(e) :- morning(robert, mon), morning(irving, tue), morning(lenore, wed).

% Exactly one option must hold
:- option(X), option(Y), X != Y.
:- not option(_).

#show option/1.