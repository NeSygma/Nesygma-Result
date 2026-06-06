% Seminar scheduling problem

% Domains
day(monday). day(tuesday). day(wednesday).
time(morning). time(afternoon).
student(george). student(helen). student(irving). student(kyle). student(lenore). student(nina). student(olivia). student(robert).

% Exactly six students give reports
6 { gives_report(Student) : student(Student) } 6.

% Each student who gives report gets exactly one slot
1 { assigned(Student, Day, Time) : day(Day), time(Time) } 1 :- gives_report(Student).

% Each slot gets exactly one student
1 { assigned(Student, Day, Time) : student(Student) } 1 :- day(Day), time(Time).

% Kyle and Lenore do not give reports
:- gives_report(kyle).
:- gives_report(lenore).

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

% Define morning assignments for convenience
morning(Day, Student) :- assigned(Student, Day, morning).

% Option rules (for final answer)
option(a) :- morning(monday, helen), morning(tuesday, george), morning(wednesday, nina).
option(b) :- morning(monday, irving), morning(tuesday, robert), morning(wednesday, helen).
option(c) :- morning(monday, nina), morning(tuesday, helen), morning(wednesday, olivia).
option(d) :- morning(monday, olivia), morning(tuesday, robert), morning(wednesday, irving).
option(e) :- morning(monday, robert), morning(tuesday, george), morning(wednesday, helen).

#show option/1.
#show morning/2.