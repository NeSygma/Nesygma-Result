% Define the time steps (puzzle order positions)
time(1..18).

% Puzzle specifications
puzzle(1). room(1,"R1"). difficulty(1,1). theme(1,"search").
puzzle(2). room(2,"R1"). difficulty(2,1). theme(2,"logic").
puzzle(3). room(3,"R2"). difficulty(3,2). theme(3,"physical").
puzzle(4). room(4,"R2"). difficulty(4,2). theme(4,"search").
puzzle(5). room(5,"R2"). difficulty(5,2). theme(5,"logic").
puzzle(6). room(6,"R1"). difficulty(6,3). theme(6,"search").
puzzle(7). room(7,"R1"). difficulty(7,3). theme(7,"logic").
puzzle(8). room(8,"R2"). difficulty(8,3). theme(8,"physical").
puzzle(9). room(9,"R3"). difficulty(9,3). theme(9,"search").
puzzle(10). room(10,"R4"). difficulty(10,3). theme(10,"physical").
puzzle(11). room(11,"R4"). difficulty(11,4). theme(11,"logic").
puzzle(12). room(12,"R3"). difficulty(12,4). theme(12,"search").
puzzle(13). room(13,"R3"). difficulty(13,4). theme(13,"logic").
puzzle(14). room(14,"R4"). difficulty(14,4). theme(14,"search").
puzzle(15). room(15,"R5"). difficulty(15,4). theme(15,"physical").
puzzle(16). room(16,"R5"). difficulty(16,5). theme(16,"logic").
puzzle(17). room(17,"R5"). difficulty(17,5). theme(17,"search").
puzzle(18). room(18,"R5"). difficulty(18,5). theme(18,"logic").

% Prerequisites for each puzzle
prerequisite(2,1).
prerequisite(3,2).
prerequisite(4,3).
prerequisite(5,4).
prerequisite(6,5).
prerequisite(7,6).
prerequisite(8,7).
prerequisite(9,8).
prerequisite(10,9).
prerequisite(11,10).
prerequisite(12,11).
prerequisite(13,12).
prerequisite(14,13).
prerequisite(15,14).
prerequisite(16,15).
prerequisite(17,16).
prerequisite(18,17).

% Required items for each puzzle
required_item(4,"key_red").
required_item(18,"key_red").
required_item(9,"key_blue").
required_item(18,"key_blue").
required_item(6,"uv_light").
required_item(12,"uv_light").
required_item(17,"uv_light").
required_item(10,"crowbar").
required_item(15,"crowbar").

% Items yielded by each puzzle
yields_item(2,"key_red").
yields_item(5,"uv_light").
yields_item(7,"key_blue").
yields_item(8,"crowbar").
yields_item(13,"gear_1").
yields_item(15,"gear_2").
yields_item(17,"gear_3").

% Define rooms and their adjacency
adjacent("R1","R2"). adjacent("R2","R1").
adjacent("R2","R3"). adjacent("R3","R2").
adjacent("R3","R4"). adjacent("R4","R3").
adjacent("R4","R5"). adjacent("R5","R4").

% Define items
item("key_red"). item("key_blue"). item("uv_light"). item("crowbar"). item("gear_1"). item("gear_2"). item("gear_3").

% Generate a possible ordering of puzzles
1 { order(T, P) : puzzle(P) } 1 :- time(T).

% Ensure each puzzle appears exactly once in the ordering
:- puzzle(P), time(T1), time(T2), T1 != T2, order(T1, P), order(T2, P).

% Prerequisite constraint: A puzzle can only be solved after all its prerequisites
:- order(T, P), prerequisite(P, Pr), not solved_before(T, Pr).
solved_before(T, Pr) :- order(Tp, Pr), Tp < T.

% Item requirement constraint: A puzzle can only be solved if the player has all required items
:- order(T, P), required_item(P, Item), not has_item(T, Item).
has_item(T, Item) :- order(Tp, Pp), Tp < T, yields_item(Pp, Item).
has_item(T, Item) :- has_item(T-1, Item), time(T), T > 1.

% Room adjacency constraint: The room of puzzle N and puzzle N+1 must be the same or adjacent
:- order(T, P1), order(T+1, P2), T < 18, room(P1, R1), room(P2, R2), not (R1 == R2 ; adjacent(R1, R2)).

% Theme balance constraint: No two consecutive puzzles can have the same theme
:- order(T, P1), order(T+1, P2), T < 18, theme(P1, Theme), theme(P2, Theme).

% Difficulty curve constraint: The difficulty difference between consecutive puzzles must be at most 1
:- order(T, P1), order(T+1, P2), T < 18, difficulty(P1, D1), difficulty(P2, D2), abs(D1 - D2) > 1.

% Helper predicates for room, difficulty, and theme
room(P, R) :- room(P, R).
difficulty(P, D) :- difficulty(P, D).
theme(P, Th) :- theme(P, Th).

% Define derived predicates for output
puzzle_order(P) :- order(T, P).
room_progression(R) :- order(T, P), room(P, R).
difficulty_progression(D) :- order(T, P), difficulty(P, D).
theme_progression(Th) :- order(T, P), theme(P, Th).
all_constraints_satisfied :- not constraint_violated.
constraint_violated :- order(T, P), prerequisite(P, Pr), not solved_before(T, Pr).
constraint_violated :- order(T, P), required_item(P, Item), not has_item(T, Item).
constraint_violated :- order(T, P1), order(T+1, P2), T < 18, room(P1, R1), room(P2, R2), not (R1 == R2 ; adjacent(R1, R2)).
constraint_violated :- order(T, P1), order(T+1, P2), T < 18, theme(P1, Theme), theme(P2, Theme).
constraint_violated :- order(T, P1), order(T+1, P2), T < 18, difficulty(P1, D1), difficulty(P2, D2), abs(D1 - D2) > 1.

% Show the solution
#show order/2.
#show puzzle_order/1.
#show room_progression/1.
#show difficulty_progression/1.
#show theme_progression/1.
#show all_constraints_satisfied/0.