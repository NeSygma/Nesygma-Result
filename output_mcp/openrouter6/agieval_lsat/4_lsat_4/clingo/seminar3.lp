% Seminar scheduling problem

% Domains
day(mon). day(tue). day(wed).
slot(am). slot(pm).
student(george). student(helen). student(irving). student(kyle). student(lenore). student(nina). student(olivia). student(robert).

% Day numbers for next day calculation
day_num(mon, 1). day_num(tue, 2). day_num(wed, 3).
next_day(Day, Next) :- day_num(Day, N), day_num(Next, N+1).

% Each student gives at most one report (choice over day and slot)
{ gives(Student, Day, Slot) : day(Day), slot(Slot) } 0..1 :- student(Student).

% Exactly one morning and one afternoon per day
1 { gives(Student, Day, am) : student(Student) } 1 :- day(Day).
1 { gives(Student, Day, pm) : student(Student) } 1 :- day(Day).

% Exactly 6 students give reports
gives(Student) :- gives(Student, _, _).
:- #count{ Student : gives(Student) } != 6.

% Constraint 1: George only on Tuesday
:- gives(george, Day, _), Day != tue.

% Constraint 2: Olivia and Robert cannot give afternoon
:- gives(olivia, _, pm).
:- gives(robert, _, pm).

% Constraint 3: If Nina gives on a day other than Wednesday, then next day both Helen and Irving give
:- gives(nina, Day, _), Day != wed, not gives(helen, Next, _), next_day(Day, Next).
:- gives(nina, Day, _), Day != wed, not gives(irving, Next, _), next_day(Day, Next).

% Additional given: George, Nina, Robert give reports and on different days
gives(george). gives(nina). gives(robert).
:- gives(george, DayG, _), gives(nina, DayN, _), DayG = DayN.
:- gives(george, DayG, _), gives(robert, DayR, _), DayG = DayR.
:- gives(nina, DayN, _), gives(robert, DayR, _), DayN = DayR.

% Derive which option could be true in this model.
option(a) :- gives(helen, wed, _).
option(b) :- gives(nina, mon, _).
option(c) :- gives(nina, tue, _).
option(d) :- gives(olivia, mon, _).
option(e) :- gives(robert, wed, _).

% Show only the option that is true.
#show option/1.