% Define the days and sessions
day(wednesday). day(thursday). day(friday).
session(am). session(pm).

% Define the lab assistants
assistant(julio). assistant(kevin). assistant(lan). assistant(nessa). assistant(olivia). assistant(rebecca).

% Assign each session a unique day and session time
1 { assigned_assistant(Assistant, Day, Session) : assistant(Assistant) } 1 :-
    day(Day), session(Session).

% Constraints:
% 1. Kevin and Rebecca must lead sessions on the same day
:- assigned_assistant(kevin, Day, _),
     assigned_assistant(rebecca, Day2, _),
     Day != Day2.

% 2. Lan and Olivia cannot lead sessions on the same day
:- assigned_assistant(lan, Day, _),
     assigned_assistant(olivia, Day, _).

% 3. Nessa must lead an afternoon session
:- assigned_assistant(nessa, _, am).

% 4. Julio's session must be on an earlier day than Olivia's
day_order(wednesday, thursday).
day_order(wednesday, friday).
day_order(thursday, friday).

:- assigned_assistant(julio, Day1, _),
     assigned_assistant(olivia, Day2, _),
     not day_order(Day1, Day2).

% Given condition: Lan does not lead a Wednesday session
:- assigned_assistant(lan, wednesday, _).

% Define a predicate for assistants leading a Thursday session
leads_thursday(Assistant) :-
    assigned_assistant(Assistant, thursday, _).

% Ensure only one assistant leads a Thursday session
1 { leads_thursday(Assistant) : assistant(Assistant) } 1.

% Map the correct answer to option/1
option(a) :- leads_thursday(rebecca).
option(b) :- leads_thursday(olivia).
option(c) :- leads_thursday(nessa).
option(d) :- leads_thursday(kevin).
option(e) :- leads_thursday(julio).

% Show the assignments and the option
#show assigned_assistant/3.
#show option/1.