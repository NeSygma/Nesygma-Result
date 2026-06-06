% Seminar scheduling problem - debug version

% Domains
day(monday). day(tuesday). day(wednesday).
time(morning). time(afternoon).
student(george). student(helen). student(irving). student(nina). student(olivia). student(robert).

% Assignment: each student assigned to exactly one slot
1 { assigned(Student, Day, Time) : day(Day), time(Time) } 1 :- student(Student).

% Each day-time slot has exactly one student
1 { assigned(Student, Day, Time) : student(Student) } 1 :- day(Day), time(Time).

% George only on Tuesday
:- assigned(george, monday, _).
:- assigned(george, wednesday, _).

% Olivia and Robert only morning
:- assigned(olivia, _, afternoon).
:- assigned(robert, _, afternoon).

% Nina condition
% If Nina on Monday, then Tuesday must have both Helen and Irving
:- assigned(nina, monday, _), not assigned(helen, tuesday, _).
:- assigned(nina, monday, _), not assigned(irving, tuesday, _).

% If Nina on Tuesday, then Wednesday must have both Helen and Irving
:- assigned(nina, tuesday, _), not assigned(helen, wednesday, _).
:- assigned(nina, tuesday, _), not assigned(irving, wednesday, _).

% If Nina on Wednesday, no condition.

% Show all assignments for debugging
#show assigned/3.

% Option rules (for final answer)
option(a) :- assigned(helen, monday, morning), assigned(george, tuesday, morning), assigned(nina, wednesday, morning).
option(b) :- assigned(irving, monday, morning), assigned(robert, tuesday, morning), assigned(helen, wednesday, morning).
option(c) :- assigned(nina, monday, morning), assigned(helen, tuesday, morning), assigned(olivia, wednesday, morning).
option(d) :- assigned(olivia, monday, morning), assigned(robert, tuesday, morning), assigned(irving, wednesday, morning).
option(e) :- assigned(robert, monday, morning), assigned(george, tuesday, morning), assigned(helen, wednesday, morning).

#show option/1.