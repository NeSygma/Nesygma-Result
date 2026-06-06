% Latin Square Puzzle with Additional Constraints

% Domain declarations as facts
row(1). row(2). row(3). row(4). row(5). row(6). row(7). row(8).
col(1). col(2). col(3). col(4). col(5). col(6). col(7). col(8).
value(1). value(2). value(3). value(4). value(5). value(6). value(7). value(8).

% Pre-filled cells (1-indexed as per problem)
grid(1,1,1).
grid(1,8,8).
grid(2,2,6).
grid(3,3,4).
grid(4,4,5).
grid(5,5,7).
grid(6,6,4).
grid(7,7,6).
grid(8,8,3).
grid(8,1,8).

% Latin Square Constraints
% Each row must contain each value exactly once
1 { grid(r,c,v) : col(c) } 1 :- row(r), value(v).

% Each column must contain each value exactly once  
1 { grid(r,c,v) : row(r) } 1 :- col(c), value(v).

% Each cell must have exactly one value
1 { grid(r,c,v) : value(v) } 1 :- row(r), col(c).

% Adjacent Pair Sum Constraint: sum > 5 for horizontally adjacent cells
% Define adjacent column pairs
adjacent(1,2). adjacent(2,3). adjacent(3,4). adjacent(4,5).
adjacent(5,6). adjacent(6,7). adjacent(7,8).

:- grid(r,c1,v1), grid(r,c2,v2), adjacent(c1,c2), v1 + v2 <= 5.

% Quadrant Parity Constraints
% Define even and odd numbers
even(2). even(4). even(6). even(8).
odd(1). odd(3). odd(5). odd(7).

% Top-left quadrant (rows 1-4, cols 1-4) must have exactly 8 even numbers
even_count_top_left(N) :- N = #count{ r,c : grid(r,c,v), even(v), r <= 4, c <= 4 }.
:- even_count_top_left(N), N != 8.

% Bottom-right quadrant (rows 5-8, cols 5-8) must have exactly 8 odd numbers
odd_count_bottom_right(N) :- N = #count{ r,c : grid(r,c,v), odd(v), r >= 5, c >= 5 }.
:- odd_count_bottom_right(N), N != 8.

% Partial Sum Constraints
% Row 1 first four cells sum to 14
% Use helper predicates to compute the sum
row1_sum(N) :- N = #sum{ v,1,1 : grid(1,1,v) } + #sum{ v,1,2 : grid(1,2,v) } + #sum{ v,1,3 : grid(1,3,v) } + #sum{ v,1,4 : grid(1,4,v) }.
:- row1_sum(N), N != 14.

% Column 1 first four cells sum to 10
col1_sum(N) :- N = #sum{ v,1,1 : grid(1,1,v) } + #sum{ v,2,1 : grid(2,1,v) } + #sum{ v,3,1 : grid(3,1,v) } + #sum{ v,4,1 : grid(4,1,v) }.
:- col1_sum(N), N != 10.

% Output the solution
#show grid/3.
#show even_count_top_left/1.
#show odd_count_bottom_right/1.
#show row1_sum/1.
#show col1_sum/1.