% --- Declare the vertices ---
vertex(0..5).

% --- Declare the edges ---
edge(0, 1).
edge(0, 2).
edge(1, 3).
edge(2, 3).
edge(2, 4).
edge(3, 5).
edge(4, 5).
edge(1, 5).

% --- Choice rule: Select vertices for the cover ---
{ selected(V) : vertex(V) }.

% --- Ensure every edge is covered ---
covered(U, V) :- edge(U, V), selected(U).
covered(U, V) :- edge(U, V), selected(V).

% --- Ensure all edges are covered ---
:- edge(U, V), not covered(U, V).

% --- Minimize the number of selected vertices ---
#minimize { V : selected(V) }.

% --- Show the selected vertices and cover size ---
#show selected/1.
#show cover_size/1.