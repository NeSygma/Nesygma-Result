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
:- assigned(j, S), not evening(S).

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

% Forbid all pairs from the options to determine which one is impossible
:- pair_j_k.
:- pair_j_m.
:- pair_j_o.
:- pair_j_p.
:- pair_m_p.

% Derive the answer based on which pair is impossible
% If pair_j_k is impossible, then option(a) is correct
option(a) :- not pair_j_k, pair_j_m, pair_j_o, pair_j_p, pair_m_p.
% If pair_j_m is impossible, then option(b) is correct
option(b) :- not pair_j_m, pair_j_k, pair_j_o, pair_j_p, pair_m_p.
% If pair_j_o is impossible, then option(c) is correct
option(c) :- not pair_j_o, pair_j_k, pair_j_m, pair_j_p, pair_m_p.
% If pair_j_p is impossible, then option(d) is correct
option(d) :- not pair_j_p, pair_j_k, pair_j_m, pair_j_o, pair_m_p.
% If pair_m_p is impossible, then option(e) is correct
option(e) :- not pair_m_p, pair_j_k, pair_j_m, pair_j_o, pair_j_p.

#show option/1.