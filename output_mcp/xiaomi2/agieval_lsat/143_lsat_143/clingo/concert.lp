% Members
member(guitarist).
member(keyboard).
member(percussionist).
member(saxophonist).
member(trumpeter).
member(violinist).

% Positions
position(1..6).

% Each member assigned to exactly one position
1 { assign(M, P) : position(P) } 1 :- member(M).

% Each position assigned exactly one member
1 { assign(M, P) : member(M) } 1 :- position(P).

% Constraint 1: guitarist not at 4
:- assign(guitarist, 4).

% Constraint 2: percussionist before keyboard
:- assign(percussionist, P1), assign(keyboard, P2), P1 >= P2.

% Constraint 3: keyboard after violinist and before guitarist
:- assign(violinist, P1), assign(keyboard, P2), P1 >= P2.
:- assign(keyboard, P2), assign(guitarist, P3), P2 >= P3.

% Constraint 4: saxophonist after either percussionist or trumpeter but not both
:- assign(saxophonist, S), assign(percussionist, P), assign(trumpeter, T), P < S, T < S.
:- assign(saxophonist, S), assign(percussionist, P), assign(trumpeter, T), P >= S, T >= S.

% Violinist performs the fourth solo
assign(violinist, 4).

% Define truth of each statement in the current ordering
true_a :- assign(percussionist, P1), assign(violinist, P2), P1 < P2.
true_b :- assign(trumpeter, P1), assign(violinist, P2), P1 < P2.
true_c :- assign(trumpeter, P1), assign(guitarist, P2), P1 < P2.
true_d :- assign(saxophonist, P1), assign(violinist, P2), P1 < P2.
true_e :- assign(trumpeter, P1), assign(saxophonist, P2), P1 < P2.

% Minimize the number of true statements among A-E
#minimize { 1@1 : true_a; 1@1 : true_b; 1@1 : true_c; 1@1 : true_d; 1@1 : true_e }.

% Map the correct answer to option/1
option(a) :- not true_a.
option(b) :- not true_b.
option(c) :- not true_c.
option(d) :- not true_d.
option(e) :- not true_e.

#show option/1.
#show assign/2.