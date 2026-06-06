% Nodes
node(1). node(2). node(3). node(4). node(5). node(6).

% Source and sink
source(1). sink(6).

% Edges with capacities
edge(1,2,10). edge(1,3,8). edge(2,3,5). edge(2,4,7). edge(3,4,3). edge(3,5,9). edge(4,6,8). edge(5,6,6).

% Flow variables: flow(From,To,Flow)
{ flow(From,To,F) : F=0..Cap } :- edge(From,To,Cap).

% Flow conservation for intermediate nodes
:- node(N), N != 1, N != 6, 
   #sum{ F : flow(X,N,F) } != #sum{ F : flow(N,Y,F) }.

% Maximize total flow from source
#maximize { F : flow(1,To,F) }.

% Compute max_flow value
max_flow(F) :- F = #sum{ f : flow(1,To,f) }.

% Show results
#show flow/3.
#show max_flow/1.