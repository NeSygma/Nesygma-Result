% --- Graph G1 ---
vertex1(1..8).

red1(1;2;5;6).
blue1(3;4;7;8).

special1(1).

edge1(1,3,10). edge1(3,1,10).
edge1(1,4,20). edge1(4,1,20).
edge1(2,3,20). edge1(3,2,20).
edge1(2,4,10). edge1(4,2,10).

edge1(5,7,10). edge1(7,5,10).
edge1(5,8,20). edge1(8,5,20).
edge1(6,7,20). edge1(7,6,20).
edge1(6,8,10). edge1(8,6,10).

edge1(1,5,30). edge1(5,1,30).
edge1(2,6,30). edge1(6,2,30).
edge1(3,7,40). edge1(7,3,40).
edge1(4,8,40). edge1(8,4,40).

% --- Graph G2 ---
vertex2(a;b;c;d;e;f;g;h).

red2(a;b;e;f).
blue2(c;d;g;h).

special2(a).

edge2(a,c,10). edge2(c,a,10).
edge2(a,d,20). edge2(d,a,20).
edge2(b,c,20). edge2(c,b,20).
edge2(b,d,10). edge2(d,b,10).

edge2(e,g,10). edge2(g,e,10).
edge2(e,h,20). edge2(h,e,20).
edge2(f,g,20). edge2(g,f,20).
edge2(f,h,10). edge2(h,f,10).

edge2(a,e,30). edge2(e,a,30).
edge2(b,f,30). edge2(f,b,30).
edge2(c,g,40). edge2(g,c,40).
edge2(d,h,40). edge2(h,d,40).

% --- Mapping ---
% Generate possible mappings
1 { mapping(V1, V2) : vertex2(V2) } 1 :- vertex1(V1).
1 { mapping(V1, V2) : vertex1(V1) } 1 :- vertex2(V2).

% --- Constraints ---
% Color preservation
:- vertex1(V1), red1(V1), mapping(V1, V2), not red2(V2).
:- vertex1(V1), blue1(V1), mapping(V1, V2), not blue2(V2).

% Special vertex preservation
:- vertex1(V1), special1(V1), mapping(V1, V2), not special2(V2).
:- vertex2(V2), special2(V2), not special1(V1), mapping(V1, V2).

% Edge and weight preservation
:- edge1(U1, V1, W), mapping(U1, U2), mapping(V1, V2),
   not edge2(U2, V2, W), not edge2(V2, U2, W).
:- edge2(U2, V2, W), not edge1(U1, V1, W),
   mapping(U1, U2), mapping(V1, V2).

% Forbidden triangle: no 3-cycle involving a special vertex with total weight 60
:- special2(S),
   edge2(S, A, W1), edge2(A, S, W1),
   edge2(S, B, W2), edge2(B, S, W2),
   edge2(A, B, W3), edge2(B, A, W3),
   W1 + W2 + W3 = 60.

% --- Output ---
is_isomorphic :- mapping(_, _).

% Show the mapping and isomorphism result
#show mapping/2.
#show is_isomorphic/0.