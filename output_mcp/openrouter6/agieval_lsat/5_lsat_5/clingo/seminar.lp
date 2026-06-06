% Students
student(george). student(helen). student(irving). student(kyle).
student(lenore). student(nina). student(olivia). student(robert).

% Days: 1=Monday, 2=Tuesday, 3=Wednesday
day(1). day(2). day(3).

% Times
time(morning). time(afternoon).

% Slots
slot(D, T) :- day(D), time(T).

% Assign each slot to exactly one student
1 { assign(D, T, S) : student(S) } 1 :- slot(D, T).

% Each student gives at most one report
:- assign(D1, T1, S), assign(D2, T2, S), (D1, T1) != (D2, T2).

% Constraint 1: George only on Tuesday
:- assign(D, T, george), D != 2.

% Constraint 2: Olivia and Robert cannot give afternoon reports
:- assign(D, afternoon, olivia).
:- assign(D, afternoon, robert).

% Helper: gives_on_day(Student, Day)
gives_on_day(S, D) :- assign(D, _, S).

% Constraint 3: Nina condition
% If Nina gives on Monday, then Tuesday must have both Helen and Irving
:- assign(1, _, nina), not gives_on_day(helen, 2).
:- assign(1, _, nina), not gives_on_day(irving, 2).
% If Nina gives on Tuesday, then Wednesday must have both Helen and Irving
:- assign(2, _, nina), not gives_on_day(helen, 3).
:- assign(2, _, nina), not gives_on_day(irving, 3).

% Fixed assignments
assign(2, afternoon, kyle).
assign(3, afternoon, helen).

% Morning reports
morning(1, S) :- assign(1, morning, S).
morning(2, S) :- assign(2, morning, S).
morning(3, S) :- assign(3, morning, S).

% Option conditions
option(a) :- morning(1, irving), morning(2, lenore), morning(3, nina).
option(b) :- morning(1, lenore), morning(2, george), morning(3, irving).
option(c) :- morning(1, nina), morning(2, irving), morning(3, lenore).
option(d) :- morning(1, robert), morning(2, george), morning(3, irving).
option(e) :- morning(1, robert), morning(2, irving), morning(3, lenore).

#show option/1.