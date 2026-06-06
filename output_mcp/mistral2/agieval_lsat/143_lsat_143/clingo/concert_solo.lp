% Base domain: band members and solo positions
member(guitarist).
member(keyboard).
member(percussion).
member(saxophonist).
member(trumpeter).
member(violinist).

% Solo positions (1 to 6)
position(1..6).

% Each member performs exactly one solo
1 { performs(M, P) : position(P) } 1 :- member(M).

% Each position is performed by exactly one member
1 { performs(M, P) : member(M) } 1 :- position(P).

% Restriction 1: The guitarist does not perform the fourth solo
:- performs(guitarist, 4).

% Restriction 2: The percussionist performs a solo before the keyboard player
:- performs(percussion, P1), performs(keyboard, P2), P1 >= P2.

% Restriction 3: The keyboard player performs after the violinist and before the guitarist
:- performs(keyboard, P2), performs(violinist, P1), P2 =< P1.
:- performs(keyboard, P2), performs(guitarist, P3), P2 >= P3.

% Restriction 4: The saxophonist performs after either the percussionist or the trumpeter, but not both
% Case 1: Saxophonist after percussion but not after trumpeter
:- performs(saxophonist, P_s), performs(percussion, P_p), P_s =< P_p.
:- performs(saxophonist, P_s), performs(trumpeter, P_t), P_s =< P_t, performs(percussion, P_p).

% Case 2: Saxophonist after trumpeter but not after percussion
:- performs(saxophonist, P_s), performs(trumpeter, P_t), P_s =< P_t.
:- performs(saxophonist, P_s), performs(percussion, P_p), P_s =< P_p, performs(trumpeter, P_t).

% Additional constraint: The violinist performs the fourth solo
performs(violinist, 4).

% Helper predicates for the options
% (A) The percussionist performs a solo before the violinist does
option_a :- performs(percussion, P), P < 4.

% (B) The trumpeter performs a solo before the violinist does
option_b :- performs(trumpeter, P), P < 4.

% (C) The trumpeter performs a solo before the guitarist does
option_c :- performs(trumpeter, P_t), performs(guitarist, P_g), P_t < P_g.

% (D) The saxophonist performs a solo before the violinist does
option_d :- performs(saxophonist, P), P < 4.

% (E) The trumpeter performs a solo before the saxophonist does
option_e :- performs(trumpeter, P_t), performs(saxophonist, P_s), P_t < P_s.

% Map the correct answer to option/1
option(a) :- option_a, not option_b, not option_c, not option_d, not option_e.
option(b) :- option_b, not option_a, not option_c, not option_d, not option_e.
option(c) :- option_c, not option_a, not option_b, not option_d, not option_e.
option(d) :- option_d, not option_a, not option_b, not option_c, not option_e.
option(e) :- option_e, not option_a, not option_b, not option_c, not option_d.

#show option/1.