% DNA Fragment Assembly Problem
% Find ordering that maximizes total overlap length

% Fragment data (lowercase for ASP constants)
frag(0,0,a). frag(0,1,t). frag(0,2,c). frag(0,3,g). frag(0,4,a). frag(0,5,t). frag(0,6,c). frag(0,7,g).
frag(1,0,c). frag(1,1,g). frag(1,2,a). frag(1,3,t). frag(1,4,c). frag(1,5,g). frag(1,6,t). frag(1,7,a).
frag(2,0,a). frag(2,1,t). frag(2,2,c). frag(2,3,g). frag(2,4,t). frag(2,5,a). frag(2,6,a). frag(2,7,c).
frag(3,0,c). frag(3,1,g). frag(3,2,t). frag(3,3,a). frag(3,4,a). frag(3,5,c). frag(3,6,g). frag(3,7,g).
frag(4,0,t). frag(4,1,a). frag(4,2,a). frag(4,3,c). frag(4,4,g). frag(4,5,g). frag(4,6,c). frag(4,7,t).
frag(5,0,a). frag(5,1,c). frag(5,2,g). frag(5,3,g). frag(5,4,c). frag(5,5,t). frag(5,6,g). frag(5,7,a).
frag(6,0,g). frag(6,1,g). frag(6,2,c). frag(6,3,t). frag(6,4,g). frag(6,5,a). frag(6,6,a). frag(6,7,a).
frag(7,0,c). frag(7,1,t). frag(7,2,g). frag(7,3,a). frag(7,4,a). frag(7,5,a). frag(7,6,t). frag(7,7,c).

% Fragment indices and lengths
frag_index(0..7).
len(I, 8) :- frag_index(I).

% Position indices for assembly order
position_index(0..7).

% Possible overlap lengths (minimum 3, maximum 8)
possible_k(I, J, K) :- frag_index(I), frag_index(J), I != J, 
                       len(I, L1), len(J, L2), 
                       K = 3..min(L1, L2).

% Check for character mismatch at position p in overlap of length K
mismatch(I, J, K) :- possible_k(I, J, K),
                     p = 0..K-1,
                     len(I, L1),
                     frag(I, L1-K+p, C1),
                     frag(J, p, C2),
                     C1 != C2.

% Valid overlap exists if no mismatch
overlap(I, J, K) :- possible_k(I, J, K), not mismatch(I, J, K).

% Maximum overlap for each pair
max_overlap(I, J, K) :- overlap(I, J, K),
                        not overlap(I, J, K1),
                        K1 > K,
                        possible_k(I, J, K1).

% Valid pair if maximum overlap exists
valid_pair(I, J) :- max_overlap(I, J, _).

% Hamiltonian path constraints
{ position(P, I) : frag_index(I) } 1 :- position_index(P).
{ position(P, I) : position_index(P) } 1 :- frag_index(I).

% Consecutive positions must have valid overlap
:- position(P, I), position(P+1, J), not valid_pair(I, J).

% Edge overlap for consecutive positions
edge_overlap(P, K) :- position(P, I), position(P+1, J), max_overlap(I, J, K).

% Maximize total overlap
#maximize { K : edge_overlap(P, K) }.

% Compute start positions for consensus sequence
start(0, 0).
start(P, S) :- position(P, I), position(P-1, J), max_overlap(J, I, K), 
               start(P-1, S0), len(J, L), S = S0 + L - K, P > 0.

% Build consensus sequence characters
consensus_char(S + C, Char) :- position(P, I), start(P, S), frag(I, C, Char).

% Assembly path order
path_order(P, I) :- position(P, I).

% Overlap details for each adjacent pair
overlap_detail(P, I, J, K, Pos1, 0) :- position(P, I), position(P+1, J), 
                                       max_overlap(I, J, K), 
                                       len(I, L), Pos1 = L - K.

% Total overlap length
total_overlap(T) :- T = #sum{ K : edge_overlap(P, K) }.

% Output directives
#show path_order/2.
#show consensus_char/2.
#show overlap_detail/6.
#show total_overlap/1.