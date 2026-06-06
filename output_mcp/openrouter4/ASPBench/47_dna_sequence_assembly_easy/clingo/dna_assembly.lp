%% DNA Fragment Assembly
%% Maximize total overlap length

%% Fragment indices
fragment(0..7).
all_fragments(0..7).

%% Fragment sequences (nucleotide at each position 0..7)
nucleotide(0,0,a). nucleotide(0,1,t). nucleotide(0,2,c). nucleotide(0,3,g). 
nucleotide(0,4,a). nucleotide(0,5,t). nucleotide(0,6,c). nucleotide(0,7,g).

nucleotide(1,0,c). nucleotide(1,1,g). nucleotide(1,2,a). nucleotide(1,3,t). 
nucleotide(1,4,c). nucleotide(1,5,g). nucleotide(1,6,t). nucleotide(1,7,a).

nucleotide(2,0,a). nucleotide(2,1,t). nucleotide(2,2,c). nucleotide(2,3,g). 
nucleotide(2,4,t). nucleotide(2,5,a). nucleotide(2,6,a). nucleotide(2,7,c).

nucleotide(3,0,c). nucleotide(3,1,g). nucleotide(3,2,t). nucleotide(3,3,a). 
nucleotide(3,4,a). nucleotide(3,5,c). nucleotide(3,6,g). nucleotide(3,7,g).

nucleotide(4,0,t). nucleotide(4,1,a). nucleotide(4,2,a). nucleotide(4,3,c). 
nucleotide(4,4,g). nucleotide(4,5,g). nucleotide(4,6,c). nucleotide(4,7,t).

nucleotide(5,0,a). nucleotide(5,1,c). nucleotide(5,2,g). nucleotide(5,3,g). 
nucleotide(5,4,c). nucleotide(5,5,t). nucleotide(5,6,g). nucleotide(5,7,a).

nucleotide(6,0,g). nucleotide(6,1,g). nucleotide(6,2,c). nucleotide(6,3,t). 
nucleotide(6,4,g). nucleotide(6,5,a). nucleotide(6,6,a). nucleotide(6,7,a).

nucleotide(7,0,c). nucleotide(7,1,t). nucleotide(7,2,g). nucleotide(7,3,a). 
nucleotide(7,4,a). nucleotide(7,5,a). nucleotide(7,6,t). nucleotide(7,7,c).

frag_len(8).  %% All fragments have length 8

%% position in fragment
position(0..7).

%% Possible overlap lengths (minimum 3, maximum 8)
overlap_len(3..8).

%% Check if fragment I can precede fragment J with overlap length K
%% The last K positions of I must match the first K positions of J
valid_overlap(I, J, K) :-
    fragment(I), fragment(J), I != J,
    overlap_len(K),
    frag_len(L),
    #count{ O : position(O), O < K, 
            nucleotide(I, L-K+O, N), nucleotide(J, O, N) } = K.

%% For each ordered pair (I,J), find the maximum valid overlap length
max_overlap(I, J, K) :- 
    valid_overlap(I, J, K),
    not valid_overlap(I, J, K+1),
    fragment(I), fragment(J), I != J.

%% For pairs with no overlap >= 3, overlap is 0
no_overlap(I, J) :- fragment(I), fragment(J), I != J,
    not valid_overlap(I, J, _).

%% Maximum overlap is 0 when no valid overlap exists
max_overlap(I, J, 0) :- no_overlap(I, J).

%% --- Assembly (Hamiltonian Path) ---

%% Each fragment appears exactly once in the assembly
1 { position_in_path(F, P) : P = 1..8 } 1 :- fragment(F).
1 { position_in_path(F, P) : fragment(F) } 1 :- P = 1..8.

%% Adjacent pairs in the path
adjacent(I, J) :- 
    position_in_path(I, P), 
    position_in_path(J, P+1),
    I != J.

%% Each adjacent pair must have a valid overlap (at least 3)
:- adjacent(I, J), max_overlap(I, J, K), K < 3.

%% Total overlap is the sum of overlaps between adjacent fragments
total_overlap(T) :- 
    T = #sum { K, I, J : adjacent(I, J), max_overlap(I, J, K) }.

%% Print debug info
assembly_order(I, J) :- adjacent(I, J).

%% Maximize total overlap
#maximize { T : total_overlap(T) }.

#show assembly_order/2.
#show total_overlap/1.
#show max_overlap/3.
#show position_in_path/2.