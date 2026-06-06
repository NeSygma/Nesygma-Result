% Chemistry Lab Session Assignment Problem

% Domains
day(wednesday). day(thursday). day(friday).
time(morning). time(afternoon).
assistant(julio). assistant(kevin). assistant(lan). assistant(nessa). assistant(olivia). assistant(rebecca).

% Sessions: 2 per day (morning and afternoon)
session(D, T) :- day(D), time(T).

% Each assistant leads exactly one session
1 { leads(A, D, T) : session(D, T) } 1 :- assistant(A).

% Each session has exactly one assistant
1 { leads(A, D, T) : assistant(A) } 1 :- session(D, T).

% Constraint 1: Kevin and Rebecca must lead sessions on the same day
same_day(A1, A2) :- leads(A1, D, _), leads(A2, D, _), A1 != A2.
:- leads(kevin, D1, _), leads(rebecca, D2, _), D1 != D2.

% Constraint 2: Lan and Olivia cannot lead sessions on the same day
:- leads(lan, D, _), leads(olivia, D, _).

% Constraint 3: Nessa must lead an afternoon session
:- leads(nessa, D, T), T != afternoon.

% Constraint 4: Julio's session must meet on an earlier day than Olivia's
% Define day order
day_order(wednesday, thursday). day_order(thursday, friday). day_order(wednesday, friday).
earlier_day(A1, A2) :- leads(A1, D1, _), leads(A2, D2, _), day_order(D1, D2).
:- leads(julio, D1, _), leads(olivia, D2, _), not earlier_day(julio, olivia).

% Additional condition: Lan does not lead a Wednesday session
:- leads(lan, wednesday, _).

% Helper: Determine which assistants lead on Thursday
leads_thursday(A) :- leads(A, thursday, _).

% Map the correct answer to option/1
% We need to find which assistant MUST lead a Thursday session
% This means in ALL valid models, that assistant leads on Thursday

% For each option, check if it's forced to lead on Thursday
option(a) :- leads_thursday(rebecca).
option(b) :- leads_thursday(olivia).
option(c) :- leads_thursday(nessa).
option(d) :- leads_thursday(kevin).
option(e) :- leads_thursday(julio).

#show option/1.
#show leads/3.