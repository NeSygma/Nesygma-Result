% Domains
student(george; helen; irving; kyle; lenore; nina; olivia; robert).
day(monday; tuesday; wednesday).
time(morning; afternoon).

% Helper: next day relation
next_day(monday, tuesday).
next_day(tuesday, wednesday).

% Choice rule for report assignments
{ report(S, D, T) : student(S), day(D), time(T) } = 6.

% Exactly 2 reports per day
:- day(D), #count { S : report(S, D, _) } != 2.

% George can only give a report on Tuesday
:- report(george, D, _), D != tuesday.

% Olivia and Robert can only give morning reports
:- report(olivia, D, T), T != morning.
:- report(robert, D, T), T != morning.

% Nina's constraint: If Nina gives a report on day D (not Wednesday), 
% then Helen and Irving must both give reports on the next day
% Define a helper predicate for the next day of Nina's report
next_day_of_nina(D, ND) :- report(nina, D, _), D != wednesday, next_day(D, ND).

% Ensure Helen and Irving give reports on the next day of Nina's report
:- next_day_of_nina(D, ND), not report(helen, ND, _).
:- next_day_of_nina(D, ND), not report(irving, ND, _).

% Given condition: George, Nina, and Robert give reports on different days
:- report(george, D1, _), report(nina, D2, _), D1 = D2.
:- report(george, D1, _), report(robert, D3, _), D1 = D3.
:- report(nina, D2, _), report(robert, D3, _), D2 = D3.

% Sentinel to check if the constraints are satisfiable
solution_exists.

% Map the correct answer to option/1
% (A) Helen gives a report on Wednesday
option(a) :- solution_exists, report(helen, wednesday, _).

% (B) Nina gives a report on Monday
option(b) :- solution_exists, report(nina, monday, _).

% (C) Nina gives a report on Tuesday
option(c) :- solution_exists, report(nina, tuesday, _).

% (D) Olivia gives a report on Monday
option(d) :- solution_exists, report(olivia, monday, _).

% (E) Robert gives a report on Wednesday
option(e) :- solution_exists, report(robert, wednesday, _).

#show option/1.
#show solution_exists.