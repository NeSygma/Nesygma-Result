% Define the days and sessions
session(morning; afternoon).
day(wednesday; thursday; friday).

% Define the lab assistants
assistant(julio; kevin; lan; nessa; olivia; rebecca).

% Define the possible assignments: assistant X leads session Y on day Z
% We will use a choice rule to allow assignments and then constrain them
{ leads(A, S, D) : assistant(A), session(S), day(D) }.

% Constraint 1: Kevin and Rebecca must lead sessions on the same day
:- day(D), leads(kevin, _, D), not leads(rebecca, _, D).
:- day(D), leads(rebecca, _, D), not leads(kevin, _, D).

% Constraint 2: Lan and Olivia cannot lead sessions on the same day
:- day(D), leads(lan, _, D), leads(olivia, _, D).

% Constraint 3: Nessa must lead an afternoon session
:- assistant(nessa), not leads(nessa, afternoon, _).

% Constraint 4: Julio's session must meet on an earlier day than Olivia's
% We need to ensure that if Olivia is on day D, Julio must be on a day before D
:- day(D), leads(olivia, _, D), not (day(E) : E < D, leads(julio, _, E)).

% Ensure each session on each day has exactly one assistant
:- day(D), session(S), 2 { leads(A, S, D) : assistant(A) }.

% Ensure each assistant leads exactly one session
:- assistant(A), 2 { leads(A, S, D) : session(S), day(D) }.

% Define the choices for the multiple-choice options
% Each option is a specific assignment of assistants to morning and afternoon sessions on each day

% Option A: Wednesday: Rebecca, Kevin; Thursday: Julio, Lan; Friday: Nessa, Olivia
option(a) :-
    leads(rebecca, morning, wednesday),
    leads(kevin, afternoon, wednesday),
    leads(julio, morning, thursday),
    leads(lan, afternoon, thursday),
    leads(nessa, morning, friday),
    leads(olivia, afternoon, friday).

% Option B: Wednesday: Olivia, Nessa; Thursday: Julio, Lan; Friday: Kevin, Rebecca
option(b) :-
    leads(olivia, morning, wednesday),
    leads(nessa, afternoon, wednesday),
    leads(julio, morning, thursday),
    leads(lan, afternoon, thursday),
    leads(kevin, morning, friday),
    leads(rebecca, afternoon, friday).

% Option C: Wednesday: Lan, Kevin; Thursday: Rebecca, Julio; Friday: Olivia, Nessa
option(c) :-
    leads(lan, morning, wednesday),
    leads(kevin, afternoon, wednesday),
    leads(rebecca, morning, thursday),
    leads(julio, afternoon, thursday),
    leads(olivia, morning, friday),
    leads(nessa, afternoon, friday).

% Option D: Wednesday: Kevin, Rebecca; Thursday: Julio, Nessa; Friday: Olivia, Lan
option(d) :-
    leads(kevin, morning, wednesday),
    leads(rebecca, afternoon, wednesday),
    leads(julio, morning, thursday),
    leads(nessa, afternoon, thursday),
    leads(olivia, morning, friday),
    leads(lan, afternoon, friday).

% Option E: Wednesday: Julio, Lan; Thursday: Olivia, Nessa; Friday: Rebecca, Kevin
option(e) :-
    leads(julio, morning, wednesday),
    leads(lan, afternoon, wednesday),
    leads(olivia, morning, thursday),
    leads(nessa, afternoon, thursday),
    leads(rebecca, morning, friday),
    leads(kevin, afternoon, friday).

% Only one option can be correct
:- 2 { option(X) : option(X) }.

#show option/1.