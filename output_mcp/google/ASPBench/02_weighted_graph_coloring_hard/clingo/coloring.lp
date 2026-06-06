% Vertices and Colors
vertex(1..36).
color(1..5).

% Weights
weight(V, 10) :- V >= 1, V <= 5.
weight(V, 3) :- V >= 6, V <= 15.
weight(V, 5) :- V >= 16, V <= 25.
weight(V, 7) :- V >= 26, V <= 36.

% Edges
edge(1,2). edge(1,3). edge(1,4). edge(1,5). edge(2,3). edge(2,4). edge(2,5). edge(3,4). edge(3,5). edge(4,5).
edge(6,7). edge(7,8). edge(8,9). edge(9,10). edge(10,11). edge(11,12). edge(12,13). edge(13,14). edge(14,15). edge(15,6).
edge(6,9). edge(7,10). edge(8,11). edge(9,12). edge(10,13). edge(11,14). edge(12,15). edge(13,6). edge(14,7). edge(15,8).
edge(6,1). edge(6,2). edge(9,2). edge(9,3). edge(12,3). edge(12,4). edge(15,4). edge(15,5).
edge(16,17). edge(17,18). edge(18,19). edge(19,20). edge(21,22). edge(22,23). edge(23,24). edge(24,25).
edge(16,21). edge(17,22). edge(18,23). edge(19,24). edge(20,25). edge(16,22). edge(17,23). edge(18,24). edge(19,25).
edge(16,1). edge(20,5). edge(18,8). edge(23,13).
edge(26,27). edge(27,28). edge(28,29). edge(29,30). edge(30,31). edge(31,32). edge(32,33). edge(33,34). edge(34,35). edge(35,36). edge(36,26).
edge(26,29). edge(27,30). edge(28,31). edge(29,32). edge(30,33). edge(31,34). edge(32,35). edge(33,36). edge(34,26). edge(35,27). edge(36,28).
edge(26,1). edge(26,5). edge(31,3). edge(28,19). edge(33,24).
edge(V, U) :- edge(U, V).

% Coloring
1 { color_of(V, C) : color(C) } 1 :- vertex(V).

% Constraints
:- edge(U, V), color_of(U, C), color_of(V, C).
used_color(C) :- color_of(V, C).
:- color(C), not used_color(C).

% Cost
weighted_cost(S) :- S = #sum { C*W, V : color_of(V, C), weight(V, W) }.
:- weighted_cost(S), S > 850.

% Output
#show color_of/2.
#show weighted_cost/1.