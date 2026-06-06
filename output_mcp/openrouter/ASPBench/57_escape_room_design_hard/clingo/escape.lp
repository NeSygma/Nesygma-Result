% Puzzles
puzzle(1..18).

% Room, difficulty, theme facts
room(1,r1). difficulty(1,1). theme(1,search).
room(2,r1). difficulty(2,1). theme(2,logic).
room(3,r2). difficulty(3,2). theme(3,physical).
room(4,r2). difficulty(4,2). theme(4,search).
room(5,r2). difficulty(5,2). theme(5,logic).
room(6,r1). difficulty(6,3). theme(6,search).
room(7,r1). difficulty(7,3). theme(7,logic).
room(8,r2). difficulty(8,3). theme(8,physical).
room(9,r3). difficulty(9,3). theme(9,search).
room(10,r4). difficulty(10,3). theme(10,physical).
room(11,r4). difficulty(11,4). theme(11,logic).
room(12,r3). difficulty(12,4). theme(12,search).
room(13,r3). difficulty(13,4). theme(13,logic).
room(14,r4). difficulty(14,4). theme(14,search).
room(15,r5). difficulty(15,4). theme(15,physical).
room(16,r5). difficulty(16,5). theme(16,logic).
room(17,r5). difficulty(17,5). theme(17,search).
room(18,r5). difficulty(18,5). theme(18,logic).

% Prerequisite facts (P requires Q before)
prereq_fact(2,1).
prereq_fact(3,2).
prereq_fact(4,3).
prereq_fact(5,4).
prereq_fact(6,5).
prereq_fact(7,6).
prereq_fact(8,7).
prereq_fact(9,8).
prereq_fact(10,9).
prereq_fact(11,10).
prereq_fact(12,11).
prereq_fact(13,12).
prereq_fact(14,13).
prereq_fact(15,14).
prereq_fact(16,15).
prereq_fact(17,16).
prereq_fact(18,17).

% Item requirements
requires_item(4,key_red).
requires_item(6,uv_light).
requires_item(9,key_blue).
requires_item(10,crowbar).
requires_item(12,uv_light).
requires_item(15,crowbar).
requires_item(17,uv_light).
requires_item(18,key_red).
requires_item(18,key_blue).

% Item yields
yields_item(2,key_red).
 yields_item(5,uv_light).
 yields_item(7,key_blue).
 yields_item(8,crowbar).
 yields_item(13,gear_1).
 yields_item(15,gear_2).
 yields_item(17,gear_3).

% Room adjacency (undirected)
adj(r1,r2). adj(r2,r1).
adj(r2,r3). adj(r3,r2).
adj(r3,r4). adj(r4,r3).
adj(r4,r5). adj(r5,r4).

% Helper: same or adjacent rooms
same_or_adj(R,R) :- room(_,R).
same_or_adj(R1,R2) :- adj(R1,R2).

% Positions
#const n = 18.
pos(1..n).

% Assign each puzzle to exactly one position
1 { at(P,Pos) : pos(Pos) } 1 :- puzzle(P).
% Each position occupied by exactly one puzzle
1 { at(P,Pos) : puzzle(P) } 1 :- pos(Pos).

% Ordering helper
before(P,Q) :- at(P,PosP), at(Q,PosQ), PosP < PosQ.

% Prerequisite constraint
:- prereq_fact(P,Q), not before(Q,P).

% Helper for item availability
earlier_item(P,Item) :- yields_item(Y,Item), before(Y,P).
% Item requirement constraint: required item must be yielded earlier
:- requires_item(P,Item), not earlier_item(P,Item).

% Room adjacency / same room constraint for consecutive positions
:- pos(Pos), Pos < n,
   at(P,Pos), at(Q,Pos+1),
   room(P,R1), room(Q,R2),
   not same_or_adj(R1,R2).

% Theme balance constraint for consecutive positions
:- pos(Pos), Pos < n,
   at(P,Pos), at(Q,Pos+1),
   theme(P,T), theme(Q,T).

% Difficulty curve constraint for consecutive positions (difference <=1)
:- pos(Pos), Pos < n,
   at(P,Pos), at(Q,Pos+1),
   difficulty(P,D1), difficulty(Q,D2), D1 > D2 + 1.
:- pos(Pos), Pos < n,
   at(P,Pos), at(Q,Pos+1),
   difficulty(P,D1), difficulty(Q,D2), D2 > D1 + 1.

% Show ordering as puzzle order list
order(Pos,P) :- at(P,Pos).
#show order/2.