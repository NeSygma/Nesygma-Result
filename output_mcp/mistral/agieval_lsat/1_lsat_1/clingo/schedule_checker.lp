% Domains
student(george; helen; irving; kyle; lenore; nina; olivia; robert).
day(monday; tuesday; wednesday).
time(morning; afternoon).

% Base schedule facts for each option (mutually exclusive)
% Option A
schedule(monday, morning, helen) :- option(a).
schedule(monday, afternoon, robert) :- option(a).
schedule(tuesday, morning, olivia) :- option(a).
schedule(tuesday, afternoon, irving) :- option(a).
schedule(wednesday, morning, lenore) :- option(a).
schedule(wednesday, afternoon, kyle) :- option(a).

% Option B
schedule(monday, morning, irving) :- option(b).
schedule(monday, afternoon, olivia) :- option(b).
schedule(tuesday, morning, helen) :- option(b).
schedule(tuesday, afternoon, kyle) :- option(b).
schedule(wednesday, morning, nina) :- option(b).
schedule(wednesday, afternoon, lenore) :- option(b).

% Option C
schedule(monday, morning, lenore) :- option(c).
schedule(monday, afternoon, helen) :- option(c).
schedule(tuesday, morning, george) :- option(c).
schedule(tuesday, afternoon, kyle) :- option(c).
schedule(wednesday, morning, robert) :- option(c).
schedule(wednesday, afternoon, irving) :- option(c).

% Option D
schedule(monday, morning, nina) :- option(d).
schedule(monday, afternoon, helen) :- option(d).
schedule(tuesday, morning, robert) :- option(d).
schedule(tuesday, afternoon, irving) :- option(d).
schedule(wednesday, morning, olivia) :- option(d).
schedule(wednesday, afternoon, lenore) :- option(d).

% Option E
schedule(monday, morning, olivia) :- option(e).
schedule(monday, afternoon, nina) :- option(e).
schedule(tuesday, morning, irving) :- option(e).
schedule(tuesday, afternoon, helen) :- option(e).
schedule(wednesday, morning, kyle) :- option(e).
schedule(wednesday, afternoon, george) :- option(e).

% Exactly 6 students give reports (2 do not)
1 { assigned(S) : student(S) } 6.
assigned(S) :- schedule(_, _, S).

% Exactly 2 reports per day (one morning, one afternoon)
:- day(D), not 1 { schedule(D, morning, S) : student(S) } 1.
:- day(D), not 1 { schedule(D, afternoon, S) : student(S) } 1.

% George can only give a report on Tuesday
:- schedule(D, _, george), D != tuesday.

% Olivia and Robert can only give morning reports
:- schedule(_, afternoon, olivia).
:- schedule(_, afternoon, robert).

% Helper predicate: Nina gives a report on a specific day and time
nina_report(D, T) :- schedule(D, T, nina).

% Define next_day relation
next_day(monday, tuesday).
next_day(tuesday, wednesday).

% Nina constraint:
% If Nina gives a report on Monday, then Tuesday must have both Helen and Irving
:- nina_report(monday, _),
   (not schedule(tuesday, _, helen) ; not schedule(tuesday, _, irving)).

% If Nina gives a report on Tuesday, then Wednesday must have both Helen and Irving
:- nina_report(tuesday, _),
   (not schedule(wednesday, _, helen) ; not schedule(wednesday, _, irving)).

% If Nina gives a report on Wednesday, no constraint (allowed)

% Derive option(a) if the schedule for A satisfies all constraints
option(a) :-
    schedule(monday, morning, helen),
    schedule(monday, afternoon, robert),
    schedule(tuesday, morning, olivia),
    schedule(tuesday, afternoon, irving),
    schedule(wednesday, morning, lenore),
    schedule(wednesday, afternoon, kyle),
    not option(b),
    not option(c),
    not option(d),
    not option(e).

% Derive option(b) if the schedule for B satisfies all constraints
option(b) :-
    schedule(monday, morning, irving),
    schedule(monday, afternoon, olivia),
    schedule(tuesday, morning, helen),
    schedule(tuesday, afternoon, kyle),
    schedule(wednesday, morning, nina),
    schedule(wednesday, afternoon, lenore),
    not option(a),
    not option(c),
    not option(d),
    not option(e).

% Derive option(c) if the schedule for C satisfies all constraints
option(c) :-
    schedule(monday, morning, lenore),
    schedule(monday, afternoon, helen),
    schedule(tuesday, morning, george),
    schedule(tuesday, afternoon, kyle),
    schedule(wednesday, morning, robert),
    schedule(wednesday, afternoon, irving),
    not option(a),
    not option(b),
    not option(d),
    not option(e).

% Derive option(d) if the schedule for D satisfies all constraints
option(d) :-
    schedule(monday, morning, nina),
    schedule(monday, afternoon, helen),
    schedule(tuesday, morning, robert),
    schedule(tuesday, afternoon, irving),
    schedule(wednesday, morning, olivia),
    schedule(wednesday, afternoon, lenore),
    not option(a),
    not option(b),
    not option(c),
    not option(e).

% Derive option(e) if the schedule for E satisfies all constraints
option(e) :-
    schedule(monday, morning, olivia),
    schedule(monday, afternoon, nina),
    schedule(tuesday, morning, irving),
    schedule(tuesday, afternoon, helen),
    schedule(wednesday, morning, kyle),
    schedule(wednesday, afternoon, george),
    not option(a),
    not option(b),
    not option(c),
    not option(d).

% Ensure only one option is selected
:- option(X), option(Y), X != Y.

#show option/1.