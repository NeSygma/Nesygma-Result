% vertices
vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6). vertex(7). vertex(8).

% edges (undirected)
edge(1,2). edge(2,1).
edge(1,3). edge(3,1).
edge(1,4). edge(4,1).
edge(2,5). edge(5,2).
edge(3,6). edge(6,3).
edge(3,7). edge(7,3).
edge(4,8). edge(8,4).
edge(5,6). edge(6,5).
edge(6,7). edge(7,6).
edge(7,8). edge(8,7).

% choice rule: any subset of vertices
{ chosen(V) } :- vertex(V).

% independence constraint: no two chosen vertices adjacent
:- chosen(U), chosen(V), edge(U,V).

% objective: maximize number of chosen vertices
#maximize {1 : chosen(V)}.

% compute size
size(S) :- S = #count{V : chosen(V)}.

#show chosen/1.
#show size/1.