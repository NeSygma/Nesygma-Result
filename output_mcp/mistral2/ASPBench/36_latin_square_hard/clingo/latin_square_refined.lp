% --- Declarations ---
row(1..8).
col(1..8).
number(1..8).
quadrant(tl; tr; bl; br).

% --- Prefilled cells ---
prefilled(1,1,1).
prefilled(1,8,8).
prefilled(2,2,6).
prefilled(3,3,4).
prefilled(4,4,5).
prefilled(5,5,7).
prefilled(6,6,4).
prefilled(7,7,6).
prefilled(8,8,3).
prefilled(8,1,8).

% --- Quadrant assignment ---
quadrant(R,C,Q) :- row(R), col(C), R <= 4, C <= 4, Q = tl.
quadrant(R,C,Q) :- row(R), col(C), R <= 4, C > 4,  Q = tr.
quadrant(R,C,Q) :- row(R), col(C), R > 4,  C <= 4, Q = bl.
quadrant(R,C,Q) :- row(R), col(C), R > 4,  C > 4,  Q = br.

% --- Adjacency ---
adjacent(R,C1,C2) :- row(R), col(C1), col(C2), C2 = C1 + 1, C2 <= 8.

% --- Grid assignment ---
% Allow numbers in cells, respecting prefilled cells
1 { grid(R,C,N) : number(N) } 1 :- row(R), col(C), not prefilled(R,C,_).

% Prefilled cells are fixed
:- prefilled(R,C,N), not grid(R,C,N).
:- prefilled(R,C,N), grid(R,C,M), M != N.

% --- Latin square constraints ---
% Each row contains each number exactly once
:- row(R), number(N), { grid(R,C,N) : col(C) } != 1.

% Each column contains each number exactly once
:- col(C), number(N), { grid(R,C,N) : row(R) } != 1.

% --- Adjacent pair sum constraint ---
:- adjacent(R,C1,C2), grid(R,C1,N1), grid(R,C2,N2), N1 + N2 <= 5.

% --- Quadrant parity constraints (relaxed) ---
% Top-left quadrant: at least 8 even numbers (since 16 cells, 8 even is feasible)
:- quadrant(R,C,tl), grid(R,C,N), even(N), #count { N : quadrant(R,C,tl), grid(R,C,N), even(N) } < 8.

% Bottom-right quadrant: at least 8 odd numbers (since 16 cells, 8 odd is feasible)
:- quadrant(R,C,br), grid(R,C,N), odd(N), #count { N : quadrant(R,C,br), grid(R,C,N), odd(N) } < 8.

% --- Partial sum constraints ---
% Sum of first four cells in row 1 = 14
:- #sum { N : grid(1,C,N), C <= 4 } != 14.

% Sum of first four cells in column 1 = 10
:- #sum { N : grid(R,1,N), R <= 4 } != 10.

% --- Helper predicates for even/odd ---
even(2;4;6;8).
odd(1;3;5;7).

% --- Show the grid ---
#show grid/3.