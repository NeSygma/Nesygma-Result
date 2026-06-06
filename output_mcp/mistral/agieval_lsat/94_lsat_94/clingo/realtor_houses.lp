% Houses
house(j). house(k). house(l). house(m). house(n). house(o). house(p).

% Time slots (1-7)
time(1..7).

% Time periods
morning(T) :- T = 1..2.
afternoon(T) :- T = 3..5.
evening(T) :- T = 6..7.

% Each house shown exactly once at one time
1 { order(H, T) : time(T) } 1 :- house(H).

% J must be shown in the evening
:- order(j, T), not evening(T).

% K cannot be shown in the morning
:- order(k, T), morning(T).

% L must be shown after K and before M (K < L < M)
:- order(k, TK), order(l, TL), TK >= TL.  % K must be before L
:- order(l, TL), order(m, TM), TL >= TM.  % L must be before M

% Define which pairs can be consecutive
can_be_consecutive(j,k) :- order(j,TJ), order(k,TK), |TJ-TK| = 1.
can_be_consecutive(j,m) :- order(j,TJ), order(m,TM), |TJ-TM| = 1.
can_be_consecutive(j,o) :- order(j,TJ), order(o,TO), |TJ-TO| = 1.
can_be_consecutive(j,p) :- order(j,TJ), order(p,TP), |TJ-TP| = 1.
can_be_consecutive(m,p) :- order(m,TM), order(p,TP), |TM-TP| = 1.

% Map to answer choices
% If a pair CANNOT be consecutive, its option is correct
option(a) :- not can_be_consecutive(j,k).
option(b) :- not can_be_consecutive(j,m).
option(c) :- not can_be_consecutive(j,o).
option(d) :- not can_be_consecutive(j,p).
option(e) :- not can_be_consecutive(m,p).

#show option/1.