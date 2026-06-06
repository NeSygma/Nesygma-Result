% Domain definitions
student(george). student(helen). student(irving). student(kyle).
student(lenore). student(nina). student(olivia). student(robert).

day(monday). day(tuesday). day(wednesday).
period(morning). period(afternoon).

% Exactly 6 students give reports
6 { gives_report(S) : student(S) } 6.

% Each report is assigned to exactly one day and period
{ report(S, D, P) : day(D), period(P) } 1 :- gives_report(S).

% Exactly 2 reports per day (one morning, one afternoon)
2 { report(S, D, P) : student(S) } 2 :- day(D), period(P).

% Each period on each day has exactly one report
1 { report(S, D, morning) : student(S) } 1 :- day(D).
1 { report(S, D, afternoon) : student(S) } 1 :- day(D).

% Condition 1: Tuesday is the only day George can give a report
:- report(george, D, P), D != tuesday.

% Condition 2: Neither Olivia nor Robert can give an afternoon report
:- report(olivia, D, afternoon).
:- report(robert, D, afternoon).

% Condition 3: If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is on Wednesday
% First, derive when Nina gives a report
nina_reports :- gives_report(nina).

% Get Nina's report day
nina_day(D) :- report(nina, D, P).

% If Nina reports on Monday, then Helen and Irving must report on Tuesday
:- nina_day(monday), not report(helen, tuesday, _).
:- nina_day(monday), not report(irving, tuesday, _).

% If Nina reports on Tuesday, then Helen and Irving must report on Wednesday
:- nina_day(tuesday), not report(helen, wednesday, _).
:- nina_day(tuesday), not report(irving, wednesday, _).

% Additional constraints from question: George, Nina, and Robert give reports and they do so on different days
gives_report(george).
gives_report(nina).
gives_report(robert).

% They must be on different days
:- report(george, D1, _), report(nina, D2, _), D1 == D2.
:- report(george, D1, _), report(robert, D2, _), D1 == D2.
:- report(nina, D1, _), report(robert, D2, _), D1 == D2.

% Helper predicates for answer choices
helen_wednesday :- report(helen, wednesday, _).
nina_monday :- report(nina, monday, _).
nina_tuesday :- report(nina, tuesday, _).
olivia_monday :- report(olivia, monday, _).
robert_wednesday :- report(robert, wednesday, _).

% Map the correct answer to option/1
option(a) :- helen_wednesday.
option(b) :- nina_monday.
option(c) :- nina_tuesday.
option(d) :- olivia_monday.
option(e) :- robert_wednesday.

#show option/1.