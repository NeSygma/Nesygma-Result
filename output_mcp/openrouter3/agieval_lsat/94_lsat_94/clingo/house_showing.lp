% House showing problem

% Define houses
house(j). house(k). house(l). house(m). house(n). house(o). house(p).

% Define time slots (positions 1-7)
position(1..7).

% Define time periods
morning(1). morning(2).
afternoon(3). afternoon(4). afternoon(5).
evening(6). evening(7).

% Each house is shown exactly once at a unique position
1 { shown(H, P) : position(P) } 1 :- house(H).
% Each position has exactly one house
1 { shown(H, P) : house(H) } 1 :- position(P).

% Constraint 1: J must be shown in the evening
:- shown(j, P), not evening(P).

% Constraint 2: K cannot be shown in the morning
:- shown(k, P), morning(P).

% Constraint 3: L must be shown after K and before M
% We need K < L < M in the sequence
:- shown(k, Pk), shown(l, Pl), shown(m, Pm), not (Pk < Pl), not (Pl < Pm).

% Helper: define consecutive positions
consecutive(P1, P2) :- position(P1), position(P2), P2 = P1 + 1.

% Define pairs that are consecutive in either order
consecutive_pair(H1, H2) :- shown(H1, P1), shown(H2, P2), consecutive(P1, P2).
consecutive_pair(H1, H2) :- shown(H1, P1), shown(H2, P2), consecutive(P2, P1).

% For each answer choice, check if the pair can be consecutive
% A: J, K
can_be_consecutive(j, k) :- consecutive_pair(j, k).
cannot_be_consecutive(j, k) :- not can_be_consecutive(j, k).

% B: J, M
can_be_consecutive(j, m) :- consecutive_pair(j, m).
cannot_be_consecutive(j, m) :- not can_be_consecutive(j, m).

% C: J, O
can_be_consecutive(j, o) :- consecutive_pair(j, o).
cannot_be_consecutive(j, o) :- not can_be_consecutive(j, o).

% D: J, P
can_be_consecutive(j, p) :- consecutive_pair(j, p).
cannot_be_consecutive(j, p) :- not can_be_consecutive(j, p).

% E: M, P
can_be_consecutive(m, p) :- consecutive_pair(m, p).
cannot_be_consecutive(m, p) :- not can_be_consecutive(m, p).

% Map the correct answer to option/1
% The pair that CANNOT be shown consecutively in either order
option(a) :- cannot_be_consecutive(j, k).
option(b) :- cannot_be_consecutive(j, m).
option(c) :- cannot_be_consecutive(j, o).
option(d) :- cannot_be_consecutive(j, p).
option(e) :- cannot_be_consecutive(m, p).

% Show the option
#show option/1.

% Also show the schedule for debugging
#show shown/2.