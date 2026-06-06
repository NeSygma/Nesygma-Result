vert(0). vert(1). vert(2). vert(3). vert(4). vert(5). vert(6). vert(7).
edge(0,1). edge(0,4).
edge(1,2). edge(1,5).
edge(2,3). edge(2,6).
edge(3,7).
edge(4,5). edge(4,6).
edge(5,7).
edge(6,7).
1 { assign(V,1), assign(V,2) } :- vert(V).
#count { V : assign(V,1) } = 4.
part1(V) :- assign(V,1).
part2(V) :- assign(V,2).
cross_edge(F,T) :- edge(F,T), part1(F), part2(T), F < T.
cross_edge(F,T) :- edge(F,T), part2(F), part1(T), F < T.
cut_size(N) :- N = #count { X : cross_edge(X) }.
#minimize { cut_size(N) }.
#show part1/1.
#show part2/1.
#show cut_size/1.
#show cross_edge/2.