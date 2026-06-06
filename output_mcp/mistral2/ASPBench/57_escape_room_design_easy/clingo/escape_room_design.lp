% --- Domain ---
puzzle(1..6).

% Difficulty levels: 1 (easy), 2 (medium), 3 (hard)
difficulty(1,1). difficulty(2,1). difficulty(3,2). difficulty(4,2). difficulty(5,3). difficulty(6,3).

% Prerequisites (P requires Q)
prerequisite(2,1).
prerequisite(3,2).
prerequisite(3,4).
prerequisite(4,1).
prerequisite(5,3).
prerequisite(6,5).

% --- Choice Rule: Assign positions to puzzles ---
1 { position(P, Pos) : Pos = 1..6 } 1 :- puzzle(P).

% --- Ensure unique positions ---
:- position(P1, Pos), position(P2, Pos), P1 != P2.

% --- Satisfy prerequisites: Q must come before P if prerequisite(P, Q) ---
:- prerequisite(P, Q), position(P, PosP), position(Q, PosQ), PosP < PosQ.

% --- Difficulty progression: Track sequence of difficulties ---
difficulty_progression(D1, D2) :-
    position(P1, Pos), position(P2, Pos+1),
    difficulty(P1, D1), difficulty(P2, D2).

% --- All dependencies are satisfied if no constraint is violated ---
satisfied :- not violated.
violated :- prerequisite(P, Q), position(P, PosP), position(Q, PosQ), PosP < PosQ.

% --- Output ---
#show puzzle_order/1.
#show difficulty_progression/2.
#show dependencies_satisfied/0.
#show puzzle_details/3.

% Helper to show puzzle_order as a list
puzzle_order(P) :- position(P, _).

% Helper to show difficulty_progression as a list
% (Already handled by difficulty_progression/2)

% Helper to show dependencies_satisfied
dependencies_satisfied :- not violated.

% Helper to show puzzle_details
puzzle_details(P, D, Prereqs) :-
    puzzle(P),
    difficulty(P, D),
    findall(Q, prerequisite(P, Q), Prereqs).