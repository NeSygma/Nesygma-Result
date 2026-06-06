% --- Instance Data ---
puzzle(1..6).
difficulty(1, 1).
difficulty(2, 1).
difficulty(3, 2).
difficulty(4, 2).
difficulty(5, 3).
difficulty(6, 3).

prereq(2, 1).
prereq(3, 2).
prereq(3, 4).
prereq(4, 1).
prereq(5, 3).
prereq(6, 5).

% --- Logic ---
time(1..6).

% Each puzzle must appear exactly once in the sequence
{ order(P, T) : time(T) } = 1 :- puzzle(P).
{ order(P, T) : puzzle(P) } = 1 :- time(T).

% A puzzle cannot be completed before all its prerequisites are completed
:- prereq(P, Pre), order(P, T1), order(Pre, T2), T1 <= T2.

% --- Output Mapping ---
puzzle_order(P, T) :- order(P, T).
difficulty_progression(T, D) :- order(P, T), difficulty(P, D).

#show puzzle_order/2.
#show difficulty_progression/2.