% Define houses and time slots
house("J"). house("K"). house("L"). house("M"). house("N"). house("O"). house("P").
time_slot(morning). time_slot(afternoon). time_slot(evening).

% Define positions (1..7)
position(1..7).

% Assign houses to positions (choice rule)
1 { assigned(H, P) : house(H) } 1 :- position(P).

% Assign time slots to positions (morning: 1-2, afternoon: 3-5, evening: 6-7)
time(P, morning) :- assigned(_, P), P = 1..2.
time(P, afternoon) :- assigned(_, P), P = 3..5.
time(P, evening) :- assigned(_, P), P = 6..7.

% Constraint 1: J must be shown in the evening
:- assigned("J", P), time(P, T), T != evening.

% Constraint 2: K cannot be shown in the morning
:- assigned("K", P), time(P, morning).

% Constraint 3: L must be shown after K and before M
% Derive after(H1, H2) and before(H1, H2) from positions
after(H1, H2) :- assigned(H1, P1), assigned(H2, P2), P1 < P2.
before(H1, H2) :- assigned(H1, P1), assigned(H2, P2), P1 < P2.

% L must be after K and before M
:- not after("K", "L").
:- not before("L", "M").

% Map the correct answer to option/1
% We need to determine which option MUST be true in all valid schedules.

% Option A: K is shown in the evening
option(a) :- assigned("K", P), time(P, evening).

% Option B: L is shown in the afternoon
option(b) :- assigned("L", P), time(P, afternoon).

% Option C: L is shown in the evening
option(c) :- assigned("L", P), time(P, evening).

% Option D: M is shown in the morning
option(d) :- assigned("M", P), time(P, morning).

% Option E: M is shown in the afternoon
option(e) :- assigned("M", P), time(P, afternoon).

% Only one option can be correct
:- option(X), option(Y), X != Y.

% Show the correct option
#show option/1.