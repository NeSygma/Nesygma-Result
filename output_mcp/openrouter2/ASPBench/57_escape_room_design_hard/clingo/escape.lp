% Puzzle data
puzzle(1). puzzle(2). puzzle(3). puzzle(4). puzzle(5). puzzle(6). puzzle(7). puzzle(8). puzzle(9). puzzle(10). puzzle(11). puzzle(12). puzzle(13). puzzle(14). puzzle(15). puzzle(16). puzzle(17). puzzle(18).

room(1,r1). room(2,r1). room(3,r2). room(4,r2). room(5,r2). room(6,r1). room(7,r1). room(8,r2). room(9,r3). room(10,r4). room(11,r4). room(12,r3). room(13,r3). room(14,r4). room(15,r5). room(16,r5). room(17,r5). room(18,r5).

difficulty(1,1). difficulty(2,1). difficulty(3,2). difficulty(4,2). difficulty(5,2). difficulty(6,3). difficulty(7,3). difficulty(8,3). difficulty(9,3). difficulty(10,3). difficulty(11,4). difficulty(12,4). difficulty(13,4). difficulty(14,4). difficulty(15,4). difficulty(16,5). difficulty(17,5). difficulty(18,5).

theme(1,search). theme(2,logic). theme(3,physical). theme(4,search). theme(5,logic). theme(6,search). theme(7,logic). theme(8,physical). theme(9,search). theme(10,physical). theme(11,logic). theme(12,search). theme(13,logic). theme(14,search). theme(15,physical). theme(16,logic). theme(17,search). theme(18,logic).

% prerequisites
prereq(2,1). prereq(3,2). prereq(4,3). prereq(5,4). prereq(6,5). prereq(7,6). prereq(8,7). prereq(9,8). prereq(10,9). prereq(11,10). prereq(12,11). prereq(13,12). prereq(14,13). prereq(15,14). prereq(16,15). prereq(17,16). prereq(18,17).

% requires items
requires(4,key_red). requires(6,uv_light). requires(9,key_blue). requires(10,crowbar). requires(12,uv_light). requires(15,crowbar). requires(17,uv_light). requires(18,key_red). requires(18,key_blue).

% yields items
yields(2,key_red). yields(5,uv_light). yields(7,key_blue). yields(8,crowbar). yields(13,gear_1). yields(15,gear_2). yields(17,gear_3).

% positions
pos(1..18).

% each position has exactly one puzzle
1 { puzzle_at_pos(Pos,P) : puzzle(P) } 1 :- pos(Pos).

% each puzzle appears exactly once
1 { puzzle_at_pos(Pos,P) : pos(Pos) } 1 :- puzzle(P).

% derive room, difficulty, theme at positions
room_at_pos(Pos,Room) :- puzzle_at_pos(Pos,P), room(P,Room).
diff_at_pos(Pos,D) :- puzzle_at_pos(Pos,P), difficulty(P,D).
theme_at_pos(Pos,Th) :- puzzle_at_pos(Pos,P), theme(P,Th).

% adjacency facts
adjacent(r1,r2). adjacent(r2,r1). adjacent(r2,r3). adjacent(r3,r2). adjacent(r3,r4). adjacent(r4,r3). adjacent(r4,r5). adjacent(r5,r4).
adjacent(R,R) :- room(R,_).

% constraints
% prerequisite order
:- prereq(P,Q), puzzle_at_pos(PosP,P), puzzle_at_pos(PosQ,Q), PosP <= PosQ.

% item requirement: at least one puzzle yields the item before P
:- requires(P,I), puzzle_at_pos(PosP,P), not { puzzle_at_pos(PosY,Y) : yields(Y,I), PosY < PosP } > 0.

% room adjacency for consecutive positions
:- pos(Pos), Pos < 18, puzzle_at_pos(Pos,P), puzzle_at_pos(Pos+1,P2), room_at_pos(Pos,RoomP), room_at_pos(Pos+1,RoomP2), not adjacent(RoomP,RoomP2).

% theme balance
:- pos(Pos), Pos < 18, theme_at_pos(Pos,Th), theme_at_pos(Pos+1,Th).

% difficulty curve
:- pos(Pos), Pos < 18, diff_at_pos(Pos,D1), diff_at_pos(Pos+1,D2), D1 > D2+1.
:- pos(Pos), Pos < 18, diff_at_pos(Pos,D1), diff_at_pos(Pos+1,D2), D2 > D1+1.

% all constraints satisfied atom
all_constraints_satisfied.

% puzzle details facts
puzzle_detail(1,r1,1,search,[],[],[]).
puzzle_detail(2,r1,1,logic,[1],[],[key_red]).
puzzle_detail(3,r2,2,physical,[2],[],[]).
puzzle_detail(4,r2,2,search,[3],[key_red],[]).
puzzle_detail(5,r2,2,logic,[4],[],[uv_light]).
puzzle_detail(6,r1,3,search,[5],[uv_light],[]).
puzzle_detail(7,r1,3,logic,[6],[],[key_blue]).
puzzle_detail(8,r2,3,physical,[7],[],[crowbar]).
puzzle_detail(9,r3,3,search,[8],[key_blue],[]).
puzzle_detail(10,r4,3,physical,[9],[crowbar],[]).
puzzle_detail(11,r4,4,logic,[10],[],[]).
puzzle_detail(12,r3,4,search,[11],[uv_light],[]).
puzzle_detail(13,r3,4,logic,[12],[],[gear_1]).
puzzle_detail(14,r4,4,search,[13],[],[]).
puzzle_detail(15,r5,4,physical,[14],[crowbar],[gear_2]).
puzzle_detail(16,r5,5,logic,[15],[],[]).
puzzle_detail(17,r5,5,search,[16],[uv_light],[gear_3]).
puzzle_detail(18,r5,5,logic,[17],[key_red,key_blue],[]).

#show puzzle_at_pos/2.
#show room_at_pos/2.
#show diff_at_pos/2.
#show theme_at_pos/2.
#show all_constraints_satisfied.
#show puzzle_detail/7.