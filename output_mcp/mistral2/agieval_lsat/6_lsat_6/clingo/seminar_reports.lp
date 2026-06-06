% Base facts
student(george). student(helen). student(irving). student(kyle).
student(lenore). student(nina). student(olivia). student(robert).

% Days and time slots
day(monday). day(tuesday). day(wednesday).
time(morning). time(afternoon).

% Assignments: report(Student, Day, Time)
% Exactly 6 reports in total, 2 per day (morning and afternoon)

% George can only give a report on Tuesday
:- report(george, Day, _), Day != tuesday.

% Olivia and Robert cannot give afternoon reports
:- report(olivia, _, afternoon).
:- report(robert, _, afternoon).

% If Nina gives a report, then on the next day Helen and Irving must both give reports,
% unless Nina's report is on Wednesday.
:- report(nina, Day, _),
   not report(helen, NextDay, _),
   not report(irving, NextDay, _),
   next_day(Day, NextDay),
   Day != wednesday.

% Helper: next_day/2
next_day(monday, tuesday).
next_day(tuesday, wednesday).

% Exactly 6 reports in total
1 { report(S, D, T) : student(S), day(D), time(T) } 6.

% Exactly 2 reports per day
:- day(D), 2 { report(_, D, _) } 2.

% Exactly one report per time slot per day
:- day(D), time(T), 1 { report(_, D, T) } 1.

% Morning reports are given by Helen, Kyle, and Lenore (in some order)
:- time(morning), student(S), report(S, _, morning),
   not (S = helen ; S = kyle ; S = lenore).

% Ensure all three morning reports are assigned to Helen, Kyle, or Lenore
morning_reports(S) :- report(S, _, morning), student(S).
:- time(morning), 3 { morning_reports(S) } 3.

% Define the correct answer mapping
% (A) Helen gives a report on Monday.
option(a) :- report(helen, monday, _).

% (B) Irving gives a report on Monday.
option(b) :- report(irving, monday, _).

% (C) Irving gives a report on Wednesday.
option(c) :- report(irving, wednesday, _).

% (D) Kyle gives a report on Tuesday.
option(d) :- report(kyle, tuesday, _).

% (E) Kyle gives a report on Wednesday.
option(e) :- report(kyle, wednesday, _).

#show option/1.