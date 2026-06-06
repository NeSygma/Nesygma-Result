% Define the houses and time slots
% Houses: j, k, l, m, n, o, p
% Time slots: morning (1,2), afternoon (3,4,5), evening (6,7)

% Houses are shown in a sequence of 7 slots
slot(1..7).

% Time slot categories
morning(1..2).
afternoon(3..5).
evening(6..7).

% Houses
house(j). house(k). house(l). house(m). house(n). house(o). house(p).

% Assign each house to a unique slot
1 { assigned(H, S) : slot(S) } 1 :- house(H).

% Each slot has exactly one house
1 { assigned(H, S) : house(H) } 1 :- slot(S).

% Rule 1: J must be shown in the evening
evening(S) :- assigned(j, S).

% Rule 2: K cannot be shown in the morning
:- assigned(k, S), morning(S).

% Rule 3: L must be shown after K and before M
% L must be after K
:- assigned(k, SK), assigned(l, SL), SL <= SK.
% L must be before M
:- assigned(l, SL), assigned(m, SM), SM <= SL.

% Define consecutive slots
consecutive(S, S+1) :- slot(S), slot(S+1).

% Define a pair of houses shown consecutively in either order
consecutive_pair(H1, H2) :-
    assigned(H1, S1),
    assigned(H2, S2),
    consecutive(S1, S2),
    H1 != H2.

% Define the pairs from the options
pair_j_k :- consecutive_pair(j, k).
pair_j_m :- consecutive_pair(j, m).
pair_j_o :- consecutive_pair(j, o).
pair_j_p :- consecutive_pair(j, p).
pair_m_p :- consecutive_pair(m, p).

% Map the correct answer to option/1
option(a) :- pair_j_k.
option(b) :- pair_j_m.
option(c) :- pair_j_o.
option(d) :- pair_j_p.
option(e) :- pair_m_p.

#show option/1.