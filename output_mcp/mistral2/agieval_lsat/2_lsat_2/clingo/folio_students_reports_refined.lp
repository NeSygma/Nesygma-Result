% Base facts: students, days, and time slots
student(george).
student(helen).
student(irving).
student(kyle).
student(lenore).
student(nina).
student(olivia).
student(robert).

day(monday).
day(tuesday).
day(wednesday).

time(morning).
time(afternoon).

% George can only give a report on Tuesday
:- report(george, D, _), D != tuesday.

% Neither Olivia nor Robert can give an afternoon report
:- report(olivia, _, afternoon).
:- report(robert, _, afternoon).

% If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is on Wednesday
:- report(nina, D, _), D != wednesday, not next_day_helen_irving(D).

next_day_helen_irving(D) :-
    day(D), 
    day(D1), 
    next_day(D, D1),
    report(helen, D1, _),
    report(irving, D1, _).

next_day(monday, tuesday).
next_day(tuesday, wednesday).

% Exactly six students give reports
{ report(S, D, T) : student(S), day(D), time(T) } = 6.

% Exactly two reports per day
:- day(D), { report(_, D, _) } != 2.

% Exactly one report per time slot per day
:- day(D), time(T), { report(_, D, T) } != 1.

% Kyle and Lenore do not give reports
:- report(kyle, _, _).
:- report(lenore, _, _).

% Define the next day relationship
next_day(monday, tuesday).
next_day(tuesday, wednesday).

% Define the morning reports for Monday, Tuesday, and Wednesday
morning_report_monday(S) :- report(S, monday, morning).
morning_report_tuesday(S) :- report(S, tuesday, morning).
morning_report_wednesday(S) :- report(S, wednesday, morning).

% Ensure that only one option is selected
:- option(X), option(Y), X != Y.

% Define the options
option(a) :-
    morning_report_monday(helen),
    morning_report_tuesday(george),
    morning_report_wednesday(nina).

option(b) :-
    morning_report_monday(irving),
    morning_report_tuesday(robert),
    morning_report_wednesday(helen).

option(c) :-
    morning_report_monday(nina),
    morning_report_tuesday(helen),
    morning_report_wednesday(olivia).

option(d) :-
    morning_report_monday(olivia),
    morning_report_tuesday(robert),
    morning_report_wednesday(irving).

option(e) :-
    morning_report_monday(robert),
    morning_report_tuesday(george),
    morning_report_wednesday(helen).

% Ensure that at least one option is selected
:- not option(a), not option(b), not option(c), not option(d), not option(e).

#show option/1.