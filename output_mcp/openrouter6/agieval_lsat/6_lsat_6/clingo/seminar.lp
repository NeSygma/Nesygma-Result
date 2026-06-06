% Students
student(george). student(helen). student(irving). student(kyle). student(lenore). student(nina). student(olivia). student(robert).

% Days
day(monday). day(tuesday). day(wednesday).

% Times
time(morning). time(afternoon).

% Exactly one morning and one afternoon report per day
1 { gives(Student, Day, morning) : student(Student) } 1 :- day(Day).
1 { gives(Student, Day, afternoon) : student(Student) } 1 :- day(Day).

% Each student gives at most one report
:- gives(Student, Day1, Time1), gives(Student, Day2, Time2), (Day1,Time1) != (Day2,Time2).

% Exactly six reporters (since six reports total)
reporter(Student) :- gives(Student, _, _).
6 { reporter(Student) : student(Student) } 6.

% Constraint 1: George only on Tuesday
:- gives(george, Day, _), Day != tuesday.

% Constraint 2: Olivia and Robert cannot give afternoon reports
:- gives(olivia, _, afternoon).
:- gives(robert, _, afternoon).

% Helper: gives on a day (any time)
gives_on_day(Student, Day) :- gives(Student, Day, _).

% Constraint 3: If Nina gives on Monday, then next day (Tuesday) Helen and Irving must both give reports
:- gives(nina, monday, _), not gives_on_day(helen, tuesday).
:- gives(nina, monday, _), not gives_on_day(irving, tuesday).

% Constraint 3: If Nina gives on Tuesday, then next day (Wednesday) Helen and Irving must both give reports
:- gives(nina, tuesday, _), not gives_on_day(helen, wednesday).
:- gives(nina, tuesday, _), not gives_on_day(irving, wednesday).

% Morning condition: The three morning reports are given by Helen, Kyle, Lenore (each exactly one)
1 { gives(helen, Day, morning) : day(Day) } 1.
1 { gives(kyle, Day, morning) : day(Day) } 1.
1 { gives(lenore, Day, morning) : day(Day) } 1.
% No other student gives a morning report
:- gives(Student, _, morning), Student != helen, Student != kyle, Student != lenore.

% Derive answer choices
helen_monday :- gives(helen, monday, morning).
irving_monday :- gives(irving, monday, afternoon).
irving_wednesday :- gives(irving, wednesday, _).
kyle_tuesday :- gives(kyle, tuesday, morning).
kyle_wednesday :- gives(kyle, wednesday, morning).

% Map the correct answer to option/1 (MANDATORY)
% We will derive which one must be true by checking consistency.
% For now, we define each option as the condition that makes it true.
option(a) :- helen_monday.
option(b) :- irving_monday.
option(c) :- irving_wednesday.
option(d) :- kyle_tuesday.
option(e) :- kyle_wednesday.

% Show the options and some key facts for debugging
#show option/1.
#show gives/3.
#show reporter/1.
#show helen_monday.
#show irving_monday.
#show irving_wednesday.
#show kyle_tuesday.
#show kyle_wednesday.