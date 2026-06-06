% Vertices and positions
vertex(0). vertex(1). vertex(2). vertex(3). vertex(4). vertex(5).
position(0). position(1). position(2). position(3). position(4). position(5).

% Edge facts
edge(0,1). edge(0,2).
edge(1,2). edge(1,3). edge(1,4).
edge(2,1). edge(2,3). edge(2,4).
edge(3,4). edge(3,5).
edge(4,3). edge(4,5).

% Place each vertex at exactly one position
1 { place(V,P) : position(P) } 1 :- vertex(V), position(P).
1 { place(V,P) : vertex(V) } 1 :- position(P), vertex(V).

% Start and end positions fixed
place(0,0). place(5,5).

% Consecutive positions must follow an edge
:- place(V,0), place(U,1), not edge(V,U).
:- place(V,1), place(U,2), not edge(V,U).
:- place(V,2), place(U,3), not edge(V,U).
:- place(V,3), place(U,4), not edge(V,U).
:- place(V,4), place(U,5), not edge(V,U).

% Define a path atom capturing the full sequence
path(V1,V2,V3,V4,V5,V6) :- 
    place(0,V1), place(1,V2), place(2,V3), place(3,V4), place(4,V5), place(5,V6).

% Show the paths
#show path/6.