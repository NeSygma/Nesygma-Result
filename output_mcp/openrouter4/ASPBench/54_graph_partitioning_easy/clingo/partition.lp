%% Balanced Graph Partitioning
%% Vertices: 0..7, partition into two sets of 4, minimize crossing edges

%% Domain
vertex(0..7).
edge(0,1). edge(0,4).
edge(1,2). edge(1,5).
edge(2,3). edge(2,6).
edge(3,7).
edge(4,5). edge(4,6).
edge(5,7).
edge(6,7).

%% Make edges symmetric for easier checking
edge(Y,X) :- edge(X,Y).

%% Each vertex assigned to exactly one partition (1 or 2)
1 { assign(V,1); assign(V,2) } 1 :- vertex(V).

%% Exactly 4 vertices in partition 1
:- #count { V : assign(V,1) } != 4.
%% Exactly 4 vertices in partition 2
:- #count { V : assign(V,2) } != 4.

%% Count crossing edges
crossing(X,Y) :- edge(X,Y), X < Y, assign(X,P1), assign(Y,P2), P1 != P2.

%% Minimize crossing edges
#minimize { 1,X,Y : crossing(X,Y) }.

#show assign/2.
#show crossing/2.
#show cut_size/1.

%% Derive cut size
cut_size(N) :- N = #count { X,Y : crossing(X,Y) }.