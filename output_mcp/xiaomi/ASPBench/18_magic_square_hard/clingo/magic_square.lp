% Domain definitions
row(1..4).
col(1..4).
val(1..16).

% Each cell gets exactly one value from 1-16
{ cell(R, C, V) : val(V) } 1 :- row(R), col(C).

% Each value used exactly once
1 { cell(R, C, V) : row(R), col(C) } 1 :- val(V).

% Magic sum for all rows = 34
:- row(R), 34 != #sum{ V, C : cell(R, C, V), col(C) }.

% Magic sum for all columns = 34
:- col(C), 34 != #sum{ V, R : cell(R, C, V), row(R) }.

% Main diagonal (top-left to bottom-right) sum = 34
:- 34 != #sum{ V, R : cell(R, R, V), row(R) }.

% Anti-diagonal (top-right to bottom-left) sum = 34
:- 34 != #sum{ V, R : cell(R, 5-R, V), row(R) }.

% Symmetrical pairs: opposite cells sum to 17
% Cell (r,c) opposite to (5-r, 5-c)
:- row(R), col(C), cell(R, C, V1), cell(5-R, 5-C, V2), V1 + V2 != 17.

% Quadrant definitions
quadrant(tl, 1, 1). quadrant(tl, 1, 2). quadrant(tl, 2, 1). quadrant(tl, 2, 2).
quadrant(tr, 1, 3). quadrant(tr, 1, 4). quadrant(tr, 2, 3). quadrant(tr, 2, 4).
quadrant(bl, 3, 1). quadrant(bl, 3, 2). quadrant(bl, 4, 1). quadrant(bl, 4, 2).
quadrant(br, 3, 3). quadrant(br, 3, 4). quadrant(br, 4, 3). quadrant(br, 4, 4).

% Each quadrant sums to 34
:- quadrant(Q, R, C), Q != Q2, quadrant(Q2, _, _), 
   34 != #sum{ V, R2, C2 : cell(R2, C2, V), quadrant(Q, R2, C2) }.

% Small primes definition
small_prime(2). small_prime(3). small_prime(5). small_prime(7).

% Corner cells
corner(1, 1). corner(1, 4). corner(4, 1). corner(4, 4).

% Small primes forbidden in corners
:- corner(R, C), cell(R, C, V), small_prime(V).

% Output
#show cell/3.