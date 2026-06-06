% Domains
student(george; helen; irving; kyle; lenore; nina; olivia; robert).
day(monday; tuesday; wednesday).
time(morning; afternoon).

% Helper to compute next day
next_day(monday, tuesday).
next_day(tuesday, wednesday).
next_day(wednesday, wednesday).

% Exactly 6 students give reports
{ gives_report(S) : student(S) } = 6.

% Assignments: student -> day -> time
% Exactly 2 reports per day: one morning and one afternoon
1 { assigned(S, D, T) : student(S), time(T) } 2 :- day(D).
:- assigned(S1, D, morning), assigned(S2, D, morning), S1 != S2.
:- assigned(S1, D, afternoon), assigned(S2, D, afternoon), S1 != S2.

% George can only give a report on Tuesday
:- assigned(george, D, T), D != tuesday.

% Olivia and Robert can only give morning reports
:- assigned(olivia, D, afternoon).
:- assigned(robert, D, afternoon).

% Nina's constraint: If Nina gives a report on day D and D != wednesday,
% then Helen and Irving must both give reports on the next day
:- assigned(nina, D, _), D != wednesday,
   not assigned(helen, NextD, _),
   not assigned(irving, NextD, _),
   next_day(D, NextD).

% Define same_day relation explicitly
same_day(S1, S2, D) :- assigned(S1, D, _), assigned(S2, D, _), S1 != S2.

% Define the condition for option (B) Helen and Nina on Wednesday
helen_nina_wednesday :- same_day(helen, nina, wednesday).

% Define conditions for other options (for completeness, though only (B) should be valid)
george_lenore_wednesday :- same_day(george, lenore, wednesday).
irving_robert_wednesday :- same_day(irving, robert, wednesday).
kyle_nina_wednesday :- same_day(kyle, nina, wednesday).
olivia_kyle_wednesday :- same_day(olivia, kyle, wednesday).

% Map the correct answer to option/1
option(a) :- george_lenore_wednesday.
option(b) :- helen_nina_wednesday.
option(c) :- irving_robert_wednesday.
option(d) :- kyle_nina_wednesday.
option(e) :- olivia_kyle_wednesday.

% Ensure that only one option is derived
:- option(X), option(Y), X != Y.

% Show the answer
#show option/1.